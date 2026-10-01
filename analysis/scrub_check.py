#!/usr/bin/env python3
"""Fails if anything under data/ or docs/ looks like an identifier that should not be public."""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATTERNS = {
    "file path": r"/Users/|/home/|C:\\\\",
    "url": r"https?://(?!creativecommons\.org|github\.com/jianshm|doi\.org|zenodo\.org|osf\.io)",
    "email": r"[\w.+-]+@[\w-]+\.[\w.]+",
    "original file name": r"IMG_\d{3,5}|\.MOV|\.mov|\.mp4",
    "uuid": r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
    "blob/sas token": r"blob\.core\.windows|sig=|sv=20",
    "real name other than the author": r"\b(Desai|Ahangama|Surendran|Kain|Yusuf|Kanchan)\b",
}
bad = 0
for base in ("data", "docs", "figures", "README.md", "CITATION.cff", "CHANGELOG.md"):
    p = os.path.join(ROOT, base)
    files = [p] if os.path.isfile(p) else [os.path.join(d, f) for d, _, fs in os.walk(p) for f in fs]
    for f in files:
        if f.endswith((".png", ".jpg")): continue
        t = open(f, encoding="utf-8", errors="ignore").read()
        for name, pat in PATTERNS.items():
            for m in re.finditer(pat, t):
                bad += 1; print(f"{os.path.relpath(f, ROOT)}: {name}: …{t[max(0,m.start()-30):m.end()+30]!r}")
print("scrub check:", "clean" if bad == 0 else f"{bad} hit(s)")
sys.exit(1 if bad else 0)
