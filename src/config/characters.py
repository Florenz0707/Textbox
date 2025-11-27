from __future__ import annotations

import re
from typing import Dict, List

from .loader import load_character_meta
from .paths import CHARACTER_DIR

# Default font if not specified per character in YAML
DEFAULT_FONT = "font3.ttf"

# Cache for max index and available expressions per character
_MAX_INDEX_CACHE: Dict[str, int] = {}
_AVAIL_EXPR_CACHE: Dict[str, List[int]] = {}


def _scan_max_index(char_id: str) -> int:
    """Return the maximum numbered n for files named '<id> (n).png' (case-insensitive)."""
    if char_id in _MAX_INDEX_CACHE:
        return _MAX_INDEX_CACHE[char_id]
    max_n = 0
    char_dir = CHARACTER_DIR / char_id
    if char_dir.is_dir():
        pattern = re.compile(rf"^{re.escape(char_id)} \((\d+)\)\.png$", re.IGNORECASE)
        for p in char_dir.glob("*.png"):
            m = pattern.match(p.name)
            if m:
                try:
                    n = int(m.group(1))
                    if n > max_n:
                        max_n = n
                except Exception:
                    pass
    _MAX_INDEX_CACHE[char_id] = max_n
    return max_n


def get_available_expressions(char_id: str) -> List[int]:
    """Return sorted list of existing expression indices within 1..max_n for the character."""
    if char_id in _AVAIL_EXPR_CACHE:
        return _AVAIL_EXPR_CACHE[char_id]
    max_n = _scan_max_index(char_id)
    char_dir = CHARACTER_DIR / char_id
    avail: List[int] = []
    for n in range(1, max_n + 1):
        if (char_dir / f"{char_id} ({n}).png").is_file():
            avail.append(n)
    _AVAIL_EXPR_CACHE[char_id] = avail
    return avail


# Build characters dict dynamically: emotion_count = max index n; font from YAML meta (optional)
_meta, _order_by_name = load_character_meta()

characters: Dict[str, dict] = {}
for cid, m in _meta.items():
    max_n = _scan_max_index(cid)
    font = m.get("font") or DEFAULT_FONT
    characters[cid] = {"emotion_count": max_n, "font": font}

# character list ordered by display name (as requested)
character_list: List[str] = [cid for cid in _order_by_name if cid in characters]

# Export meta too for other modules that need name/color
character_meta: Dict[str, dict] = _meta
