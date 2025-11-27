from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple, Set

from PIL import Image

from ..config.characters import characters, character_list
from ..config.paths import (
    BACKGROUND_DIR,
    CHARACTER_DIR,
    CACHE_DIR,
    cache_file,
)
from ..config.settings import BACKGROUND_NUM


@dataclass
class State:
    # Selection (0-based role index; expression/background are 1-based to match filenames)
    selected_role_index: int = 0
    selected_expr: int = 1
    selected_bg: int = 1

    # Roles confirmed (preloaded)
    confirmed_roles: Set[str] = field(default_factory=set)


def get_current_character(state: State) -> str:
    return character_list[state.selected_role_index]


def get_current_emotion_count(state: State) -> int:
    name = get_current_character(state)
    return int(characters.get(name, {}).get("emotion_count", 0))


def show_current_character(state: State) -> None:
    print(f"当前角色: {get_current_character(state)}")


def set_role(state: State, new_index: int) -> None:
    if 0 <= new_index < len(character_list):
        state.selected_role_index = new_index
        # Reset expression to 1 when switching role
        state.selected_expr = 1


def adjust_expr(state: State, delta: int) -> None:
    total = get_current_emotion_count(state)
    if total <= 0:
        state.selected_expr = 1
        return
    cur = state.selected_expr
    cur = ((cur - 1 + delta) % total) + 1
    state.selected_expr = cur


def adjust_bg(state: State, delta: int) -> None:
    total = BACKGROUND_NUM
    cur = state.selected_bg
    cur = ((cur - 1 + delta) % total) + 1
    state.selected_bg = cur


def ensure_character_prepared(character_name: str) -> None:
    # 若缓存中已有该角色文件前缀，视为已生成
    if any(p.name.startswith(f"{character_name}_") for p in CACHE_DIR.glob(f"{character_name}_*.png")):
        return
    generate_and_save_images(character_name)


def generate_and_save_images(character_name: str) -> None:
    emotion_count = int(characters.get(character_name, {}).get("emotion_count", 0))
    if emotion_count < 1:
        print(f"未找到角色 {character_name} 的表情资源，跳过预合成。")
        return

    print("正在加载")
    for bg_idx in range(1, BACKGROUND_NUM + 1):
        background_path = BACKGROUND_DIR / f"c{bg_idx}.png"
        background = Image.open(background_path).convert("RGBA")

        for emo_idx in range(1, emotion_count + 1):
            overlay_path = CHARACTER_DIR / character_name / f"{character_name} ({emo_idx}).png"
            if not overlay_path.is_file():
                continue
            overlay = Image.open(overlay_path).convert("RGBA")

            result = background.copy()
            result.paste(overlay, (0, 134), overlay)

            save_path = cache_file(character_name, emo_idx, bg_idx)
            result.save(save_path)

    print("加载完成")


def get_selection(state: State) -> Tuple[int, int]:
    # Ensure selection within bounds
    if get_current_emotion_count(state) <= 0:
        return 1, 1
    expr = max(1, min(state.selected_expr, get_current_emotion_count(state)))
    bg = max(1, min(state.selected_bg, BACKGROUND_NUM))
    return expr, bg


def clear_cache() -> None:
    for p in CACHE_DIR.glob("*.png"):
        try:
            p.unlink()
        except Exception:
            pass
