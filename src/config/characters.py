from __future__ import annotations

from typing import Dict, List

from .loader import load_character_meta
from .paths import CHARACTER_DIR
from .settings import DEFAULT_FONT

# Cache for expression file lists per character
_EXPRESSION_FILES_CACHE: Dict[str, List[str]] = {}


def get_expression_files(char_id: str) -> List[str]:
    """Return sorted list of PNG filenames (without extension) for the character, ordered lexicographically."""
    if char_id in _EXPRESSION_FILES_CACHE:
        return _EXPRESSION_FILES_CACHE[char_id]

    char_dir = CHARACTER_DIR / char_id
    files: List[str] = []
    if char_dir.is_dir():
        # Get all PNG files and sort lexicographically
        png_files = sorted([p.stem for p in char_dir.glob("*.png")])
        files = png_files

    _EXPRESSION_FILES_CACHE[char_id] = files
    return files


# Build characters dict dynamically: expression_files = list of filenames; font from YAML meta (optional)
_meta, _order_by_name = load_character_meta()

characters: Dict[str, dict] = {}
for cid, m in _meta.items():
    expr_files = get_expression_files(cid)
    font = m.get("font") or DEFAULT_FONT
    characters[cid] = {"expression_files": expr_files, "font": font}

# character list ordered by display name (as requested)
character_list: List[str] = [cid for cid in _order_by_name if cid in characters]

# Export meta too for other modules that need name/color
character_meta: Dict[str, dict] = _meta
