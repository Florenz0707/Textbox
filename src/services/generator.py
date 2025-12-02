from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Set, Tuple

from PIL import Image

from ..config.characters import character_list, characters
from ..config.paths import (
    BACKGROUND_DIR,
    CACHE_DIR,
    CHARACTER_DIR,
    cache_file,
    get_background_files,
)


@dataclass
class State:
    # Selection (0-based role index; expression/background are indices into filename lists)
    selected_role_index: int = 0
    selected_expr_index: int = 0
    selected_bg_index: int = 0

    # Roles confirmed (preloaded)
    confirmed_roles: Set[str] = field(default_factory=set)


def get_current_character(state: State) -> str:
    return character_list[state.selected_role_index]


def get_current_expression_files(state: State) -> List[str]:
    """Get list of expression filenames for current character."""
    name = get_current_character(state)
    return characters.get(name, {}).get("expression_files", [])


def get_current_background_files() -> List[str]:
    """Get list of background filenames."""
    return get_background_files()


def get_current_expression_name(state: State) -> str:
    """Get current expression filename (without extension)."""
    files = get_current_expression_files(state)
    if not files:
        return ""
    idx = max(0, min(state.selected_expr_index, len(files) - 1))
    return files[idx]


def get_current_background_name(state: State) -> str:
    """Get current background filename (without extension)."""
    files = get_current_background_files()
    if not files:
        return ""
    idx = max(0, min(state.selected_bg_index, len(files) - 1))
    return files[idx]


def show_current_character(state: State) -> None:
    print(f"当前角色: {get_current_character(state)}")


def set_role(state: State, new_index: int) -> None:
    if 0 <= new_index < len(character_list):
        state.selected_role_index = new_index
        # Reset expression index when switching role
        state.selected_expr_index = 0


def adjust_expr(state: State, delta: int) -> None:
    files = get_current_expression_files(state)
    if not files:
        state.selected_expr_index = 0
        return
    total = len(files)
    cur = state.selected_expr_index
    cur = (cur + delta) % total
    state.selected_expr_index = cur


def adjust_bg(state: State, delta: int) -> None:
    files = get_current_background_files()
    if not files:
        state.selected_bg_index = 0
        return
    total = len(files)
    cur = state.selected_bg_index
    cur = (cur + delta) % total
    state.selected_bg_index = cur


def ensure_character_prepared(character_name: str) -> None:
    # 若缓存中已有该角色文件前缀，视为已生成
    if any(
        p.name.startswith(f"{character_name}_")
        for p in CACHE_DIR.glob(f"{character_name}_*.png")
    ):
        return
    generate_and_save_images(character_name)


def generate_and_save_images(character_name: str) -> None:
    expr_files = characters.get(character_name, {}).get("expression_files", [])
    bg_files = get_background_files()

    if not expr_files:
        print(f"未找到角色 {character_name} 的表情资源，跳过预合成。")
        return

    if not bg_files:
        print(f"未找到背景资源，跳过预合成。")
        return

    print("正在加载")
    char_dir = CHARACTER_DIR / character_name

    for bg_name in bg_files:
        background_path = BACKGROUND_DIR / f"{bg_name}.png"
        if not background_path.is_file():
            continue
        background = Image.open(background_path).convert("RGBA")

        for expr_name in expr_files:
            overlay_path = char_dir / f"{expr_name}.png"
            if not overlay_path.is_file():
                continue
            overlay = Image.open(overlay_path).convert("RGBA")

            result = background.copy()
            result.paste(overlay, (0, 134), overlay)

            save_path = cache_file(character_name, expr_name, bg_name)
            result.save(save_path)

    print("加载完成")


def get_selection(state: State) -> Tuple[str, str]:
    """Get current selection as (expression_filename, background_filename)."""
    expr_name = get_current_expression_name(state)
    bg_name = get_current_background_name(state)

    # Fallback to empty strings if no files available
    if not expr_name:
        expr_files = get_current_expression_files(state)
        if expr_files:
            expr_name = expr_files[0]

    if not bg_name:
        bg_files = get_current_background_files()
        if bg_files:
            bg_name = bg_files[0]

    return expr_name, bg_name


def clear_cache() -> None:
    for p in CACHE_DIR.glob("*.png"):
        try:
            p.unlink()
        except Exception:
            pass
