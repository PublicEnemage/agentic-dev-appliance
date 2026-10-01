import check_seats
from conftest import messages

LAYERS = ["data", "domain-core", "services-apis", "frontend", "integration", "deployment-runtime", "operations"]


def good_layers():
    layers = {
        "data": {"author_seat": "Architect", "challenger_seat": "Builder"},
        "services-apis": {"author_seat": "Architect", "challenger_seat": "Builder"},
        "frontend": {"author_seat": "Architect", "challenger_seat": "Builder"},
        "integration": {"author_seat": "Architect", "challenger_seat": "Operator"},
        "deployment-runtime": {"author_seat": "Operator", "challenger_seat": "Architect"},
        "operations": {"author_seat": "Operator", "challenger_seat": "Verifier"},
        "domain-core": {"not_applicable": "Thin CRUD product; no domain computation", "approver": "Engineering Lead"},
    }
    return layers


def test_default_roster_and_clean_artifact_pass(repo):
    repo.artifact("intent", 1)
    report = check_seats.check(repo.root)
    assert report.ok, messages(report)


def test_refuses_author_as_approver(repo):
    repo.artifact("story", 1, author_seat="Product", challenger_seat="Verifier", approver="Product")
    assert "author and approver are the same seat" in messages(check_seats.check(repo.root))


def test_refuses_author_as_challenger(repo):
    repo.artifact("intent", 1, author_seat="Product", challenger_seat="Product")
    assert "author and challenger are the same seat" in messages(check_seats.check(repo.root))


def test_refuses_author_and_challenger_on_one_holder(repo):
    # Product and Operator are both held by Agent A in the default roster.
    repo.artifact("intent", 1, author_seat="Product", challenger_seat="Operator")
    assert "share holder 'Agent A'" in messages(check_seats.check(repo.root))


def test_refuses_unknown_seat(repo):
    repo.artifact("intent", 1, challenger_seat="QA Lead")
    assert "'QA Lead' is not a seat" in messages(check_seats.check(repo.root))


def test_refuses_steward_on_an_artifact(repo):
    repo.artifact("intent", 1, challenger_seat="Steward")
    assert "the Steward holds no artifact seat" in messages(check_seats.check(repo.root))


def test_refuses_agent_approver_on_business_artifact(repo):
    repo.artifact("intent", 1, author_seat="Product", challenger_seat="Verifier", approver="Architect")
    assert "needs a human approver" in messages(check_seats.check(repo.root))


def test_refuses_holder_with_incompatible_pair(repo):
    repo.edit_yaml("docs/roles.yml", lambda r: r["holders"].update({"Agent C": ["Builder", "Verifier"]}))
    assert "holds incompatible seats Builder and Verifier" in messages(check_seats.check(repo.root))


def test_refuses_steward_sharing_a_holder(repo):
    repo.edit_yaml("docs/roles.yml", lambda r: r["holders"].update({"Agent E": ["Steward", "Delivery"]}))
    assert "holds the Steward seat with other seats" in messages(check_seats.check(repo.root))


def test_refuses_shared_human_holder_without_disclosure_flag(repo):
    repo.edit_yaml("appliance.yml", lambda a: a.update({"single_principal": False}))
    assert "set single_principal: true" in messages(check_seats.check(repo.root))


def test_architecture_with_every_layer_qualified_passes(repo):
    repo.artifact("intent", 1)
    repo.artifact("architecture", 1, parents=["INTENT-001"], author_seat="Architect",
                  challenger_seat="Builder", approver="Engineering Lead", layers=good_layers())
    report = check_seats.check(repo.root)
    assert report.ok, messages(report)


def test_refuses_architecture_missing_a_layer(repo):
    layers = good_layers()
    del layers["frontend"]
    repo.artifact("architecture", 1, parents=["INTENT-001"], author_seat="Architect",
                  challenger_seat="Builder", approver="Engineering Lead", layers=layers)
    assert "layer 'frontend' has no section" in messages(check_seats.check(repo.root))


def test_refuses_unqualified_layer_seat_and_points_to_crew_review(repo):
    # The WorldSIM case: domain-core needed, but no seat's charter covers it.
    layers = good_layers()
    layers["domain-core"] = {"author_seat": "Architect", "challenger_seat": "Builder"}
    repo.artifact("architecture", 1, parents=["INTENT-001"], author_seat="Architect",
                  challenger_seat="Builder", approver="Engineering Lead", layers=layers)
    out = messages(check_seats.check(repo.root))
    assert "layer 'domain-core': Architect is not qualified" in out
    assert "open a crew review" in out


def test_refuses_layer_author_and_challenger_on_one_holder(repo):
    layers = good_layers()
    layers["frontend"] = {"author_seat": "Designer", "challenger_seat": "Architect"}
    repo.artifact("architecture", 1, parents=["INTENT-001"], author_seat="Architect",
                  challenger_seat="Builder", approver="Engineering Lead", layers=layers)
    assert "layer 'frontend' author and challenger share holder 'Agent B'" in messages(check_seats.check(repo.root))


def test_refuses_not_applicable_layer_without_approver(repo):
    layers = good_layers()
    layers["domain-core"] = {"not_applicable": "No domain logic"}
    repo.artifact("architecture", 1, parents=["INTENT-001"], author_seat="Architect",
                  challenger_seat="Builder", approver="Engineering Lead", layers=layers)
    assert "not-applicable without an approver" in messages(check_seats.check(repo.root))


def test_refuses_domain_area_no_seat_can_challenge(repo):
    repo.artifact("business-case", 1, parents=["INTENT-001"], challenger_seat="Verifier",
                  domain_areas=[{"area": "airspace-rules"}])
    assert "no seat is qualified to challenge domain area 'airspace-rules'" in messages(check_seats.check(repo.root))


def test_domain_area_with_qualified_seat_passes(repo):
    def add_domain(r):
        r["seats"]["Domain Advisor"] = {"kind": "agent", "concern": "Airspace rules", "qualified_layers": ["domain-core"]}
        r["holders"]["Agent F"] = ["Domain Advisor"]
        r["qualified_domains"] = {"airspace-rules": ["Domain Advisor"]}
    repo.edit_yaml("docs/roles.yml", add_domain)
    repo.artifact("intent", 1)
    repo.artifact("business-case", 1, parents=["INTENT-001"], challenger_seat="Verifier",
                  domain_areas=[{"area": "airspace-rules"}])
    report = check_seats.check(repo.root)
    assert report.ok, messages(report)
