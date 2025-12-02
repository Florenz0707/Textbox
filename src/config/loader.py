from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Tuple

import yaml

from .paths import CONFIG_DIR


def _read_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Invalid YAML structure in {path}")
    return data


def load_character_meta() -> Tuple[Dict[str, Dict[str, Any]], list[str]]:
    """
    Load character metadata from config/character.yaml (new schema).

    Expected schema (preferred):
    character:
      <id>:
        name: "中文名"
        color: [R, G, B]
        font: font3.ttf   # optional

    Fallbacks for backward compatibility are supported but discouraged.

    Returns:
      meta: { id: { name: str, color: (R,G,B), font: str|None } }
      order_by_id: list of ids sorted lexicographically by id (english key)
    """
    path = CONFIG_DIR / "character.yaml"
    data = _read_yaml(path)

    meta: Dict[str, Dict[str, Any]] = {}

    if "character" in data and isinstance(data["character"], dict):
        raw = data["character"]
        for cid, cfg in raw.items():
            if not isinstance(cfg, dict):
                continue
            name = cfg.get("name")
            color = cfg.get("color")
            font = cfg.get("font")
            if isinstance(color, (list, tuple)) and len(color) == 3:
                color_t = tuple(int(x) for x in color)
            else:
                color_t = (255, 255, 255)
            meta[cid] = {
                "name": str(name) if name is not None else cid,
                "color": color_t,
                "font": str(font) if font else None,
            }
    else:
        # Backward compatibility (old schemas)
        if "characters" in data and isinstance(data["characters"], dict):
            raw = data["characters"]
            for cid, cfg in raw.items():
                font = (cfg or {}).get("font")
                meta[cid] = {
                    "name": cid,
                    "color": (255, 255, 255),
                    "font": str(font) if font else None,
                }
        else:
            # Top-level mapping heuristic
            for cid, cfg in data.items():
                if isinstance(cfg, dict):
                    meta[cid] = {
                        "name": cid,
                        "color": (255, 255, 255),
                        "font": str(cfg.get("font")) if cfg.get("font") else None,
                    }

    # Order by english id lexicographically
    order = sorted(meta.keys())
    return meta, order


def load_settings() -> Dict[str, Any]:
    """Load optional settings override from config/settings.yaml."""
    path = CONFIG_DIR / "settings.yaml"
    data = _read_yaml(path)
    return data if isinstance(data, dict) else {}


def load_text_configs() -> Dict[str, Any]:
    """Load optional text decoration configs from config/text_configs.yaml."""
    path = CONFIG_DIR / "text_configs.yaml"
    data = _read_yaml(path)
    return data if isinstance(data, dict) else {}
