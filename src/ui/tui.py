from __future__ import annotations
import os
import time
import msvcrt
from typing import Callable

from ..config.characters import character_list, characters, character_meta
from ..config.settings import AUTO_PASTE_IMAGE, AUTO_SEND_IMAGE, PASTE_HOTKEY, SEND_HOTKEY, BACKGROUND_NUM
from ..services.generator import State, set_role, adjust_expr, adjust_bg, get_current_character


KEY_HELP = [
    "方向键 上/下：切换角色",
    "方向键 左/右：切换表情",
    "PgUp/PgDn：切换背景",
    "C：确认当前角色并预加载资源",
    "Enter：按当前选择生成（从剪贴板取文本或图片）",
    "Q：退出",
]


def _clear():
    os.system('cls')


def _render(state: State, status: str | None = None) -> None:
    _clear()
    cid = get_current_character(state)
    meta = character_meta.get(cid, {})
    name = meta.get("name", cid)
    total_roles = len(character_list)
    emo_total = int(characters.get(cid, {}).get("emotion_count", 0))

    print("文本框生成器（TUI 模式）")
    print("—" * 40)
    print(f"配置：自动粘贴={AUTO_PASTE_IMAGE}({PASTE_HOTKEY})，自动发送={AUTO_SEND_IMAGE}({SEND_HOTKEY})，背景总数={BACKGROUND_NUM}")
    print(f"当前：角色[{state.selected_role_index+1}/{total_roles}] {name} ({cid})  确认={'是' if (cid in state.confirmed_roles) else '否'}")
    print(f"      表情[{state.selected_expr}/{max(emo_total,1)}]  背景[{state.selected_bg}/{BACKGROUND_NUM}]")
    print("—" * 40)
    print("操作：")
    for line in KEY_HELP:
        print("- ", line)
    if status:
        print("—" * 40)
        print(status)


def run_tui(state: State, *, on_confirm: Callable[[State], str | None], on_generate: Callable[[State], str | None]) -> None:
    status: str | None = None
    _render(state, status)
    while True:
        ch = msvcrt.getwch()
        if ch in ('q', 'Q'):
            break
        if ch in ('c', 'C'):
            status = on_confirm(state) or "已确认并预加载。"
            _render(state, status)
            continue
        if ch == '\r':  # Enter
            status = on_generate(state) or "已生成到剪贴板。"
            _render(state, status)
            continue

        # Special keys (arrows/PgUp/PgDn) start with '\xe0'
        if ch == '\xe0':
            code = msvcrt.getwch()
            if code == 'H':  # Up
                new_idx = (state.selected_role_index - 1) % len(character_list)
                set_role(state, new_idx)
                status = None
                _render(state, status)
                continue
            if code == 'P':  # Down
                new_idx = (state.selected_role_index + 1) % len(character_list)
                set_role(state, new_idx)
                status = None
                _render(state, status)
                continue
            if code == 'K':  # Left
                adjust_expr(state, -1)
                status = None
                _render(state, status)
                continue
            if code == 'M':  # Right
                adjust_expr(state, +1)
                status = None
                _render(state, status)
                continue
            if code == 'I':  # PgUp
                adjust_bg(state, -1)
                status = None
                _render(state, status)
                continue
            if code == 'Q':  # PgDn
                adjust_bg(state, +1)
                status = None
                _render(state, status)
                continue

        # Ignore other keys
        time.sleep(0.01)
