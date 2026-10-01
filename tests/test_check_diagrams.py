import check_diagrams
from conftest import REPO, messages
from lib import read_front_matter

ARCH_BODY = read_front_matter(REPO / "docs/templates/architecture.md")[1]
UX_BODY = read_front_matter(REPO / "docs/templates/ux-design.md")[1]
F = "```"


def arch(repo, body, status="in-review", **meta):
    repo.artifact("architecture", 1, body=body, status=status, parents=["CD-001"],
                  author_seat="Architect", challenger_seat="Builder", approver="Engineering Lead", **meta)


def test_draft_is_exempt(repo):
    arch(repo, "No diagrams yet.\n", status="draft")
    assert check_diagrams.check(repo.root).ok


def test_architecture_with_every_diagram_passes(repo):
    arch(repo, ARCH_BODY)
    report = check_diagrams.check(repo.root)
    assert report.ok, messages(report)


def test_refuses_architecture_in_review_without_diagrams(repo):
    arch(repo, "The order service writes to the database and publishes an event.\n")
    out = messages(check_diagrams.check(repo.root))
    for tag in ["context", "components", "data-model", "key-interactions", "deployment"]:
        assert f"missing required diagram '{tag}'" in out


def test_refuses_data_model_in_the_wrong_form(repo):
    body = ARCH_BODY.replace("erDiagram\n  CUSTOMER ||--o{ ORDER : places", "flowchart LR\n  CUSTOMER --> ORDER")
    arch(repo, body)
    assert "diagram 'data-model' must be a er diagram" in messages(check_diagrams.check(repo.root))


def test_refuses_data_model_with_no_relationships(repo):
    thin = f"<!-- diagram: data-model -->\n{F}mermaid\nerDiagram\n  ORDER {{\n    string id\n  }}\n{F}\n"
    start = ARCH_BODY.index("<!-- diagram: data-model -->")
    end = ARCH_BODY.index(F, ARCH_BODY.index(F + "mermaid\nerDiagram") + 3) + 3
    arch(repo, ARCH_BODY[:start] + thin + ARCH_BODY[end:])
    assert "diagram 'data-model' is too thin" in messages(check_diagrams.check(repo.root))


def test_refuses_unknown_tag(repo):
    arch(repo, ARCH_BODY + f"\n<!-- diagram: org-chart -->\n{F}mermaid\nflowchart LR\n  A --> B\n{F}\n")
    assert "unknown diagram tag 'org-chart'" in messages(check_diagrams.check(repo.root))


def test_untagged_diagram_does_not_count(repo):
    untagged = ARCH_BODY.replace("<!-- diagram: deployment -->\n", "")
    arch(repo, untagged)
    assert "missing required diagram 'deployment'" in messages(check_diagrams.check(repo.root))


def test_not_applicable_with_approver_passes(repo):
    body = UX_BODY.replace("<!-- diagram: navigation -->\n", "")
    repo.artifact("ux-design", 1, body=body, status="in-review", parents=["UC-001"],
                  author_seat="Designer", challenger_seat="Product", approver="Intent Owner",
                  diagrams={"navigation": {"not_applicable": "Single-screen tool", "approver": "Intent Owner"}})
    report = check_diagrams.check(repo.root)
    assert report.ok, messages(report)


def test_refuses_not_applicable_without_approver(repo):
    body = UX_BODY.replace("<!-- diagram: navigation -->\n", "")
    repo.artifact("ux-design", 1, body=body, status="in-review", parents=["UC-001"],
                  author_seat="Designer", challenger_seat="Product", approver="Intent Owner",
                  diagrams={"navigation": {"not_applicable": "Single-screen tool"}})
    assert "not-applicable without an approver" in messages(check_diagrams.check(repo.root))


def test_refuses_ux_design_without_user_flows(repo):
    repo.artifact("ux-design", 1, body="Screens are described in prose.\n", status="approved",
                  parents=["UC-001"], author_seat="Designer", challenger_seat="Product", approver="Intent Owner")
    out = messages(check_diagrams.check(repo.root))
    assert "missing required diagram 'user-flows'" in out
    assert "missing required diagram 'navigation'" in out


def test_tagged_state_diagram_elsewhere_is_checked(repo):
    body = f"<!-- diagram: states -->\n{F}mermaid\nflowchart LR\n  A --> B\n{F}\n"
    repo.artifact("increment-intent", 1, body=body, status="in-review", parents=["PLAN-001"], challenger_seat="Verifier")
    assert "diagram 'states' must be a state diagram" in messages(check_diagrams.check(repo.root))
