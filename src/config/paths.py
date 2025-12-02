from __future__ import annotations

import os
from pathlib import Path

# Standardized project paths for Textbox
# This file is at: src/config/paths.py
# parents[0]=.../src/config, [1]=.../src, [2]=.../
SRC_ROOT = Path(__file__).resolve().parents[1]  # .../src
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # repo root

# Config directory at project root
CONFIG_DIR = PROJECT_ROOT / "config"

# Always use the repository-root resource directory
RESOURCE_ROOT = PROJECT_ROOT / "resource"

BACKGROUND_DIR = RESOURCE_ROOT / "background"
CHARACTER_DIR = RESOURCE_ROOT / "character"
FONT_DIR = RESOURCE_ROOT / "font"

# Cache directory (default repo_root/cache). Allow override via env.
CACHE_DIR = Path(os.getenv("TEXTBOX_CACHE_DIR", str(PROJECT_ROOT / "cache")))
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def font_path(font_file: str) -> Path:
    return FONT_DIR / font_file


def get_background_files() -> list[str]:
    """Return sorted list of PNG filenames (without extension) from background directory, ordered lexicographically."""
    if not BACKGROUND_DIR.is_dir():
        return []
    return sorted([p.stem for p in BACKGROUND_DIR.glob("*.png")])


def compose_name(character: str, expr_name: str, bg_name: str) -> str:
    """Generate cache filename from character, expression filename, and background filename."""
    # Sanitize filenames to avoid issues with special characters
    safe_expr = expr_name.replace(" ", "_").replace("(", "").replace(")", "")
    safe_bg = bg_name.replace(" ", "_").replace("(", "").replace(")", "")
    return f"{character}_{safe_expr}_{safe_bg}.png"


def cache_file(character: str, expr_name: str, bg_name: str) -> Path:
    return CACHE_DIR / compose_name(character, expr_name, bg_name)
