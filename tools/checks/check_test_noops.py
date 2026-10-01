"""E3 (static part): tests that can pass while measuring nothing.

WorldSIM's largest hazard class was false green: tests that returned early, swallowed
an error, or were skipped in bulk while CI stayed green (NM-027, 028, 047, 056, 058,
061, 096). This lint refuses those shapes.

Python test files (test_*.py, *_test.py), inside test functions:
- any return statement (a test has nothing to return; an early return is a silent pass)
- an except clause whose body is only pass, or that returns
- pytest.skip(...) or pytest.xfail(...) called in the body
- a non-strict xfail marker (strict expected-fail is how red-first tests land; see E2)
Python test files, file or class level:
- pytestmark with skip or skipif, or a skip marker on a class (blanket skip)

JavaScript and TypeScript test files (*.spec.*, *.test.*):
- describe.skip, test.describe.skip or describe.fixme (blanket skip)
- a bare `return;`, or `if (...) return;` with no value
- .catch(() => false | null | undefined | {}) and empty catch blocks

Per-test skips are allowed only with a skip-registry id that has not expired:
- Python: @pytest.mark.skip(reason="SKIP-001: ...")
- JS/TS:  test.skip(...)  // skip-registry: SKIP-001
The skip registry is docs/skips.yml. An expired or unknown id fails.

The runtime zero-assertion check arrives with E2 (v0.3).
"""

from __future__ import annotations

import ast
import datetime as dt
import re
import sys
from pathlib import Path

from lib import Report, load_yaml, root_from_argv, to_datetime

SKIP_ID = re.compile(r"\bSKIP-\d{3}\b")
PY_TEST = re.compile(r"^(test_.*|.*_test)\.py$")
JS_TEST = re.compile(r"\.(spec|test)\.(c|m)?[jt]sx?$")
EXCLUDED_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build"}

JS_RULES = [
    (re.compile(r"\b(?:test\.)?describe\.(?:skip|fixme)\s*\("), "blanket skip of a whole describe block"),
    (re.compile(r"^\s*return\s*;?\s*(?://.*)?$"), "bare return in a test file; an early return passes silently"),
    (re.compile(r"\bif\s*\(.*\)\s*\{?\s*return\s*;?\s*\}?\s*$"), "conditional early return; the test passes without asserting"),
    (re.compile(r"\.catch\(\s*\(?[^)]*\)?\s*=>\s*(?:false|null|undefined|\{\s*\})\s*\)"), "catch-to-false hides the failure"),
    (re.compile(r"\bcatch\s*(?:\([^)]*\))?\s*\{\s*\}"), "empty catch block hides the failure"),
]
JS_PER_TEST_SKIP = re.compile(r"\b(?:test|it)\.(?:skip|fixme)\s*\(")


def load_skips(root: Path, report: Report) -> dict[str, dt.datetime | None]:
    path = root / "docs/skips.yml"
    if not path.is_file():
        return {}
    data = load_yaml(path)
    out = {}
    for e in data.get("skips") or []:
        sid = str(e.get("id"))
        out[sid] = to_datetime(e.get("expires"))
        for f in ("id", "test", "owner", "expires", "reason"):
            if not e.get(f):
                report.add("E3", "docs/skips.yml", f"{sid}: missing '{f}'")
    return out


def skip_problem(text: str, skips: dict, today: dt.datetime) -> str | None:
    ids = SKIP_ID.findall(text or "")
    if not ids:
        return "skip without a skip-registry id (docs/skips.yml)"
    for sid in ids:
        if sid not in skips:
            return f"skip cites {sid}, which is not in docs/skips.yml"
        exp = skips[sid]
        if exp is None or exp < today:
            return f"skip {sid} has expired; fix the test or renew the entry"
    return None


def marker_name(dec: ast.expr) -> tuple[str, ast.Call | None]:
    call = dec if isinstance(dec, ast.Call) else None
    node = dec.func if call else dec
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
    return ".".join(reversed(parts)), call


