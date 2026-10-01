# Changelog

## v0.1.0-abstract — 2026-10-01 (planned)
- Camera metrics with provenance for three clips of athlete P01 (1080×1920, 480×848, low-light control), exported from pipeline commit c48c714.
- Sensor session envelopes (aggregates; January and July sessions, n = 3 deliveries each).
- Pre-specified tolerances, verdict rule and gate thresholds (`data/thresholds.json`).
- `analysis/compare.py` reproduces Table 1 of the SSAC27 abstract; `analysis/figure1.py` regenerates Figure 1.
- Per-delivery sensor files held in `_pending_consent/` until the manufacturer's written consent is on file.
- Program A protocol (6–12 bowlers) pre-registered on OSF; `docs/PROGRAM_A_protocol.md` mirrors the registration.
