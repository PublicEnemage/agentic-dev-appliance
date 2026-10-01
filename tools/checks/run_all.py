"""Run every implemented appliance check. Exit non-zero if any check fails.

Usage:
    python tools/checks/run_all.py [--root PATH] [--gate case|design|plan|release] [--base REF]
"""

from __future__ import annotations

import sys

import check_artifacts
import check_caps
import check_contracts
import check_crew
import check_diagrams
import check_dor
import check_migrations
import check_registry
import check_seats
import check_test_noops
from lib import root_from_argv


def main(argv: list[str]) -> int:
    root = root_from_argv(argv)
    gate = argv[argv.index("--gate") + 1] if "--gate" in argv else None
    base = argv[argv.index("--base") + 1] if "--base" in argv else None
    results = [
        check_artifacts.check(root).emit("E10 artifacts"),
        check_seats.check(root).emit("SEATS"),
        check_dor.check(root, gate).emit(f"DOR{' gate ' + gate if gate else ''}"),
        check_caps.check(root).emit("E9 caps"),
        check_registry.check(root).emit("E11 registry"),
        check_test_noops.check(root).emit("E3 test no-ops"),
        check_contracts.check(root).emit("E14 data contracts"),
        check_migrations.check(root, base).emit("E15 migrations"),
        check_diagrams.check(root).emit("E16 diagrams"),
        check_crew.check(root).emit("E17 crew proposals"),
    ]
    failed = sum(results)
    print(f"\n{len(results) - failed}/{len(results)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
