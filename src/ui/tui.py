from __future__ import annotations

import msvcrt
import os
import time
from typing import Callable

from ..config.characters import character_list, character_meta
from ..config.settings import (
    AUTO_PASTE_IMAGE,
    AUTO_SEND_IMAGE,
    PASTE_HOTKEY,
    SEND_HOTKEY,
)
from ..services.generator import (
    State,
    adjust_bg,
    adjust_expr,
    get_current_background_files,
    get_current_background_name,
    get_current_character,
    get_current_expression_files,
    get_current_expression_name,
    set_role,
)

KEY_HELP = [
    "方向键 上/下：切换角色",
    "方向键 左/右：切换表情",
    "PgUp/PgDn：切换背景",
    "C：确认当前角色并预加载资源",
    "Q：退出",
]


def _clear():
    os.system("cls")


def _render(state: State, status: str | None = None) -> None:
    _clear()
    cid = get_current_character(state)
    meta = character_meta.get(cid, {})
    name = meta.get("name", cid)
    total_roles = len(character_list)

    expr_files = get_current_expression_files(state)
    bg_files = get_current_background_files()
    expr_total = len(expr_files)
    bg_total = len(bg_files)

    expr_name = get_current_expression_name(state) or "(无)"
    bg_name = get_current_background_name(state) or "(无)"
    expr_index = state.selected_expr_index + 1 if expr_total > 0 else 0
    bg_index = state.selected_bg_index + 1 if bg_total > 0 else 0

    print("文本框生成器（TUI 模式）")
    print("—" * 40)
    print(
        f"配置：自动粘贴={AUTO_PASTE_IMAGE}({PASTE_HOTKEY})，自动发送={AUTO_SEND_IMAGE}({SEND_HOTKEY})"
    )
    print(
        f"当前：角色[{state.selected_role_index + 1}/{total_roles}] {name} ({cid})  确认={'是' if (cid in state.confirmed_roles) else '否'}"
    )
    print(f"      表情[{expr_index}/{expr_total}] {expr_name}")
    print(f"      背景[{bg_index}/{bg_total}] {bg_name}")
    print("—" * 40)
    print("操作：")
    for line in KEY_HELP:
        print("- ", line)
    if status:
        print("—" * 40)
        print(status)


def run_tui(
    state: State,
    *,
    on_confirm: Callable[[State], str | None],
    on_generate: Callable[[State], str | None],
) -> None:
    status: str | None = None
    _render(state, status)
    while True:
        ch = msvcrt.getwch()
        if ch in ("q", "Q"):
            break
        if ch in ("c", "C"):
            status = on_confirm(state) or "已确认并预加载。"
            _render(state, status)
            continue

        # Special keys (arrows/PgUp/PgDn) start with '\xe0'
        if ch == "\xe0":
            code = msvcrt.getwch()
            if code == "H":  # Up
                new_idx = (state.selected_role_index - 1) % len(character_list)
                set_role(state, new_idx)
                status = None
                _render(state, status)
                continue
            if code == "P":  # Down
                new_idx = (state.selected_role_index + 1) % len(character_list)
                set_role(state, new_idx)
                status = None
                _render(state, status)
                continue
            if code == "K":  # Left
                adjust_expr(state, -1)
                status = None
                _render(state, status)
                continue
            if code == "M":  # Right
                adjust_expr(state, +1)
                status = None
                _render(state, status)
                continue
            if code == "I":  # PgUp
                adjust_bg(state, -1)
                status = None
                _render(state, status)
                continue
            if code == "Q":  # PgDn
                adjust_bg(state, +1)
                status = None
                _render(state, status)
                continue

        # Ignore other keys
        time.sleep(0.01)
