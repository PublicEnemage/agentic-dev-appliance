"""Tests for the E3 lint. The bad samples are written into a temp repository as strings,
so this file itself stays clean under the lint it tests."""

import datetime as dt

import check_test_noops
from conftest import messages

TODAY = dt.datetime(2026, 10, 1)

SKIPS = """skips:
  - id: SKIP-001
    test: tests/test_sample.py::test_waits
    owner: Verifier
    expires: 2026-12-01
    reason: Fixture lands in INC-004
  - id: SKIP-002
    test: tests/test_sample.py::test_old
    owner: Verifier
    expires: 2026-09-01
    reason: Expired on purpose
"""


def lint(repo, rel, source):
    repo.write("docs/skips.yml", SKIPS)
    repo.write(rel, source)
    return messages(check_test_noops.check(repo.root, today=TODAY))


def test_clean_python_test_passes(repo):
    out = lint(repo, "tests/test_sample.py", "def test_adds():\n    assert 1 + 1 == 2\n")
    assert out == ""


def test_refuses_python_early_return(repo):
    src = "def test_panel(page):\n    if not page:\n        return\n    assert page.ok\n"
    assert "early return passes silently" in lint(repo, "tests/test_sample.py", src)


def test_refuses_python_swallowed_exception(repo):
    src = "def test_call():\n    try:\n        call()\n    except Exception:\n        pass\n"
    assert "swallows the failure" in lint(repo, "tests/test_sample.py", src)


def test_refuses_python_in_body_skip(repo):
    src = "import pytest\n\ndef test_db():\n    pytest.skip('no db')\n"
    assert "pytest.skip() in the body" in lint(repo, "tests/test_sample.py", src)


def test_refuses_python_blanket_skip(repo):
    src = "import pytest\npytestmark = pytest.mark.skip(reason='later')\n\ndef test_a():\n    assert True\n"
    assert "blanket skip via pytestmark" in lint(repo, "tests/test_sample.py", src)


def test_refuses_python_class_skip(repo):
    src = "import pytest\n\n@pytest.mark.skip(reason='SKIP-001')\nclass TestGroup:\n    def test_a(self):\n        assert True\n"
    assert "blanket skip on a test class" in lint(repo, "tests/test_sample.py", src)


def test_python_registered_skip_passes(repo):
    src = "import pytest\n\n@pytest.mark.skip(reason='SKIP-001: fixture pending')\ndef test_waits():\n    assert True\n"
    assert lint(repo, "tests/test_sample.py", src) == ""


def test_refuses_python_unregistered_skip(repo):
    src = "import pytest\n\n@pytest.mark.skip(reason='flaky')\ndef test_waits():\n    assert True\n"
    assert "skip without a skip-registry id" in lint(repo, "tests/test_sample.py", src)


def test_refuses_python_expired_skip(repo):
    src = "import pytest\n\n@pytest.mark.skip(reason='SKIP-002')\ndef test_old():\n    assert True\n"
    assert "SKIP-002 has expired" in lint(repo, "tests/test_sample.py", src)


def test_refuses_python_non_strict_xfail(repo):
    src = "import pytest\n\n@pytest.mark.xfail\ndef test_red():\n    assert False\n"
    assert "xfail must be strict=True" in lint(repo, "tests/test_sample.py", src)


def test_python_strict_xfail_passes(repo):
    src = "import pytest\n\n@pytest.mark.xfail(strict=True)\ndef test_red():\n    assert False\n"
    assert lint(repo, "tests/test_sample.py", src) == ""


def test_refuses_ts_conditional_early_return(repo):
    src = "test('panel', async ({ page }) => {\n  const ok = await page.isVisible('#p');\n  if (!ok) return;\n  expect(ok).toBe(true);\n});\n"
    assert "conditional early return" in lint(repo, "e2e/panel.spec.ts", src)


def test_refuses_ts_catch_to_false(repo):
    src = "test('svg', async ({ page }) => {\n  const has = await svg.isVisible().catch(() => false);\n  expect(has).toBe(true);\n});\n"
    assert "catch-to-false" in lint(repo, "e2e/svg.spec.ts", src)


def test_refuses_ts_blanket_describe_skip(repo):
    src = "test.describe.skip('cluster', () => {\n  test('a', () => {});\n});\n"
    assert "blanket skip of a whole describe block" in lint(repo, "e2e/cluster.spec.ts", src)


def test_ts_registered_per_test_skip_passes(repo):
    src = "test.skip('waits', async () => {}); // skip-registry: SKIP-001\n"
    assert lint(repo, "e2e/waits.spec.ts", src) == ""


def test_refuses_ts_unregistered_skip(repo):
    src = "test.fixme('perf on shared runner', async () => {});\n"
    assert "skip without a skip-registry id" in lint(repo, "e2e/perf.spec.ts", src)