def call_text(call: ast.Call | None, src: str) -> str:
    return ast.get_source_segment(src, call) or "" if call is not None else ""


class PyVisitor(ast.NodeVisitor):
    def __init__(self, rel: str, src: str, report: Report, skips: dict, today: dt.datetime):
        self.rel, self.src, self.report, self.skips, self.today = rel, src, report, skips, today

    def add(self, node: ast.AST, msg: str) -> None:
        self.report.add("E3", f"{self.rel}:{getattr(node, 'lineno', 0)}", msg)

    def check_markers(self, decorators, is_class: bool) -> None:
        for dec in decorators:
            name, call = marker_name(dec)
            if name.endswith("mark.skip") or name.endswith("mark.skipif"):
                if is_class:
                    self.add(dec, "blanket skip on a test class; skips apply to one test")
                else:
                    problem = skip_problem(call_text(call, self.src), self.skips, self.today)
                    if problem:
                        self.add(dec, problem)
            if name.endswith("mark.xfail"):
                strict = call and any(k.arg == "strict" and isinstance(k.value, ast.Constant) and k.value.value is True for k in call.keywords)
                if not strict:
                    self.add(dec, "xfail must be strict=True, so it fails if the test starts passing")

    def visit_Module(self, node: ast.Module) -> None:
        for stmt in node.body:
            if isinstance(stmt, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "pytestmark" for t in stmt.targets):
                seg = ast.get_source_segment(self.src, stmt.value) or ""
                if "skip" in seg:
                    self.add(stmt, "blanket skip via pytestmark; skips apply to one test")
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.check_markers(node.decorator_list, is_class=True)
        self.generic_visit(node)

    def visit_FunctionDef(self, node) -> None:
        if node.name.startswith("test"):
            self.check_markers(node.decorator_list, is_class=False)
            self.check_body(node)
        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef

    def check_body(self, fn) -> None:
        stack = list(fn.body)
        while stack:
            n = stack.pop()
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
                continue
            if isinstance(n, ast.Return):
                self.add(n, f"return inside test '{fn.name}'; an early return passes silently")
            if isinstance(n, ast.ExceptHandler) and all(isinstance(b, ast.Pass) for b in n.body):
                self.add(n, f"except clause in '{fn.name}' swallows the failure")
            if isinstance(n, ast.Call):
                name, _ = marker_name(n)
                if name in ("pytest.skip", "pytest.xfail"):
                    self.add(n, f"{name}() in the body of '{fn.name}'; use a registered per-test marker")
            stack.extend(ast.iter_child_nodes(n))


def iter_files(root: Path):
    for p in root.rglob("*"):
        if not p.is_file() or EXCLUDED_DIRS & set(p.relative_to(root).parts):
            continue
        if p.relative_to(root).parts[:2] == ("tests", "fixtures"):
            continue
        yield p


def check(root: Path, today: dt.datetime | None = None) -> Report:
    report = Report()
    today = today or dt.datetime.now()
    skips = load_skips(root, report)
    for p in iter_files(root):
        rel = str(p.relative_to(root))
        if PY_TEST.match(p.name):
            src = p.read_text(encoding="utf-8")
            try:
                tree = ast.parse(src)
            except SyntaxError as e:
                report.add("E3", rel, f"does not parse: {e.msg}")
                continue
            PyVisitor(rel, src, report, skips, today).visit(tree)
        elif JS_TEST.search(p.name):
            for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                for rx, msg in JS_RULES:
                    if rx.search(line):
                        report.add("E3", f"{rel}:{i}", msg)
                if JS_PER_TEST_SKIP.search(line):
                    problem = skip_problem(line, skips, today)
                    if problem:
                        report.add("E3", f"{rel}:{i}", problem)
    return report


if __name__ == "__main__":
    sys.exit(check(root_from_argv()).emit("E3 test no-ops"))
