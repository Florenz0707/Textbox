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
try:
    from .config.settings import (
        AUTO_PASTE_IMAGE,
        AUTO_SEND_IMAGE,
        PASTE_HOTKEY,
        SEND_HOTKEY,
        TEXT_ST_POS,
        TEXT_ED_POS,
    )
    from .config.characters import characters, character_list, character_meta
    from .config.paths import cache_file, font_path
    from .services.generator import (
        State,
        get_current_character,
        ensure_character_prepared,
        get_selection,
    )
    from .io.keys import send
    from .io.clipboard import (
        try_get_image,
        copy_png_bytes_to_clipboard,
    )
    from .services.paste_image import paste_image_to_bytes
    from .services.render_text import render_text_to_bytes
    from .ui.tui import run_tui
    import pyperclip
except Exception:
    from src.config.settings import (
        AUTO_PASTE_IMAGE,
        AUTO_SEND_IMAGE,
        PASTE_HOTKEY,
        SEND_HOTKEY,
        TEXT_ST_POS,
        TEXT_ED_POS,
    )
    from src.config.characters import characters, character_list, character_meta
    from src.config.paths import cache_file, font_path
    from src.services.generator import (
        State,
        get_current_character,
        ensure_character_prepared,
        get_selection,
    )
    from src.io.keys import send
    from src.io.clipboard import (
        try_get_image,
        copy_png_bytes_to_clipboard,
    )
    from src.services.paste_image import paste_image_to_bytes
    from src.services.render_text import render_text_to_bytes
    from src.ui.tui import run_tui
    import pyperclip


def _build_banner() -> str:
    role_lines = []
    for idx, cid in enumerate(character_list, start=1):
        name = character_meta.get(cid, {}).get("name", cid)
        role_lines.append(f"- {idx}\t{name} ({cid})")

    lines = [
        "文本框生成器（TUI 模式）",
        "—" * 40,
        "角色列表：",
        *role_lines,
        "",
        "操作：",
        "- 方向键 上/下：切换角色",
        "- 方向键 左/右：切换表情",
        "- PgUp/PgDn：切换背景",
        "- C：确认当前角色并预加载资源",
        "- Enter：按当前选择生成（从剪贴板取文本或图片）",
        "- Q：退出",
        "",
        f"配置：自动粘贴={AUTO_PASTE_IMAGE}({PASTE_HOTKEY})，自动发送={AUTO_SEND_IMAGE}({SEND_HOTKEY})",
        "",
        "提示：请先按 C 确认角色完成预加载，再按 Enter 生成。",
    ]
    return "\n".join(lines)


def _on_confirm(state: State) -> str | None:
    name = get_current_character(state)
    ensure_character_prepared(name)
    state.confirmed_roles.add(name)
    return f"已确认并预加载角色：{name}"


def _on_generate(state: State) -> str | None:
    character_name = get_current_character(state)
    if character_name not in state.confirmed_roles:
        return "请先按 C 确认并预加载当前角色"

    expr, bg = get_selection(state)
    baseimage_file = cache_file(character_name, expr, bg)

    rect_top_left = TEXT_ST_POS
    rect_bottom_right = TEXT_ED_POS

    # Clipboard-first: try image, else text
    image = try_get_image()
    text = pyperclip.paste() if not image else ""

    if (not text) and image is None:
        return "剪贴板无文本或图片可用"

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
        return f"生成失败: {e}"

    copy_png_bytes_to_clipboard(png_bytes)

    if AUTO_PASTE_IMAGE:
        send(PASTE_HOTKEY)
        time.sleep(0.3)
        if AUTO_SEND_IMAGE:
            send(SEND_HOTKEY)
    return "已复制到剪贴板" + (" 并已粘贴/发送" if AUTO_PASTE_IMAGE else "")


def main() -> None:
    state = State()
    print(_build_banner())
    # 进入 TUI 主循环
    run_tui(state, on_confirm=_on_confirm, on_generate=_on_generate)


if __name__ == "__main__":
    main()
