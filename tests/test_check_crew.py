import copy

import check_crew
import pytest
from conftest import messages


def good(**over):
    """A complete proposal under the default roster. Author Delivery sits on Agent A."""
    meta = {
        "status": "in-review",
        "author_seat": "Delivery",
        "challenger_seat": "Architect",
        "approver": "Engineering Lead",
        "proposed_seat": "Accessibility Reviewer",
        "charter": {
            "trigger": "A UX design artifact enters review",
            "inputs": [{"artifact": "ux-design", "from": "Designer"}],
            "value": "Judges flows against accessibility standards before build starts",
            "outputs": [{"artifact": "review", "for": "Builder", "acceptance": "Every finding has a fix or a reasoned decline"}],
            "standards": ["docs/standards/data/README.md"],
            "templates": ["docs/templates/review.md"],
            "verifier": {"seat": "Verifier", "evidence": "Review files exist beside each UX design and cite the standard"},
        },
        "peer_review": [
            {"seat": "Designer", "recommendation": "accept", "demand": "Hands over flows for review", "evidence": "NM-014 UI shipped without it"},
            {"seat": "Builder", "recommendation": "accept-with-conditions", "demand": "Takes findings as tasks", "evidence": "Two rework cycles"},
        ],
        "peer_recommendation": "accept-with-conditions",
    }
    for k, v in over.items():
        meta[k] = v
    return meta


def charter(**over):
    c = copy.deepcopy(good()["charter"])
    c.update(over)
    return {"charter": c}


def run(repo, **over):
    repo.write("docs/standards/data/README.md", "Standard.\n")
    repo.write("docs/templates/review.md", "Template.\n")
    repo.artifact("role-proposal", 1, review=False, **good(**over))
    return check_crew.check(repo.root)


def test_complete_proposal_passes(repo):
    report = run(repo)
    assert report.ok, messages(report)


def test_drafts_are_exempt(repo):
    assert run(repo, status="draft", charter={}).ok


@pytest.mark.parametrize("key", ["trigger", "value"])
def test_refuses_missing_charter_text(repo, key):
    c = good()["charter"]
    del c[key]
    assert f"charter.{key} is missing" in messages(run(repo, charter=c))


def test_refuses_input_without_a_sender(repo):
    c = good()["charter"]
    c["inputs"] = [{"artifact": "ux-design"}]
    assert "charter.inputs #1 needs 'artifact' and 'from'" in messages(run(repo, charter=c))


def test_refuses_input_from_a_phantom_seat(repo):
    c = good()["charter"]
    c["inputs"] = [{"artifact": "ux-design", "from": "QA Lead"}]
    assert "'QA Lead', which is not a seat" in messages(run(repo, charter=c))


def test_refuses_output_without_acceptance(repo):
    c = good()["charter"]
    c["outputs"] = [{"artifact": "review", "for": "Builder"}]
    assert "'acceptance'" in messages(run(repo, charter=c))


def test_refuses_work_nobody_consumes(repo):
    c = good()["charter"]
    c["outputs"] = [{"artifact": "review", "for": "Accessibility Reviewer", "acceptance": "n/a"}]
    assert "for the proposed seat itself" in messages(run(repo, charter=c))


def test_refuses_input_from_the_proposed_seat(repo):
    c = good()["charter"]
    c["inputs"] = [{"artifact": "ux-design", "from": "Accessibility Reviewer"}]
    assert "comes from the proposed seat itself" in messages(run(repo, charter=c))


def test_refuses_missing_standards_and_templates(repo):
    c = good()["charter"]
    c["standards"] = []
    c["templates"] = ["{{docs/templates/...}}"]
    out = messages(run(repo, charter=c))
    assert "charter.standards needs at least one entry" in out
    assert "charter.templates needs at least one entry" in out


def test_refuses_a_template_that_does_not_exist(repo):
    c = good()["charter"]
    c["templates"] = ["docs/templates/nope.md"]
    assert "'docs/templates/nope.md' does not exist" in messages(run(repo, charter=c))


def test_refuses_missing_verifier_evidence(repo):
    c = good()["charter"]
    c["verifier"] = {"seat": "Verifier"}
    assert "charter.verifier needs 'seat' and 'evidence'" in messages(run(repo, charter=c))


def test_refuses_verifier_who_is_the_author(repo):
    c = good()["charter"]
    c["verifier"] = {"seat": "Delivery", "evidence": "own notes"}
    assert "the verifier is the author" in messages(run(repo, charter=c))


def test_refuses_verifier_on_the_authors_holder(repo):
    c = good()["charter"]
    c["verifier"] = {"seat": "Operator", "evidence": "files"}  # Operator and Delivery share Agent A
    assert "share holder 'Agent A'" in messages(run(repo, charter=c))


def test_refuses_fewer_than_two_peers(repo):
    peers = good()["peer_review"][:1]
    assert "at least two distinct peers" in messages(run(repo, peer_review=peers))


def test_refuses_author_as_peer(repo):
    peers = good()["peer_review"] + [{"seat": "Delivery", "recommendation": "accept", "demand": "x", "evidence": "y"}]
    assert "the author cannot be a peer" in messages(run(repo, peer_review=peers))


def test_refuses_peer_on_the_authors_holder(repo):
    peers = good()["peer_review"] + [{"seat": "Operator", "recommendation": "accept", "demand": "x", "evidence": "y"}]
    assert "shares holder 'Agent A' with the author" in messages(run(repo, peer_review=peers))


def test_refuses_human_peer(repo):
    peers = good()["peer_review"] + [{"seat": "Engineering Lead", "recommendation": "accept", "demand": "x", "evidence": "y"}]
    assert "human seat" in messages(run(repo, peer_review=peers))


def test_refuses_peer_without_demand_or_evidence(repo):
    peers = good()["peer_review"]
    peers[0]["evidence"] = ""
    assert "needs 'demand'" in messages(run(repo, peer_review=peers))


def test_refuses_when_a_consumer_gave_no_review(repo):
    c = good()["charter"]
    c["outputs"].append({"artifact": "report", "for": "Verifier", "acceptance": "Complete"})
    assert "seat 'Verifier' sends input to or consumes output" in messages(run(repo, charter=c))


def test_refuses_group_more_favourable_than_its_members(repo):
    assert "more favourable than its least favourable peer" in messages(run(repo, peer_recommendation="accept"))


def test_refuses_approval_over_a_rejection(repo):
    peers = good()["peer_review"]
    peers[1]["recommendation"] = "reject"
    out = messages(run(repo, status="approved", peer_review=peers, peer_recommendation="reject"))
    assert "approved while the peer group recommends rejection" in out


def test_refuses_proposing_a_seat_that_exists(repo):
    assert "already exists" in messages(run(repo, proposed_seat="Builder"))


def test_refuses_unfilled_placeholders(repo):
    assert "proposed_seat is missing" in messages(run(repo, proposed_seat="{{Name of the new seat}}"))
