"""Every artifact template must carry the required fields and a seat assignment that the
seat check accepts under the default roster. A template that fails its own checks would
teach every new project the wrong thing."""

import check_seats
import pytest
import yaml
from conftest import REPO, TYPES, messages
from lib import read_front_matter

TEMPLATES = sorted(p for p in (REPO / "docs/templates").glob("*.md")
                   if (read_front_matter(p)[0] or {}).get("type"))
REQUIRED = yaml.safe_load((REPO / "docs/artifact-types.yml").read_text())["required_fields"]


def test_every_artifact_type_has_a_template():
    covered = {read_front_matter(p)[0]["type"] for p in TEMPLATES}
    assert covered == set(TYPES), sorted(set(TYPES) - covered)


@pytest.mark.parametrize("template", TEMPLATES, ids=lambda p: p.stem)
def test_template_has_required_fields(template):
    meta, _ = read_front_matter(template)
    missing = [f for f in REQUIRED if f not in meta]
    assert not missing, missing


@pytest.mark.parametrize("template", TEMPLATES, ids=lambda p: p.stem)
def test_template_seats_pass_the_seat_check(repo, template):
    meta, body = read_front_matter(template)
    t = TYPES[meta["type"]]
    meta.update({"id": f"{t['prefix']}-001", "layers": None, "domain_areas": None})
    repo.write(f"{t['dir']}/{t['prefix']}-001-sample.md",
               "---\n" + yaml.safe_dump(meta, sort_keys=False) + "---\n" + body)
    report = check_seats.check(repo.root)
    seat_findings = [f for f in report.findings if f.check == "SEATS"]
    assert not seat_findings, messages(report)


@pytest.mark.parametrize("template", TEMPLATES, ids=lambda p: p.stem)
def test_template_carries_valid_starter_diagrams(template):
    """Each required diagram appears in the template as a tagged, well-formed sample,
    so a new artifact starts with the picture rather than a blank."""
    from check_diagrams import diagram_problems
    types_cfg = yaml.safe_load((REPO / "docs/artifact-types.yml").read_text())
    meta, body = read_front_matter(template)
    required = types_cfg["required_diagrams"].get(meta["type"], [])
    assert diagram_problems(body, required, {}, types_cfg) == []


def test_role_proposal_template_teaches_the_job_description():
    """The template's front matter carries every charter line the crew check reads."""
    meta, _ = read_front_matter(REPO / "docs/templates/role-proposal.md")
    assert set(meta["charter"]) == {"trigger", "inputs", "value", "outputs", "standards", "templates", "verifier"}
    assert set(meta["charter"]["verifier"]) == {"seat", "evidence"}
    assert {"proposed_seat", "peer_review", "peer_recommendation"} <= set(meta)
