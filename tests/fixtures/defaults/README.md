# Test defaults

The checks' tests run against these files, not against the project's own copies.
A project changes its roles, settings and constitution at bootstrap; those changes must
never break the template's tests (dry run 1, question Q11). Files the appliance owns and
projects do not edit (floor, artifact types, enforcement registry, templates) are read
from the repository itself. The checklist is generated from the floor at test time.
