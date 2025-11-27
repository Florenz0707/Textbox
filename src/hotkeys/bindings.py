from __future__ import annotations
from typing import Callable
import keyboard

from ..config.settings import HOTKEY
from ..services.generator import (
    State,
    switch_character,
    set_expression,
    show_current_character,
    clear_cache,
)


def bind_all(state: State, *, start_callback: Callable[[], None]) -> None:
    # Ctrl+1..9 角色1-9（注意：与旧逻辑保持一致传入 1..9）
    for idx in range(1, 10):
        keyboard.add_hotkey(f"ctrl+{idx}", lambda i=idx: switch_character(state, i))

    # 特殊映射（与旧版本一致）
    keyboard.add_hotkey('ctrl+q', lambda: switch_character(state, 10))  # 角色10
    keyboard.add_hotkey('ctrl+e', lambda: switch_character(state, 11))  # 角色11
    keyboard.add_hotkey('ctrl+r', lambda: switch_character(state, 12))  # 角色12
    keyboard.add_hotkey('ctrl+t', lambda: switch_character(state, 15))  # 角色13（注意：原代码如此）
    keyboard.add_hotkey('ctrl+y', lambda: switch_character(state, 0))   # 角色14（注意：原代码如此：0 -> -1）

    # 表情 Alt+1..9
    for idx in range(1, 10):
        keyboard.add_hotkey(f"alt+{idx}", lambda i=idx: set_expression(state, i))

    # 其他
    keyboard.add_hotkey('ctrl+0', lambda: show_current_character(state))
    keyboard.add_hotkey('ctrl+Tab', clear_cache)

    # 生成
    keyboard.add_hotkey(HOTKEY, start_callback, suppress=True)
