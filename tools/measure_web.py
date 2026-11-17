"""Measure the QUORUM landing page's computed values from source.

    python3 -I tools/measure_web.py

This is a static computed-value witness, not a rendered screenshot. The gm
browser verb in this environment runs headful Chrome only and needs a desktop
session, so the page is recorded as unrendered in QUORUM-LOG.md. Values here
are computed from the source that ships, with no browser and no guessing.
"""
from __future__ import annotations

import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
WEB = ROOT / "web"
OUT = ROOT / "analysis" / "web-measurements.json"


def relative_luminance(rgb: tuple[int, int, int]) -> float:
    channels = []
    for value in rgb:
        c = value / 255.0
        channels.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    la, lb = relative_luminance(a), relative_luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return round((hi + 0.05) / (lo + 0.05), 3)


def hex_rgb(value: str) -> tuple[int, int, int]:
    return tuple(int(value[i:i + 2], 16) for i in (1, 3, 5))


def main() -> int:
    html = (WEB / "index.html").read_text(encoding="utf-8")
    css = (WEB / "style.css").read_text(encoding="utf-8")
    install_css = (WEB / "install.css").read_text(encoding="utf-8")
    css_all = css + install_css
    root = dict(re.findall(r"--([a-z-]+):\s*(#[0-9a-fA-F]{6})", css))
    paper = hex_rgb(root.get("paper", "#f4f1e8"))
    ink = hex_rgb(root.get("ink", "#10221d"))
    band = hex_rgb(root.get("band", "#0b1f1a"))
    muted = hex_rgb(root.get("muted", "#52524a"))
    result = {
        "method": "static source computation, no browser",
        "rendered": False,
        "render_note": "gm browser verb is headful-only and needs a desktop session in this environment",
        "html_bytes": len(html.encode("utf-8")),
        "css_bytes": len(css_all.encode("utf-8")),
        "figures_printed": len(re.findall(r'data-figure="', html)),
        "figure_keys": sorted(set(re.findall(r'data-figure="([a-z_]+)"', html))),
        "h1_count": len(re.findall(r"<h1\b", html)),
        "section_count": len(re.findall(r'<section\b', html)),
        "table_count": len(re.findall(r"<table\b", html)),
        "skip_link": 'class="skip"' in html,
        "lang_attribute": 'lang="en"' in html,
        "aria_live_status": 'aria-live="polite"' in html,
        "hero_alt_text": "aria-labelledby" in html and "<desc" in html,
        "reduced_motion_guard": "prefers-reduced-motion" in css_all,
        "min_interactive_target_px": min(
            int(x) for x in re.findall(r"min-height:\s*(\d+)px", css_all)
            if int(x) >= 44
        ) if re.findall(r"min-height:\s*(\d+)px", css_all) else None,
        "interactive_targets": sorted(set(re.findall(r"\.(copy|step-n|skip|wordmark)[,{ ]", css_all))),
        "contrast_paper_ink": contrast(paper, ink),
        "contrast_paper_muted": contrast(paper, muted),
        "contrast_band_paper": contrast(band, paper),
        "procedures": {
            "contrast": "WCAG relative luminance from the CSS custom properties",
            "figures": "count data-figure attributes in index.html",
            "targets": "minimum min-height declaration in the two stylesheets",
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in
                      ("rendered", "figures_printed", "contrast_paper_ink",
                       "contrast_paper_muted", "min_interactive_target_px", "reduced_motion_guard")},
                     sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
