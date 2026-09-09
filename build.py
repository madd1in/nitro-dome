#!/usr/bin/env python3
"""Wrap the artifact-format source into a standalone page for GitHub Pages.

`src/game.html` is the canonical source and is kept in Claude's artifact format:
no doctype, no <html>/<head>/<body> — the artifact host supplies those. GitHub
Pages does not, so this script adds them and nothing else. The game code itself
is copied through byte for byte.

    python build.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src" / "game.html"
OUT = ROOT / "index.html"

DESCRIPTION = (
    "Autoball in einer Neon-Kuppel: Boost, Flips, Wandfahren und Tore gegen "
    "KI-Gegner. Three.js mit eigener Physik, prozeduraler Musik und Bloom-Pipeline."
)
FAVICON = (
    "data:image/svg+xml,"
    "<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22>"
    "<text y=%22.92em%22 font-size=%2290%22>%F0%9F%9A%97</text></svg>"
)


def build() -> str:
    src = SRC.read_text(encoding="utf-8")
    # everything up to and including the stylesheet belongs in <head>
    marker = "</style>"
    cut = src.index(marker) + len(marker)
    head, body = src[:cut], src[cut:]

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="{DESCRIPTION}">
<meta name="theme-color" content="#05060c">
<meta name="color-scheme" content="dark">
<meta property="og:title" content="Nitro Dome">
<meta property="og:description" content="{DESCRIPTION}">
<meta property="og:type" content="website">
<link rel="icon" href="{FAVICON}">
{head}
</head>
<body>
{body.strip()}
</body>
</html>
"""


if __name__ == "__main__":
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size:,} bytes)")
