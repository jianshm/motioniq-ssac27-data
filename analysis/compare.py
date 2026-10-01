#!/usr/bin/env python3
"""Recompute Table 1 of the SSAC27 abstract from the released data, and check it against
data/camera/table1_expected.csv.

Inputs (all in this repository):
  data/camera/*_metrics_with_provenance.json   camera metrics with per-metric provenance (frame, stream, landmarks)
  data/sensor/envelopes.csv                    sensor session envelopes (mean, SD, min, max; n = 3 deliveries per session)
  data/thresholds.json                         pre-specified tolerances, verdict rule, gates

Run:  python3 analysis/compare.py        (exit code 0 = every 1080p-clip delta and verdict reproduces)

No pipeline code is needed: the comparison is arithmetic on released numbers. Deltas are computed from
unrounded values (camera value minus session mean), exactly as the abstract's Table 1 states.
"""
import csv, json, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
thr = json.load(open(f"{ROOT}/data/thresholds.json"))
TOL = {"knee": thr["tolerances"]["front_knee_flexion_at_ffc_deg"],
       "angle": thr["tolerances"]["other_angles_deg"],
       "timing": thr["tolerances"]["timing_ms"],
       "separation": thr["tolerances"]["shoulder_hip_separation_deg"]["value"]}

def verdict(d, tol):
    if d is None: return "WITHHELD"
    return "CLOSE" if abs(d) <= tol else "MODERATE" if abs(d) <= 2 * tol else "OFF"

# sensor envelopes
env = {}
for r in csv.DictReader(open(f"{ROOT}/data/sensor/envelopes.csv")):
    env[(r["metric"], r["session_label"])] = {k: float(r[k]) for k in ("mean", "sd", "min", "max")} | {"n": int(r["n"])}

# camera metrics → the five pre-specified rows (+ the two exploratory rows), per clip
SPEC = [  # (table label, section, metric name, transform, sensor row, tolerance key)
    ("Front knee flexion at FFC", "atFfcMetrics", "Front knee flexion at FFC", lambda v: 180 - v, "Front knee flexion @FFC (°)", "knee"),
    ("Bowling elbow angle at release", "atReleaseMetrics", "Bowling elbow angle", lambda v: 180 - v, "Bowling elbow flexion @REL (°)", "angle"),
    ("Trunk lateral lean at release (vs. absolute trunk angle)", "atReleaseMetrics", "Trunk lateral lean at release", lambda v: v, "Trunk frontal (abs) @REL (°)", "angle"),
    ("Trunk lateral lean at release (vs. pelvis-relative)", "atReleaseMetrics", "Thorax–pelvis lateral flexion at release", lambda v: v, "Spine lateral flexion @REL (°) [trunk rel. pelvis]", "angle"),
    ("Shoulder–hip separation at release (|EQ|)", "atReleaseMetrics", "Shoulder–hip separation", lambda v: v, "Shoulder–hip separation @REL (°) |abs|", "separation"),
]

def camera_rows(clip):
    a = json.load(open(f"{ROOT}/data/camera/{clip}_metrics_with_provenance.json"))
    rows = []
    for label, sec, name, f, srow, tk in SPEC:
        m = next((x for x in a.get(sec, []) if x["name"] == name), None)
        val = f(m["value"]) if m else None
        conf = m["confidence"] if m else None
        rows.append((label, val, conf, srow, TOL[tk]))
    ph = a["phases"]; fps = a["fps"]
    bfc = ph.get("backFootContactFrame"); ffc = ph.get("frontFootContactFrame"); rel = ph.get("releaseFrame")
    rows.append(("BFC→FFC time (ms)", None if bfc is None or ffc is None else (ffc - bfc) / fps * 1000, None, "BFC→FFC (ms)", TOL["timing"]))
    rows.append(("FFC→release time (ms)", None if ffc is None or rel is None else (rel - ffc) / fps * 1000, None, "FFC→REL (ms)", TOL["timing"]))
    return rows, a

expected = {(r["clip"], r["metric"]): r for r in csv.DictReader(open(f"{ROOT}/data/camera/table1_expected.csv"))}

def sep_abs(srow, sess):
    # separation is compared as |EQ| (magnitude): envelopes.csv carries a "|abs|" row for it
    return env[(srow, sess)]

fails = 0
for clip in ("clipB_1080x1920", "clipA_480x848", "lowlight_control"):
    rows, a = camera_rows(clip)
    print(f"\n== {clip}  (detection {a['poseDetectionRate']}, fps {a['fps']}, release frame {a['phases'].get('releaseFrame')}, "
          f"FFC {a['phases'].get('frontFootContactFrame')}, BFC {a['phases'].get('backFootContactFrame')})")
    print(f"{'metric':58s} {'camera':>9s} {'conf':>5s} | {'Jan mean±SD':>14s} {'Δ':>7s} {'verdict':9s} | {'Jul mean±SD':>14s} {'Δ':>7s} {'verdict':9s}")
    for label, val, conf, srow, tol in rows:
        out = f"{label:58s} {('—' if val is None else f'{val:9.3f}'):>9s} {('' if conf is None else f'{conf:.2f}'):>5s}"
        for sess in ("January", "July"):
            e = env.get((srow, sess))
            if e is None:
                out += f" | {'n/a':>14s} {'':>7s} {'':9s}"; continue
            d = None if val is None else val - e["mean"]
            v = verdict(d, tol)
            out += f" | {e['mean']:6.2f} ± {e['sd']:5.2f} {('—' if d is None else f'{d:+7.2f}'):>7s} {v:9s}"
            exp = expected.get((clip, label))
            if exp and clip == "clipB_1080x1920":  # the abstract's Table 1 clip: enforce exact reproduction
                key = "delta_jan" if sess == "January" else "delta_jul"; vkey = "verdict_jan" if sess == "January" else "verdict_jul"
                ed = exp[key]
                ok = (v == exp[vkey]) and (d is None and ed == "" or (d is not None and ed != "" and abs(d - float(ed)) < (0.1 if "time" in label else 0.005)))
                if not ok:
                    fails += 1; out += "  <-- MISMATCH vs table1_expected.csv"
        print(out)
    if clip == "clipA_480x848":
        print("   note: this JSON export used release frame 50; table1_expected.csv rows for clip A come from the "
              "re-run with release frame 51 (the release-frame sensitivity the abstract describes). The abstract quotes "
              "no clip-A value beyond 'one of five within tolerance', which holds under both picks (against July).")
    if clip == "lowlight_control":
        print("   every metric withheld:", [n.split(':')[0] for n in a["notes"] if "not shown" in n])

print("\nRESULT:", "all 1080p-clip deltas and verdicts reproduce" if fails == 0 else f"{fails} mismatch(es)")
sys.exit(0 if fails == 0 else 1)
