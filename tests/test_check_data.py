import subprocess

import check_contracts
import check_migrations
import check_seats
from conftest import messages

GOOD = """id: orders.created
kind: event
producer: order-service
consumers: [billing-service]
version: 1.2.0
compatibility: backward
schema:
  type: object
  required: [order_id]
"""


# E14 data contracts

def test_no_contracts_folder_passes(repo):
    assert check_contracts.check(repo.root).ok


def test_valid_contract_passes(repo):
    repo.write("contracts/orders-created.yml", GOOD)
    report = check_contracts.check(repo.root)
    assert report.ok, messages(report)


def test_refuses_contract_with_no_consumers(repo):
    # WorldSIM NM-038: events emitted that nothing consumed.
    repo.write("contracts/orders-created.yml", GOOD.replace("consumers: [billing-service]", "consumers: []"))
    assert "no consumers" in messages(check_contracts.check(repo.root))


def test_refuses_contract_missing_producer(repo):
    repo.write("contracts/orders-created.yml", GOOD.replace("producer: order-service\n", ""))
    assert "missing 'producer'" in messages(check_contracts.check(repo.root))


def test_refuses_unknown_kind_and_compatibility(repo):
    repo.write("contracts/orders-created.yml", GOOD.replace("kind: event", "kind: carrier-pigeon").replace("compatibility: backward", "compatibility: loose"))
    out = messages(check_contracts.check(repo.root))
    assert "kind 'carrier-pigeon'" in out
    assert "compatibility 'loose'" in out


def test_refuses_bad_version(repo):
    repo.write("contracts/orders-created.yml", GOOD.replace("version: 1.2.0", "version: v2"))
    assert "not MAJOR.MINOR.PATCH" in messages(check_contracts.check(repo.root))


def test_refuses_duplicate_contract_id(repo):
    repo.write("contracts/a.yml", GOOD)
    repo.write("contracts/b.yml", GOOD)
    assert "duplicate contract id 'orders.created'" in messages(check_contracts.check(repo.root))


def test_refuses_unparseable_contract(repo):
    repo.write("contracts/broken.yml", "id: [unclosed\n")
    assert "does not parse" in messages(check_contracts.check(repo.root))


# E15 append-only migrations

def git(root, *args):
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


def base_commit(repo):
    """Commit the repository with one merged migration; return the commit id."""
    repo.write("migrations/001_create_orders.sql", "CREATE TABLE orders (id TEXT);\n")
    git(repo.root, "init", "-q", "-b", "main")
    git(repo.root, "-c", "user.name=t", "-c", "user.email=t@t", "add", "-A")
    git(repo.root, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "base")
    out = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo.root, capture_output=True, text=True, check=True)
    return out.stdout.strip()


def commit_all(repo):
    git(repo.root, "-c", "user.name=t", "-c", "user.email=t@t", "add", "-A")
    git(repo.root, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "change")


def test_no_migrations_folder_passes(repo):
    assert check_migrations.check(repo.root, "does-not-matter").ok


def test_adding_a_migration_passes(repo):
    base = base_commit(repo)
    repo.write("migrations/002_add_total.sql", "ALTER TABLE orders ADD total NUMERIC;\n")
    commit_all(repo)
    report = check_migrations.check(repo.root, base)
    assert report.ok, messages(report)


def test_refuses_edited_migration(repo):
    base = base_commit(repo)
    repo.write("migrations/001_create_orders.sql", "CREATE TABLE orders (id TEXT, total NUMERIC);\n")
    commit_all(repo)
    assert "merged migration edited" in messages(check_migrations.check(repo.root, base))


def test_refuses_deleted_migration(repo):
    base = base_commit(repo)
    (repo.root / "migrations/001_create_orders.sql").unlink()
    repo.write("migrations/.keep", "")
    commit_all(repo)
    assert "merged migration deleted" in messages(check_migrations.check(repo.root, base))


def test_refuses_renamed_migration(repo):
    base = base_commit(repo)
    (repo.root / "migrations/001_create_orders.sql").rename(repo.root / "migrations/001_orders.sql")
    commit_all(repo)
    assert "merged migration deleted" in messages(check_migrations.check(repo.root, base))


def test_refuses_to_pass_silently_without_a_base(repo):
    base_commit(repo)
    out = messages(check_migrations.check(repo.root, "origin/nowhere"))
    assert "cannot resolve base ref 'origin/nowhere'" in out


# Optional Data Architect seat

def test_refuses_unadopted_optional_seat_on_an_artifact(repo):
    repo.artifact("standard", 1, author_seat="Data Architect", challenger_seat="Verifier", approver="Engineering Lead")
    assert "optional seat no one holds" in messages(check_seats.check(repo.root))


def test_adopted_optional_seat_passes(repo):
    repo.edit_yaml("docs/roles.yml", lambda r: r["holders"].update({"Agent F": ["Data Architect"]}))
    repo.artifact("standard", 1, author_seat="Data Architect", challenger_seat="Verifier", approver="Engineering Lead")
    report = check_seats.check(repo.root)
    assert report.ok, messages(report)


def test_refuses_data_architect_held_with_builder(repo):
    repo.edit_yaml("docs/roles.yml", lambda r: r["holders"].update({"Agent C": ["Builder", "Data Architect"]}))
    assert "holds incompatible seats Builder and Data Architect" in messages(check_seats.check(repo.root))
