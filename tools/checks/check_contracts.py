"""E14: data contracts (standard STD-002).

Every exchange between components has one contract file in the contracts folder named in
appliance.yml (data.contracts_dir). Refuses when a contract file:
- does not parse, or is not a mapping
- misses id, kind, producer, consumers, version, compatibility or schema
- has a kind or compatibility mode outside the allowed values
- has no consumers: output no one reads (WorldSIM NM-038)
- has a version that is not MAJOR.MINOR.PATCH, or an empty schema
- shares its id with another contract

A project with no contracts folder passes; the check starts applying when the folder exists.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

from lib import Report, load_yaml, root_from_argv

KINDS = {"api", "event", "file", "table"}
COMPAT = {"backward", "forward", "full", "none"}
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
REQUIRED = ["id", "kind", "producer", "consumers", "version", "compatibility", "schema"]


def check(root: Path) -> Report:
    report = Report()
    data_cfg = (load_yaml(root / "appliance.yml").get("data") or {})
    cdir = root / data_cfg.get("contracts_dir", "contracts")
    if not cdir.is_dir():
        return report
    seen: dict[str, str] = {}
    for p in sorted([*cdir.rglob("*.yml"), *cdir.rglob("*.yaml")]):
        rel = str(p.relative_to(root))
        try:
            c = yaml.safe_load(p.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            report.add("E14", rel, f"does not parse: {e.__class__.__name__}")
            continue
        if not isinstance(c, dict):
            report.add("E14", rel, "a contract must be a mapping")
            continue
        for f in REQUIRED:
            if f == "consumers" and f in c:
                continue
            if f not in c or c[f] in (None, "", [], {}):
                report.add("E14", rel, f"missing '{f}'")
        if c.get("kind") and c["kind"] not in KINDS:
            report.add("E14", rel, f"kind '{c['kind']}' is not one of {sorted(KINDS)}")
        if c.get("compatibility") and c["compatibility"] not in COMPAT:
            report.add("E14", rel, f"compatibility '{c['compatibility']}' is not one of {sorted(COMPAT)}")
        if "consumers" in c and not c.get("consumers"):
            report.add("E14", rel, "no consumers: output no one reads is a dead contract (STD-002 clause 2)")
        if c.get("version") is not None and not SEMVER.match(str(c["version"])):
            report.add("E14", rel, f"version '{c['version']}' is not MAJOR.MINOR.PATCH")
        cid = c.get("id")
        if cid:
            if cid in seen:
                report.add("E14", rel, f"duplicate contract id '{cid}' (also {seen[cid]})")
            seen[str(cid)] = rel
    return report


if __name__ == "__main__":
    sys.exit(check(root_from_argv()).emit("E14 data contracts"))
