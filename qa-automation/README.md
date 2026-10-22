# Tool Calling author-package checks

Run `python -m pip install -r qa-automation/workspace-auth-requirements.txt`, then `python -m pytest qa-automation/tests -q` with Python 3.11. Tests execute the actual embedded learner checks against synthetic replies; they make no model calls.

See [the dated review receipt](../publishing-house/reviews/learner-validation-2026-10-22.md) for the live acceptance boundary and owner actions. The learner guide is the live replay procedure. Never record credentials in evidence or mark PH tasks complete from an offline pass.
