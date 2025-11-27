from __future__ import annotations
from dataclasses import dataclass

import random

from typing import Tuple
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
    current_character_index: int = 10  # 与旧版保持一致（1-based 语义配合 get_current_character())
    last_random_value: int = -1
    forced_expression: int | None = None  # Alt+N 指定本次表情


def get_current_character(state: State) -> str:
    return character_list[state.current_character_index - 1]


def get_current_emotion_count(state: State) -> int:
    return characters.get(get_current_character(state), {}).get("emotion_count", 0)


def set_expression(state: State, idx: int) -> None:
    name = get_current_character(state)
    emotion_count = characters.get(name, {}).get("emotion_count", 0)
    if 1 <= idx <= emotion_count:
        print(f"已切换至第{idx}个表情")
        state.forced_expression = idx


def show_current_character(state: State) -> None:
    print(f"当前角色: {get_current_character(state)}")


def switch_character(state: State, new_index: int) -> bool:
    # 仍按既有逻辑：接受 0..len-1（注意当前 state 以 1-based 取名）
    if 0 <= new_index < len(character_list):
        state.current_character_index = new_index
        character_name = get_current_character(state)
        print(f"已切换到角色: {character_name}")
        ensure_character_prepared(character_name)
        return True
    return False


def ensure_character_prepared(character_name: str) -> None:
    # 若缓存中已有该角色文件前缀，视为已生成
    if any(p.name.startswith(f"{character_name}_") for p in CACHE_DIR.glob(f"{character_name}_*.png")):
        return
    generate_and_save_images(character_name)


def generate_and_save_images(character_name: str) -> None:
    emotion_count = characters.get(character_name, {}).get("emotion_count", 0)
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
                # 允许中间缺号，直接跳过
                continue
            overlay = Image.open(overlay_path).convert("RGBA")

            result = background.copy()
            result.paste(overlay, (0, 134), overlay)

            save_path = cache_file(character_name, emo_idx, bg_idx)
            result.save(save_path)

    print("加载完成")


def clear_cache() -> None:
    for p in CACHE_DIR.glob("*.png"):
        try:
            p.unlink()
        except Exception:
            pass


def get_random_expr_bg(state: State) -> Tuple[int, int]:
    # 返回 (expression, background) 1-based
    emotion_count = get_current_emotion_count(state)
    if emotion_count < 1:
        raise ValueError("当前角色没有可用的表情资源")

    total_images = BACKGROUND_NUM * emotion_count

    if state.forced_expression is not None:
        if not (1 <= state.forced_expression <= emotion_count):
            state.forced_expression = None
        else:
            rv = random.randint((state.forced_expression - 1) * BACKGROUND_NUM + 1,
                                state.forced_expression * BACKGROUND_NUM)
            state.last_random_value = rv
            expr = (rv - 1) // BACKGROUND_NUM + 1
            bg = (rv - 1) % BACKGROUND_NUM + 1
            state.forced_expression = None
            return expr, bg

    max_attempts = 100
    attempts = 0
    while attempts < max_attempts:
        rv = random.randint(1, total_images)
        current_emotion = (rv - 1) // BACKGROUND_NUM

        if state.last_random_value == -1:
            state.last_random_value = rv
            break

        if current_emotion != (state.last_random_value - 1) // BACKGROUND_NUM:
            state.last_random_value = rv
            break
        attempts += 1

    expr = (state.last_random_value - 1) // BACKGROUND_NUM + 1
    bg = (state.last_random_value - 1) % BACKGROUND_NUM + 1
    return expr, bg
