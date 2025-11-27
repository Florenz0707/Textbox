from __future__ import annotations
from pathlib import Path
import os

# Standardized project paths for Textbox
# This file is at: src/config/paths.py
# parents[0]=.../src/config, [1]=.../src, [2]=.../
SRC_ROOT = Path(__file__).resolve().parents[1]       # .../src
PROJECT_ROOT = Path(__file__).resolve().parents[2]   # repo root

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


def compose_name(character: str, expr: int, bg: int) -> str:
    return f"{character}_{expr}_{bg}.png"


def cache_file(character: str, expr: int, bg: int) -> Path:
    return CACHE_DIR / compose_name(character, expr, bg)
