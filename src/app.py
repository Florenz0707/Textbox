from __future__ import annotations

import time
from pathlib import Path

# Bootstrap to support running as a standalone script: `python src/app.py`
if __name__ == "__main__" and __package__ is None:
    import sys

    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

# Prefer relative imports; fallback to absolute
import logging

import keyboard

from src.config.characters import character_list, character_meta, characters
from src.config.paths import cache_file, font_path
from src.config.settings import (
    AUTO_PASTE_IMAGE,
    AUTO_SEND_IMAGE,
    BLOCK_HOTKEY,
    ENABLE_WHITELIST,
    PASTE_HOTKEY,
    SEND_HOTKEY,
    TEXT_ED_POS,
    TEXT_ST_POS,
    WHITELIST,
)
from src.io.clipboard import copy_png_bytes_to_clipboard, cut_all_capture
from src.io.keys import send
from src.io.window import get_foreground_exe_name
from src.services.generator import (
    State,
    ensure_character_prepared,
    get_current_character,
    get_selection,
)
from src.services.paste_image import paste_image_to_bytes
from src.services.render_text import render_text_to_bytes
from src.utils.logging_setup import setup_logging

logger = logging.getLogger(__name__)


def _log_text_preview(text: str, limit: int = 1000) -> str:
    try:
        if len(text) > limit:
            return text[:limit] + f"...(truncated, len={len(text)})"
        return text
    except Exception:
        return text


def _build_banner() -> str:
    role_lines = []
    for idx, cid in enumerate(character_list, start=1):
        name = character_meta.get(cid, {}).get("name", cid)
        role_lines.append(f"- {idx}\t{name} ({cid})")

    wl = ", ".join(WHITELIST) if ENABLE_WHITELIST else "禁用"

    lines = [
        "文本框生成器（TUI + 全局发送热键）",
        "—" * 40,
        "角色列表：",
        *role_lines,
        "",
        "操作（TUI内）：",
        "- 方向键 上/下：切换角色",
        "- 方向键 左/右：切换表情",
        "- PgUp/PgDn：切换背景",
        "- C：确认当前角色并预加载资源",
        "- Q：退出",
        "",
        f"全局发送热键：{SEND_HOTKEY}（白名单：{wl}）",
        f"生成后：自动粘贴={AUTO_PASTE_IMAGE}({PASTE_HOTKEY})，",
        f"自动发送={AUTO_SEND_IMAGE}({SEND_HOTKEY})",
        "",
        "提示：请先在 TUI 中按 C 确认角色完成预加载，然后到聊天窗口按发送热键触发生成。",
    ]
    return "\n".join(lines)


def _generate_with_current_selection(state: State) -> str | None:
    character_name = get_current_character(state)
    if character_name not in state.confirmed_roles:
        msg = "未确认当前角色（请在 TUI 中按 C 预加载）"
        logger.warning(msg)
        return msg

    expr, bg = get_selection(state)
    baseimage_file = cache_file(character_name, expr, bg)
    logger.info(
        "开始生成: role=%s expr=%d bg=%d base=%s",
        character_name,
        expr,
        bg,
        baseimage_file,
    )

    rect_top_left = TEXT_ST_POS
    rect_bottom_right = TEXT_ED_POS

    # 按需求：全选并剪切当前内容，再基于剪切到的内容生成
    text = ""
    image = None
    try:
        text, image = cut_all_capture()
    except Exception as e:
        logger.exception("剪切当前内容失败: %s", e)
        text, image = "", None

    if image is not None:
        try:
            logger.info(
                "图片输入: size=%dx%d mode=%s",
                getattr(image, "width", -1),
                getattr(image, "height", -1),
                getattr(image, "mode", "unknown"),
            )
        except Exception:
            pass
    elif text:
        logger.info("文本输入(预览): %s", _log_text_preview(text))

    if (not text) and image is None:
        msg = "剪贴板无文本或图片可用（剪切后为空）"
        logger.warning(msg)
        return msg

    try:
        if image is not None:
            png_bytes = paste_image_to_bytes(
                base_image=baseimage_file,
                rect_top_left=rect_top_left,
                rect_bottom_right=rect_bottom_right,
                content_image=image,
                role_name=character_name,
            )
        else:
            fp = font_path(characters[character_name]["font"])  # resource/font 下
            png_bytes = render_text_to_bytes(
                base_image=baseimage_file,
                rect_top_left=rect_top_left,
                rect_bottom_right=rect_bottom_right,
                text=text,
                font_path=fp,
                role_name=character_name,
            )
    except Exception as e:
        logger.exception("生成失败: %s", e)
        return f"生成失败: {e}"

    try:
        copy_png_bytes_to_clipboard(png_bytes)
        logger.info("已写入剪贴板 PNG: %d bytes", len(png_bytes))
    except Exception as e:
        logger.exception("写入剪贴板失败: %s", e)
        return f"复制到剪贴板失败: {e}"

    if AUTO_PASTE_IMAGE:
        try:
            send(PASTE_HOTKEY)
            time.sleep(0.3)
            if AUTO_SEND_IMAGE:
                send(SEND_HOTKEY)
            logger.info("已模拟粘贴%s", "并发送" if AUTO_SEND_IMAGE else "")
        except Exception as e:
            logger.exception("模拟粘贴/发送失败: %s", e)
            return f"已复制但粘贴/发送失败: {e}"
    return "已复制到剪贴板" + (" 并已粘贴/发送" if AUTO_PASTE_IMAGE else "")


def _global_send_callback(state: State):
    # 白名单检查
    if ENABLE_WHITELIST:
        exe = get_foreground_exe_name()
        if not exe or exe not in WHITELIST:
            # 透传按键
            send(SEND_HOTKEY)
            return

    msg = _generate_with_current_selection(state)
    if msg:
        logger.info("全局发送回调: %s", msg)


def _setup_global_send_hotkey(state: State) -> None:
    suppress_flag = (
        True if (BLOCK_HOTKEY or True) else False
    )  # 发送热键一律抑制，避免原始回车提前发送
    try:
        keyboard.add_hotkey(
            SEND_HOTKEY, lambda: _global_send_callback(state), suppress=suppress_flag
        )
        logger.info("已注册全局发送热键: %s (suppress=%s)", SEND_HOTKEY, suppress_flag)
    except Exception as e:
        logger.exception("注册全局发送热键失败: %s", e)


def _on_confirm(state: State) -> str | None:
    name = get_current_character(state)
    try:
        ensure_character_prepared(name)
        state.confirmed_roles.add(name)
        msg = f"已确认并预加载角色：{name}"
        logger.info(msg)
        return msg
    except Exception as e:
        logger.exception("预加载失败: %s", e)
        return f"预加载失败: {e}"


def main() -> None:
    setup_logging()  # overwrite log.txt on each start
    logger.info("应用启动。角色数=%d", len(character_list))
    print(_build_banner())

    state = State()

    # 全局发送热键（在后台监听）
    _setup_global_send_hotkey(state)

    # 进入 TUI 主循环（用于切换与确认）
    try:
        from .ui.tui import run_tui  # late import to avoid circular
    except Exception:
        from src.ui.tui import run_tui
    run_tui(state, on_confirm=_on_confirm, on_generate=lambda s: None)

    logger.info("应用退出。")


if __name__ == "__main__":
    main()
