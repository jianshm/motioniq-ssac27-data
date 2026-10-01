"""Figure 1 of the SSAC27 abstract — 'What one 30 fps frame hides'.
Reads the per-delivery sensor file when it has been released (data/sensor/per_delivery_release_metrics.csv,
consent-gated — see docs/RELEASE_CHECKLIST.md); until then the six peak angular rates and the ±3-sample ranges are
the values quoted in the abstract, embedded below. Single hue, print-safe, one series per panel (no legend).
Run: python3 analysis/figure1.py  → figures/Figure1.png"""
import os, csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# --- data (verbatim from the sensor files) ---
trials = ["01272", "01274", "01275", "07201", "07202", "07203"]
rate = np.array([2109.6, 2635.1, 2019.8, 2086.4, 2157.1, 1862.7])          # peak upper-arm angular rate, deg/s
elbow_pm3 = np.array([2.12, 6.23, 15.50, 14.42, 20.66, 13.69])              # elbow flexion range within ±3 samples of release, deg
trunk_pm3 = np.array([37.04, 33.14, 37.86])                                 # trunk frontal range within ±3 samples, July trials only
fps = [30, 60, 240]
_pd = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "sensor", "per_delivery_release_metrics.csv")
if os.path.exists(_pd):  # columns: delivery, peak_upper_arm_rate_deg_s, elbow_range_pm3_deg, trunk_range_pm3_deg (blank if not computed)
    _rows = list(csv.DictReader(open(_pd)))
    rate = np.array([float(r["peak_upper_arm_rate_deg_s"]) for r in _rows])
    elbow_pm3 = np.array([float(r["elbow_range_pm3_deg"]) for r in _rows if r["elbow_range_pm3_deg"]])
    trunk_pm3 = np.array([float(r["trunk_range_pm3_deg"]) for r in _rows if r["trunk_range_pm3_deg"]])
    print("per-delivery sensor file found; plotting released values")
tol = 5.0

INK = "#1f2933"; INK2 = "#52606d"; MUTED = "#9aa5b1"; GRID = "#e4e7eb"; BAND = "#f0f1f3"; SURF = "#ffffff"
MARK = "#2f5f8f"   # single hue for marks; text never wears it

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "axes.edgecolor": GRID,
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.titlecolor": INK, "axes.spines.top": False, "axes.spines.right": False})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 3.0), dpi=300, gridspec_kw={"width_ratios": [1.15, 1], "wspace": 0.42})
fig.patch.set_facecolor(SURF)

rng = np.random.default_rng(3)

# ---------- left: rotation per frame at 30/60/240 fps ----------
ax = ax1
ax.set_facecolor(SURF)
ax.axhspan(0, tol, color=BAND, zorder=0)
ax.axhline(tol, color=MUTED, lw=1, ls=(0, (3, 2)), zorder=1)
ax.text(-0.5, tol + 1.2, "±5° tolerance", color=INK2, fontsize=7, ha="left", va="bottom")
for i, f in enumerate(fps):
    per_frame = rate / f
    x = i + rng.uniform(-0.13, 0.13, size=len(per_frame))
    ax.scatter(x, per_frame, s=42, color=MARK, edgecolor=SURF, linewidth=1.2, zorder=3)
    lo, hi = per_frame.min(), per_frame.max()
    ax.plot([i - 0.28, i + 0.28], [lo, lo], color=MARK, lw=0.8, alpha=0.5, zorder=2)
    ax.plot([i - 0.28, i + 0.28], [hi, hi], color=MARK, lw=0.8, alpha=0.5, zorder=2)
    ax.text(i + 0.33, hi, f"{lo:.0f}–{hi:.0f}°", color=INK, fontsize=7.5, va="center", ha="left")
ax.set_xticks(range(3)); ax.set_xticklabels([f"{f} fps" for f in fps])
ax.set_xlim(-0.55, 2.75)
ax.set_ylim(0, 95)
ax.set_yticks([0, 20, 40, 60, 80])
ax.set_ylabel("Arm rotation per video frame (°)")
ax.set_title("Arm rotation inside one video frame", loc="left", fontsize=9, pad=9)
ax.text(0, 1.005, "peak upper-arm rate 1,863–2,635 °/s (six deliveries) ÷ frame period", transform=ax.transAxes,
        color=INK2, fontsize=7, va="bottom")
ax.yaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
ax.tick_params(length=0)

# ---------- right: angle change within ±3 samples of release ----------
ax = ax2
ax.set_facecolor(SURF)
ax.axhspan(0, tol, color=BAND, zorder=0)
ax.axhline(tol, color=MUTED, lw=1, ls=(0, (3, 2)), zorder=1)
ax.text(1.9, tol + 0.8, "±5° tolerance", color=INK2, fontsize=7, ha="right", va="bottom")
groups = [("Elbow flexion\n(n = 6)", elbow_pm3), ("Trunk lateral lean\n(July, n = 3)", trunk_pm3)]
for i, (lab, vals) in enumerate(groups):
    x = i + rng.uniform(-0.12, 0.12, size=len(vals))
    ax.scatter(x, vals, s=42, color=MARK, edgecolor=SURF, linewidth=1.2, zorder=3)
    lo, hi = vals.min(), vals.max()
    ax.plot([i - 0.25, i + 0.25], [lo, lo], color=MARK, lw=0.8, alpha=0.5, zorder=2)
    ax.plot([i - 0.25, i + 0.25], [hi, hi], color=MARK, lw=0.8, alpha=0.5, zorder=2)
    n_ex = int((vals > tol).sum())
    ax.text(i + 0.3, hi, f"{lo:.0f}–{hi:.0f}°\n{n_ex} of {len(vals)} exceed", color=INK, fontsize=7.5, va="center", ha="left")
ax.set_xticks([0, 1]); ax.set_xticklabels([g[0] for g in groups])
ax.set_xlim(-0.5, 1.95)
ax.set_ylim(0, 42)
ax.set_yticks([0, 10, 20, 30, 40])
ax.set_ylabel("Range across ±3 samples of release (°)")
ax.set_title("Angle range across ±3 samples", loc="left", fontsize=9, pad=9)
ax.text(0, 1.005, "rel−3 … rel+3: ≈60 ms total at inferred 100 Hz", transform=ax.transAxes,
        color=INK2, fontsize=7, va="bottom")
ax.yaxis.grid(True, color=GRID, lw=0.8); ax.set_axisbelow(True)
ax.tick_params(length=0)

fig.subplots_adjust(left=0.085, right=0.985, top=0.84, bottom=0.17)
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures", "Figure1.png")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
fig.savefig(OUT, dpi=300, facecolor=SURF)
print("saved")
