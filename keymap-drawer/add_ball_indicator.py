#!/usr/bin/env python3
"""
Post-processes the keymap-drawer output SVG to add a small circle next to the
right thumb cluster on each layer, showing what the real trackball does while
that layer is held/active (move vs. scroll, and the speed gear).

Pure documentation touch-up: reads/rewrites keymap-drawer/charybdis.svg only,
after the keymap-drawer CI step has already generated it. Does not touch the
keymap, the physical layout, or anything that gets compiled onto the board.

The per-layer behavior below mirrors config/boards/shields/charybdis/charybdis_right.overlay
(the trackball_listener gearbox) - if that ever changes, update BALL_BY_LAYER too.
"""

import re
import sys
from pathlib import Path

SVG_PATH = Path(__file__).parent / "charybdis.svg"

# glyph: "*" = cursor movement, "^" (rendered as up/down arrows) = scroll
# speed: extra small label under the glyph, omitted when it's the 1x default
BALL_BY_LAYER = {
    "Base": {"glyph": "●", "speed": None},       # ● move, 1x (default)
    "NAV":  {"glyph": "↕", "speed": "1/3"},       # ↕ scroll, 1/3 speed
    "NUM":  {"glyph": "●", "speed": "1/2"},       # ● move, 1/2 speed (slow)
    "RSE":  {"glyph": "●", "speed": "3x"},        # ● move, 3x speed (fast)
    "MSE":  {"glyph": "●", "speed": None},        # ● move, 1x
    "FUN":  {"glyph": "●", "speed": None},        # ● move, 1x
    "BLT":  {"glyph": "●", "speed": None},        # ● move, 1x
    "GAME": {"glyph": "●", "speed": None},        # ● move, 1x
}

# local coordinates inside each layer's own key/combo group, to the right of
# the right thumb cluster (row 3, same y as the thumb keys) - well inside the
# canvas width already reserved by the wider rows above, so this can't expand
# the layer's bounding box or collide with anything.
BALL_X = 560
BALL_Y = 196
BALL_R = 14

LAYER_GROUP_RE = re.compile(
    r'(<g transform="translate\([\d.]+, [\d.]+\)" class="layer-(\w+)">.*?'
    r'<g transform="translate\(0, [\d.]+\)">)',
    re.DOTALL,
)


def ball_snippet(layer_name: str) -> str:
    spec = BALL_BY_LAYER.get(layer_name)
    if spec is None:
        return ""
    lines = [
        '<g class="ball-indicator">',
        f'<circle cx="{BALL_X}" cy="{BALL_Y}" r="{BALL_R}" '
        'fill="#1f3d7a" stroke="#60666c" stroke-width="1"/>',
    ]
    if spec["speed"]:
        lines.append(
            f'<text x="{BALL_X}" y="{BALL_Y - 3}" font-size="12" fill="#d1d6db" '
            'text-anchor="middle" dominant-baseline="middle">'
            f'{spec["glyph"]}</text>'
        )
        lines.append(
            f'<text x="{BALL_X}" y="{BALL_Y + 9}" font-size="9" fill="#d1d6db" '
            'text-anchor="middle" dominant-baseline="middle">'
            f'{spec["speed"]}</text>'
        )
    else:
        lines.append(
            f'<text x="{BALL_X}" y="{BALL_Y}" font-size="13" fill="#d1d6db" '
            'text-anchor="middle" dominant-baseline="middle">'
            f'{spec["glyph"]}</text>'
        )
    lines.append("</g>")
    return "".join(lines)


def main() -> int:
    svg = SVG_PATH.read_text(encoding="utf-8")

    if "ball-indicator" in svg:
        print("Ball indicators already present, skipping (already processed).")
        return 0

    def inject(match: re.Match) -> str:
        layer_name = match.group(2)
        return match.group(1) + ball_snippet(layer_name)

    new_svg, count = LAYER_GROUP_RE.subn(inject, svg)

    if count != len(BALL_BY_LAYER):
        print(
            f"Expected to patch {len(BALL_BY_LAYER)} layers, matched {count}. "
            "Layer names in the SVG may have changed - check BALL_BY_LAYER.",
            file=sys.stderr,
        )
        return 1

    SVG_PATH.write_text(new_svg, encoding="utf-8")
    print(f"Added ball indicators to {count} layers in {SVG_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
