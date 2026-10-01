#!/usr/bin/env bash
# One-time setup of the PUBLIC data repository. Run from inside this folder. Never run inside the private MotionIQ repo.
set -euo pipefail
test ! -d .git || { echo "already a git repo"; exit 1; }
python3 analysis/compare.py >/dev/null && echo "compare.py: OK"
git init -b main
git add -A            # _pending_consent/ is ignored by .gitignore
git commit -m "v0.1.0-abstract: released data behind the SSAC27 abstract (camera metrics with provenance, sensor envelopes, thresholds, comparison script)"
git tag -a v0.1.0-abstract -m "Data release accompanying the SSAC27 Research Paper Competition abstract (Oct 1 2026)"
echo
echo "Next: create an EMPTY public repo on GitHub named motioniq-ssac27-data (no README), then:"
echo "  git remote add origin https://github.com/jianshm/motioniq-ssac27-data.git && git push -u origin main --tags"
echo "Then: GitHub → Releases → 'Draft a new release' from tag v0.1.0-abstract; enable Zenodo for the repo first so the release mints a DOI."
