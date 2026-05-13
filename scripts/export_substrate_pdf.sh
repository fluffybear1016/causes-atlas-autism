#!/usr/bin/env bash
#
# export_substrate_pdf.sh — produce print-grade PDFs of the substrate diagram.
#
# Per ChatGPT design feedback:
#   • 16:9 slide-native (1920×1080) is the canonical artifact
#   • 8.5×11 portrait is secondary (handoff/appendix)
#   • Vector-preserved, embedded fonts, no raster flattening
#   • Pure background retained; do not let export tooling compress black levels
#
# This script tries headless Chromium first (best fidelity).
# Falls back to manual browser-print instructions if Chromium not available.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SLIDE_HTML="$ROOT/ui/components/substrate_diagram_slide.html"
PAPER_HTML="$ROOT/ui/components/substrate_diagram.html"
OUT_DIR="$ROOT/exports"
mkdir -p "$OUT_DIR"

SLIDE_PDF="$OUT_DIR/substrate_diagram_slide_16x9.pdf"
PAPER_PDF="$OUT_DIR/substrate_diagram_paper_8x11.pdf"

# Find a Chromium-class binary
CHROME=""
for candidate in \
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  "/Applications/Chromium.app/Contents/MacOS/Chromium" \
  "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" \
  "$(command -v chromium-browser 2>/dev/null || true)" \
  "$(command -v google-chrome 2>/dev/null || true)" \
  "$(command -v chromium 2>/dev/null || true)" \
; do
  if [[ -n "$candidate" && -e "$candidate" ]]; then
    CHROME="$candidate"
    break
  fi
done

print_manual_instructions() {
  cat <<EOF

  ⚠ No Chromium-class browser auto-detected for headless export.

  Manual export (browser print-to-PDF preserves vectors):

  1) PRIMARY (canonical, 16:9 slide-native):
       open "$SLIDE_HTML"
       In browser: Cmd+P (Mac) / Ctrl+P (Linux/Win)
       Destination: "Save as PDF"
       Layout: Landscape
       Paper size: choose "1920×1080" if available, else "Letter Landscape"
       Margins: None
       Background graphics: ON
       Save to: $SLIDE_PDF

  2) SECONDARY (handoff, 8.5×11 portrait):
       open "$PAPER_HTML"
       Cmd+P → Save as PDF
       Layout: Portrait, US Letter, Margins: Default, Background: ON
       Save to: $PAPER_PDF

  Reload-and-redo if any of these regressed:
    - Background not pure (export tooling lightened black levels)
    - Margins tightened (lost negative space)
    - Fonts substituted (Inter not embedded)

EOF
}

if [[ -z "$CHROME" ]]; then
  print_manual_instructions
  exit 0
fi

echo "Using browser: $CHROME"

# Primary: 16:9 slide-native, 1920×1080
"$CHROME" \
  --headless=new \
  --disable-gpu \
  --no-margins \
  --no-pdf-header-footer \
  --print-to-pdf-no-header \
  --hide-scrollbars \
  --virtual-time-budget=2000 \
  --window-size=1920,1080 \
  --print-to-pdf="$SLIDE_PDF" \
  "file://$SLIDE_HTML" 2>/dev/null

if [[ -f "$SLIDE_PDF" ]]; then
  size=$(stat -f%z "$SLIDE_PDF" 2>/dev/null || stat -c%s "$SLIDE_PDF")
  echo "✓ wrote $SLIDE_PDF ($size bytes, 16:9 slide-native)"
else
  echo "✗ slide-native export failed"
fi

# Secondary: 8.5×11 portrait
"$CHROME" \
  --headless=new \
  --disable-gpu \
  --no-margins \
  --no-pdf-header-footer \
  --print-to-pdf-no-header \
  --hide-scrollbars \
  --virtual-time-budget=2000 \
  --print-to-pdf="$PAPER_PDF" \
  "file://$PAPER_HTML" 2>/dev/null

if [[ -f "$PAPER_PDF" ]]; then
  size=$(stat -f%z "$PAPER_PDF" 2>/dev/null || stat -c%s "$PAPER_PDF")
  echo "✓ wrote $PAPER_PDF ($size bytes, 8.5×11 portrait)"
fi

echo
echo "Verification:"
echo "  • Open the PDFs. Confirm: vector geometry zooms cleanly, fonts are Inter/IBM Plex,"
echo "    backgrounds are pure (slide=#08090b, paper=#fbfaf6), L3 has visible breathing room,"
echo "    L6 has exactly 5 institutional names."
echo "  • If any regressed, re-export via browser Print→Save as PDF (preserves vectors better"
echo "    than headless Chromium in some Chromium builds)."
