from __future__ import annotations
from typing import Dict, List

# Dynamic text decoration builder based on character meta (name/color)
# Keeps existing positions/font_size templates per role; falls back to a default layout.

from .characters import character_meta

WHITE = (255, 255, 255)

# Base templates: only position + font_size; colors and texts will be filled dynamically
POS_TEMPLATES: Dict[str, List[Dict]] = {
    "nanoka": [
        {"position": (759, 63), "font_size": 196},
        {"position": (955, 175), "font_size": 92},
        {"position": (1053, 117), "font_size": 147},
        {"position": (1197, 175), "font_size": 92},
    ],
    "hiro": [
        {"position": (759, 63), "font_size": 196},
        {"position": (955, 175), "font_size": 92},
        {"position": (1143, 110), "font_size": 147},
        {"position": (1283, 175), "font_size": 92},
    ],
    "ema": [
        {"position": (759, 73), "font_size": 186},
        {"position": (949, 175), "font_size": 92},
        {"position": (1039, 117), "font_size": 147},
        {"position": (1183, 175), "font_size": 92},
    ],
    "sherri": [
        {"position": (759, 73), "font_size": 186},
        {"position": (943, 110), "font_size": 147},
        {"position": (1093, 175), "font_size": 92},
        {"position": (0, 0), "font_size": 1},
    ],
    "anan": [
        {"position": (759, 73), "font_size": 186},
        {"position": (949, 175), "font_size": 92},
        {"position": (1039, 117), "font_size": 147},
        {"position": (1183, 175), "font_size": 92},
    ],
    "noa": [
        {"position": (759, 73), "font_size": 186},
        {"position": (945, 175), "font_size": 92},
        {"position": (1042, 117), "font_size": 147},
        {"position": (1186, 175), "font_size": 92},
    ],
    "coco": [
        {"position": (759, 73), "font_size": 186},
        {"position": (945, 175), "font_size": 92},
        {"position": (1042, 117), "font_size": 147},
        {"position": (1186, 175), "font_size": 92},
    ],
    "alisa": [
        {"position": (759, 73), "font_size": 186},
        {"position": (945, 175), "font_size": 92},
        {"position": (1042, 117), "font_size": 147},
        {"position": (1186, 175), "font_size": 92},
    ],
    "reia": [
        {"position": (759, 73), "font_size": 186},
        {"position": (945, 175), "font_size": 92},
        {"position": (1042, 117), "font_size": 147},
        {"position": (1186, 175), "font_size": 92},
    ],
    "mago": [
        {"position": (759, 73), "font_size": 186},
        {"position": (945, 175), "font_size": 92},
        {"position": (1042, 117), "font_size": 147},
        {"position": (1186, 175), "font_size": 92},
    ],
    "hanna": [
        {"position": (759, 73), "font_size": 186},
        {"position": (945, 175), "font_size": 92},
        {"position": (1042, 117), "font_size": 147},
        {"position": (1186, 175), "font_size": 92},
    ],
    "meruru": [
        {"position": (759, 73), "font_size": 186},
        {"position": (945, 175), "font_size": 92},
        {"position": (1042, 117), "font_size": 147},
        {"position": (1186, 175), "font_size": 92},
    ],
    "miria": [
        {"position": (759, 73), "font_size": 186},
        {"position": (945, 175), "font_size": 92},
        {"position": (1042, 117), "font_size": 147},
        {"position": (1186, 175), "font_size": 92},
    ],
    "yuki": [
        {"position": (759, 63), "font_size": 196},
        {"position": (948, 175), "font_size": 92},
        {"position": (1053, 117), "font_size": 147},
        {"position": (0, 0), "font_size": 1},
    ],
    "momoi": [
        {"position": (759, 73), "font_size": 186},
        {"position": (945, 175), "font_size": 92},
        {"position": (1042, 117), "font_size": 147},
        {"position": (1186, 175), "font_size": 92},
    ],
}

# Fallback template if a role has no predefined positions
FALLBACK_TEMPLATE: List[Dict] = [
    {"position": (759, 73), "font_size": 186},
    {"position": (945, 175), "font_size": 92},
    {"position": (1042, 117), "font_size": 147},
    {"position": (1186, 175), "font_size": 92},
]


def _segments_from_name(name: str) -> List[str]:
    if not name:
        return ["", "", "", ""]
    chars = list(name)
    s1 = chars[0] if len(chars) >= 1 else ""
    s2 = chars[1] if len(chars) >= 2 else ""
    s3 = chars[2] if len(chars) >= 3 else ""
    s4 = "".join(chars[3:]) if len(chars) >= 4 else ""
    return [s1, s2, s3, s4]


# Build text configs dict dynamically
text_configs_dict: Dict[str, List[Dict]] = {}

for cid, meta in character_meta.items():
    name = meta.get("name") or cid
    color = tuple(meta.get("color") or WHITE)
    segments = _segments_from_name(name)
    template = POS_TEMPLATES.get(cid, FALLBACK_TEMPLATE)

    configs: List[Dict] = []
    for idx, tpl in enumerate(template):
        seg_text = segments[idx] if idx < len(segments) else ""
        seg_color = color if idx == 0 else WHITE
        configs.append({
            "text": seg_text,
            "position": tpl["position"],
            "font_color": seg_color,
            "font_size": tpl["font_size"],
        })
    text_configs_dict[cid] = configs
