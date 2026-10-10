#!/usr/bin/env python3
"""Check that the figures used by the docs read on both themes.

The site has a light theme (sand) and a dark theme. A figure drawn on a
transparent background shows the page color through it, so black lines
vanish on the dark theme. Every figure must therefore have an opaque
background; diagrams should have a white one.

For each image a page uses (``.. figure::`` and ``.. image::`` under
docs/source), the script reports:

  FAIL   the image has transparent pixels (alpha below 255).
  CHECK  opaque, but its border is not white. Fine for a photo or a
         screenshot; a diagram should be re-exported on white.
  ok     opaque, with a white border.

Usage (from the repo root):
  /usr/bin/python3 tools/check_figures.py                 # every page
  /usr/bin/python3 tools/check_figures.py lectures/lecture3   # one folder or file
  /usr/bin/python3 tools/check_figures.py --all            # list ok files too

Exit status is 1 if any image FAILs or is missing, else 0.
"""
import re
import sys
from pathlib import Path

from PIL import Image, ImageSequence

SOURCE = Path(__file__).resolve().parent.parent / "docs" / "source"
DIRECTIVE = re.compile(r"^\s*\.\. (?:figure|image)::\s+(\S+)", re.M)
WHITE = 245          # a channel at or above this counts as white
WHITE_SHARE = 0.95   # share of border pixels that must be white


def images_used(scope):
    """Map each image path to the .rst files that use it."""
    used = {}
    for rst in sorted(scope.rglob("*.rst") if scope.is_dir() else [scope]):
        for ref in DIRECTIVE.findall(rst.read_text(encoding="utf-8")):
            if ref.startswith(("http://", "https://")):
                continue
            path = SOURCE / ref.lstrip("/") if ref.startswith("/") else rst.parent / ref
            used.setdefault(path.resolve(), []).append(rst.relative_to(SOURCE))
    return used


def check(path):
    """Return (status, detail) for one image file."""
    with Image.open(path) as im:
        frames = [f.convert("RGBA") for f in ImageSequence.Iterator(im)]
    transparent = sum(sum(1 for a in f.getchannel("A").getdata() if a < 255) for f in frames)
    if transparent:
        return "FAIL", f"{transparent} transparent pixels"
    f = frames[0].convert("RGB")
    w, h = f.size
    border = [f.getpixel((x, y)) for x in range(w) for y in (0, 1, h - 2, h - 1)]
    border += [f.getpixel((x, y)) for y in range(h) for x in (0, 1, w - 2, w - 1)]
    share = sum(1 for p in border if min(p) >= WHITE) / len(border)
    if share < WHITE_SHARE:
        return "CHECK", f"border {share:.0%} white (photo or screenshot?)"
    return "ok", f"border {share:.0%} white"


def main(argv):
    show_all = "--all" in argv
    args = [a for a in argv if a != "--all"]
    scope = (SOURCE / args[0]).resolve() if args else SOURCE
    used = images_used(scope)
    counts = {"ok": 0, "CHECK": 0, "FAIL": 0, "MISSING": 0}
    for path in sorted(used):
        if not path.exists():
            status, detail = "MISSING", "file not found"
        else:
            status, detail = check(path)
        counts[status] += 1
        if status != "ok" or show_all:
            pages = ", ".join(str(p) for p in used[path][:2])
            print(f"{status:7s} {path.relative_to(SOURCE)}  ({detail}; used in {pages})")
    print(f"\n{len(used)} images: " + ", ".join(f"{n} {k}" for k, n in counts.items()))
    return 1 if counts["FAIL"] or counts["MISSING"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
