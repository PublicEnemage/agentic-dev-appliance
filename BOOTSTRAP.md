# Bootstrap

How a new project starts from this template. Cycle 1 builds no product code. Cycle 1 is
setup, the smoke cycle and the discovery track.

## Steps

1. **Create the repository** from this template. Pin `floor_version` in `appliance.yml`.
2. **Create identities and rules.** Until check E1 ships (v0.2), agents commit under the
   human's GitHub identity. Keep `single_principal: true` and the disclosure in `CLAUDE.md`.
   Protect `main`, and every other lane you create, with required checks.
3. **Name the human seats.** Fill the Intent Owner and Engineering Lead in `CLAUDE.md`.
4. **Bootstrap session.** One agent session fills the slots:
   - `CLAUDE.md`: mission and principles
   - `docs/roles.yml`: narrow each seat's `qualified_layers` to what its holder can judge,
     and name the seat for `domain-core` and any `qualified_domains`
   - `.github/CODEOWNERS`: the right handles
   - `appliance.yml`: grade and merge autonomy
5. **Challenge the bootstrap.** A fresh session, a different seat, reviews the bootstrap
   output against `docs/dor/floor.yml` and `docs/roles.yml`. It is asked to find what is
   wrong or missing. The bootstrap author never approves its own setup.
6. **Approve.** The Engineering Lead reviews the challenge and merges.
7. **Install the hooks:** `git config core.hooksPath .githooks`
8. **Smoke cycle.** On a branch, break each check on purpose and confirm it refuses:
   - an artifact in the wrong folder (E10)
   - an artifact whose author is also its approver (SEATS)
   - a deleted floor row in `docs/dor/checklist.yml` (DOR)
   - a test with an early return (E3)
   - a registry entry with a gap in its IDs (E11)

   Record the date and results in `STATE.md`. Discard the branch.
9. **Discovery track.** Write the intent and business case with the Intent Owner, then
   users, use cases, NFRs and the risk assessment. Run
   `python tools/checks/check_dor.py --gate case` until the case gate passes.

Delivery starts once the case and design gates pass and there is baselined work to pull.

## Checks

```
pip install -r tools/checks/requirements.txt
python tools/checks/run_all.py              # every implemented check
python tools/checks/run_all.py --gate case  # also require the case gate rows
python -m pytest -q tests                   # the checks' own tests
```

What each check enforces, and what is still advisory, is in `docs/enforcement.yml`.
