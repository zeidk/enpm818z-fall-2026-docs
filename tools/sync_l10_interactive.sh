#!/usr/bin/env bash
# Copy the L10 interactive slides (built by make_interactive.py in the slides repo)
# into docs/source/_extra/lectures/lecture10/interactive/, which Sphinx serves as is.
# Replaces only that folder. Run from the docs repo root.
set -euo pipefail
SRC="${1:-../../latex/enpm818z-fall-2026-latex/slides/lectures/lecture10/interactive}"
DST="docs/source/_extra/lectures/lecture10/interactive"
for p in L10_interactive.html L10_interactive_assets L10_interactive_media katex; do
  [ -e "$SRC/$p" ] || { echo "missing: $SRC/$p" >&2; exit 1; }
done
rm -rf "$DST"
mkdir -p "$DST"
cp -r "$SRC/L10_interactive.html" "$SRC/L10_interactive_assets" "$SRC/L10_interactive_media" "$SRC/katex" "$DST/"
if grep -q -e 'ENPMnote' -e 'presenter' "$DST/L10_interactive.html"; then echo "warning: the page still mentions notes or the presenter" >&2; fi
du -sh "$DST"
