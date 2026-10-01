# motioniq-ssac27-data

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23073507.svg)](https://doi.org/10.5281/zenodo.23073507) · Pre-registration: [osf.io/sxawp](https://osf.io/sxawp)

Released data behind **"When Should a Phone Refuse to Measure? Confidence-Gated Single-Camera Biomechanics for Cricket Pace Bowling"** — an abstract submitted to the MIT Sloan Sports Analytics Conference 2027 Research Paper Competition (sole author: Jiansh Maker; October 1, 2026). Every number in the abstract's Table 1 and Figure 1 can be recomputed from the files here with two short scripts. The measurement pipeline itself (pose estimation, event detection, confidence gating, provenance) is not part of this release; the competition requires the data, and encourages but does not require the model code.

## What is here

| Path | Contents | Licence |
|---|---|---|
| `data/camera/*_metrics_with_provenance.json` | Three clips of one bowler (athlete **P01**, the author): 1080×1920 and 480×848 front-on phone clips at 30 fps, and a low-light capture-failure control. Each metric carries its confidence, the frame and landmark stream it was computed from, and the landmark pixel coordinates behind it; withheld metrics carry the reason. The per-frame 2D landmark streams (pixel coordinates only; no images) are included so any angle can be recomputed. Exported from pipeline commit `c48c714` (the pose service is unchanged through `ddb8b1c`). | CC BY 4.0 |
| `data/camera/table1_expected.csv` | The comparison table the abstract's Table 1 is drawn from (camera value, confidence, sensor envelope, delta and verdict against both sensor sessions). | CC BY 4.0 |
| `data/sensor/envelopes.csv` | Reference envelopes from a Vayu Equilibrium full-body IMU system worn by the same athlete: mean, SD, min, max and n for every derived metric, per session (January, July; n = 3 deliveries each). Sampling rate inferred ≈ 100 Hz (not manufacturer-confirmed); every millisecond value depends on it. | CC BY 4.0 (with attribution to the manufacturer) |
| `data/thresholds.json` | The pre-specified tolerances (knee ±7°, other angles ±5°, timing ±25 ms), the verdict rule, the "discriminates" rule and the gate thresholds fixed in code (landmark visibility 0.35, pose detection 0.5, release visibility 0.5, bowler height 0.25 × frame, Reliable tier 0.7). | CC BY 4.0 |
| `analysis/compare.py` | Recomputes every delta and verdict from the files above and checks them against `table1_expected.csv`. Exit code 0 means Table 1 reproduces. | MIT |
| `analysis/figure1.py` | Regenerates Figure 1 (`figures/Figure1.png`). | MIT |
| `analysis/scrub_check.py` | Fails if anything identifying has crept into the release. | MIT |
| `docs/PROGRAM_A_protocol.md` | The pre-registered paired camera–sensor study of 6–12 bowlers (October–November 2026; OSF osf.io/sxawp) whose results the full paper will report. Committed before the first capture. | CC BY 4.0 |
| `docs/RELEASE_CHECKLIST.md` | Consent, anonymisation and reproducibility checks run before every push. | — |

Per-delivery sensor files (peak upper-arm angular rate, the ±3-sample ranges, per-delivery events) are held back in `_pending_consent/` (git-ignored) until the manufacturer's written consent is on file, at which point they move to `data/sensor/per_delivery_release_metrics.csv` and `analysis/figure1.py` reads them directly. Until then Figure 1 is drawn from the six values quoted in the abstract, embedded in the script.

## Reproduce

```bash
python3 analysis/compare.py      # prints both clips against both sensor sessions; exit 0 = Table 1 reproduces
python3 analysis/figure1.py      # writes figures/Figure1.png   (needs numpy, matplotlib)
```

## How to read the comparison

The camera clips and the sensor sessions were **not recorded at the same time** (unpaired, up to thirteen months apart), so each sensor session is a same-athlete reference envelope, not ground truth. The comparison screens plausibility; it is not concurrent validity and nothing here is a validation of the camera against the sensors. A test "discriminates" only when the envelope's SD (from n = 3 deliveries, itself imprecise) is narrower than the tolerance; among the five pre-specified metrics only the front-knee angle meets that against the January session, and verdicts are envelope-dependent (see the July columns). Both clips were analysed with a hand-picked release frame; run unattended, the pipeline finds no release frame on the 1080p clip and publishes no elbow. Back-foot contact is withheld on every clip because no selector reproduced frame-adjudicated contact.

## Anonymisation and consent

The only athlete in this release is the author (P01), a minor, with parental consent. No video, frame or image of any person is included; landmark streams are pixel coordinates. Sensor data are derived metrics, released with the manufacturer's consent as recorded in `docs/RELEASE_CHECKLIST.md`. Clips of other bowlers used in the pipeline's regression harness are not part of this release; where the abstract cites them ("8 of 18 corpus clips"), it cites counts only.

## Versions

`v0.1.0-abstract` (Oct 1 2026) → `v1.0.0-paper` (Dec 4 2026, adds the Program A paired data) → `v1.1.0-camera-ready` (Feb 2027). Each GitHub release mints a Zenodo DOI; cite the DOI of the version you used (`CITATION.cff`).

## Contact

Jiansh Maker — via the repository's issues. Mentor: Jeetu Maker (mentored on architecture; built nothing; no analysis value comes from him).
