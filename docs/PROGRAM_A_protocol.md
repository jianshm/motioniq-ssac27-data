# Program A — paired camera–sensor capture protocol (pre-specified, October–November 2026)

Status: pre-specified before data collection and registered on OSF (osf.io/sxawp, registration DOI 10.17605/OSF.IO/SXAWP); this file mirrors the registration and is committed and tagged before the first capture session. Amendments are appended, dated, never edited in place.

## Design
- Bowlers: 6–12 pace bowlers (confirmatory sample; minimum 6; stop at 12 or on Nov 30 2026, whichever first) plus up to 6 spin bowlers as a separately analysed secondary stratum (never pooled into confirmatory verdicts; recruited alongside or after the pace minimum). Each bowler ≥ 12 deliveries; front-on and side-on cameras simultaneously.
- Secondary hypothesis H8 (all bowlers): at 30 fps with unattended release, camera error for at-release angles increases with the sensor-measured peak upper-arm angular rate, so spin bowlers show smaller release error than pace bowlers. Tested only with ≥ 3 spin and ≥ 6 pace bowlers.
- Camera: phone, 1080p or higher, **≥ 60 fps native** (no slow-motion re-timing), bowler ≥ 1/3 of frame height, side-on primary and front-on secondary, tripod, pitch length measured with a tape and recorded per session.
- Sensors: Vayu Equilibrium full-body set with wrist and head sensors fitted; timestamped exports with the **sampling rate stated by the manufacturer**; quaternions exported (not Euler only); a sync event (three-jump or clap) at the start of every over, visible to both cameras and the sensors.
- Release reference: the wrist-sensor (or Apple Watch) timestamp with the camera frame alongside, so release is adjudicated independently of the feature under test. Radar per delivery, gun position and axis recorded.

## Metrics (fixed)
Front-knee angle at front-foot contact (side-on: sagittal flexion; front-on: 2D frontal projection, reported separately) · elbow angle at release (side-on and front-on) · trunk lateral lean at release (front-on) and trunk forward lean (side-on) · front-foot-contact → release time · back-foot-contact → front-foot-contact time (only if a selector passes the adjudicated truth windows; otherwise reported withheld) · shoulder–hip separation (exploratory for both systems).

## Analysis (fixed before the first session)
- Per metric: mean absolute error, Bland–Altman bias with 95% limits of agreement (with confidence intervals), Pearson r with n, ICC(2,1); reported per bowler and pooled.
- Coverage–risk: for each metric, the fraction of deliveries on which the pipeline emits a value (coverage) and the fraction of emitted values beyond tolerance (risk), at the shipped gate thresholds and at two alternative thresholds either side.
- Tolerances: knee ±7°, other angles ±5°, timing ±25 ms (unchanged from the Phase-0 pre-specification). Three reporting bands: within tolerance / within 2× / beyond (not offered). Never relaxed after the fact.
- Event-definition offset: measured release offset between the sensor's peak upper-arm angular rate and the wrist-sensor timestamp, and between each and the adjudicated camera frame, reported before any "at release" comparison.
- Unattended vs assisted: every camera metric reported twice — as the shipped configuration emits it, and with the adjudicated release frame supplied.

## Not covered (stated so it cannot be claimed later)
Elbow flexion is compared only where a synced elbow reference exists at ≥ 60 fps; if none does, the elbow verdict remains the mechanism argument (angular rate × frame period), not a measured error.
