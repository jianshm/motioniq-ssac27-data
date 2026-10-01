# Release checklist — run before every `git push` to the public repository

Nothing here is optional. The private MotionIQ repository is never a remote of this one.

## Consent and rights
- [ ] Athlete P01 (the author, a minor): parental consent for the camera clips and the sensor sessions is on file. Date: ____
- [ ] Vayu Technology Corp: **written** consent to publish sensor-derived per-delivery files (`_pending_consent/sensor_per_delivery/`). Until it is on file those files stay in `_pending_consent/` (git-ignored) and only `data/sensor/envelopes.csv` (aggregates already disclosed in the signed LOI exhibit) is public. Date / email reference: ____
- [ ] Any clip from another bowler (academy footage or the individually named player): written permission from the player (and guardian if under 18) **and** the academy. Harness clips from the Australian program stay out until the Oct 15 mapping and Oct 31 written confirmation are complete. Otherwise counts only, never per-clip files.
- [ ] Patent counsel has confirmed that nothing in this release discloses the gating mechanism beyond what the provisional (App. 64/137,064, filed Aug 19 2026) already covers. Rule of thumb: numbers, thresholds and outputs of the gates are fine; the decision logic, selectors and code are not.

## Anonymisation (automated in `analysis/scrub_check.py`, run it)
- [ ] No video, frame, thumbnail, contact sheet or image of a person anywhere in the tree (`.gitignore` blocks the common extensions — check anyway).
- [ ] No file paths, user IDs, analysis UUIDs, blob URLs, e-mail addresses, device names or the phone's original file names inside any JSON/CSV/MD.
- [ ] Athlete referred to as P01; no date of birth; session labels are "January"/"July" with the year stated only where verified.
- [ ] Per-frame landmark streams are pixel coordinates only (no image), rounded to ≤ 4 dp.

## Reproducibility
- [ ] `python3 analysis/compare.py` exits 0 (every Table 1 delta and verdict reproduces from the released numbers).
- [ ] `python3 analysis/figure1.py` regenerates `figures/Figure1.png` byte-for-byte or with only rendering differences.
- [ ] `data/thresholds.json` is unchanged since it was pre-specified (its `pre_specified_on` date and the commit that introduced it are the record).
- [ ] README states the pipeline commit the metrics were exported from (`c48c714`; pose service unchanged through `ddb8b1c`).

## Versioning
- [ ] Tag: `v0.1.0-abstract` (Oct 1 2026) · `v1.0.0-paper` (Dec 4 2026, with Program A) · `v1.1.0-camera-ready` (Feb 2027).
- [ ] GitHub release created for each tag; Zenodo integration switched on so each release mints a DOI; DOI pasted into CITATION.cff and the paper.
- [ ] CHANGELOG.md entry names what was added and what consent it rests on.
