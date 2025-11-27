from __future__ import annotations
import time
from pathlib import Path

# Bootstrap to support running as a standalone script: `python src/app.py`
# This allows falling back to absolute imports (from src....) when package context is missing.
if __name__ == "__main__" and __package__ is None:
    import sys
    project_root = Path(__file__).resolve().parent.parent  # repo root
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

# Prefer relative imports (package mode), fallback to absolute imports (script mode)
try:
    from .config.settings import (
        HOTKEY,
        BLOCK_HOTKEY,
        PASTE_HOTKEY,
        SEND_HOTKEY,
        ENABLE_WHITELIST,
        WHITELIST,
        AUTO_PASTE_IMAGE,
        AUTO_SEND_IMAGE,
        TEXT_ST_POS,
        TEXT_ED_POS,
    )
    from .config.characters import characters
    from .config.paths import cache_file, font_path
    from .hotkeys.bindings import bind_all
    from .services.generator import (
        State,
        get_current_character,
        get_random_expr_bg,
        ensure_character_prepared,
        show_current_character,
    )
    from .io.window import get_foreground_exe_name
    from .io.keys import send
    from .io.clipboard import (
        cut_all_and_get_text,
        try_get_image,
        copy_png_bytes_to_clipboard,
    )
    from .services.paste_image import paste_image_to_bytes
    from .services.render_text import render_text_to_bytes
except Exception:
    from src.config.settings import (
        HOTKEY,
        BLOCK_HOTKEY,
        PASTE_HOTKEY,
        SEND_HOTKEY,
        ENABLE_WHITELIST,
        WHITELIST,
        AUTO_PASTE_IMAGE,
        AUTO_SEND_IMAGE,
        TEXT_ST_POS,
        TEXT_ED_POS,
    )
    from src.config.characters import characters
    from src.config.paths import cache_file, font_path
    from src.hotkeys.bindings import bind_all
    from src.services.generator import (
        State,
        get_current_character,
        get_random_expr_bg,
        ensure_character_prepared,
        show_current_character,
    )
    from src.io.window import get_foreground_exe_name
    from src.io.keys import send
    from src.io.clipboard import (
        cut_all_and_get_text,
        try_get_image,
        copy_png_bytes_to_clipboard,
    )
    from src.services.paste_image import paste_image_to_bytes
    from src.services.render_text import render_text_to_bytes



def _print_banner() -> None:
    print(
        """角色说明:
1为樱羽艾玛，2为二阶堂希罗，3为橘雪莉，4为远野汉娜
5为夏目安安，6为月代雪，7为冰上梅露露，8为城崎诺亚，9为莲见蕾雅，10为佐伯米莉亚
11为黑部奈叶香，12为宝生玛格，13为紫藤亚里沙，14为泽渡可可

快捷键说明:
Ctrl+1 到 Ctrl+9: 切换角色1-9
Ctrl+q: 切换角色10
Ctrl+w: 切换角色11
Ctrl+e: 切换角色12
Ctrl+r: 切换角色13
Ctrl+t: 切换角色14
Ctrl+0: 显示当前角色
Alt+1-9: 切换表情1-9(部分角色表情较少 望大家谅解)
Enter: 生成图片
Esc: 退出程序
Ctrl+Tab: 清除图片

程序说明：
首次更换角色需预加载，需等待数秒；清除缓存后建议重启。
感谢支持。
"""
    )


def _start_callback(state: State) -> None:
    # 白名单检查：启用白名单且当前窗口不在白名单 -> 透传按键
    if ENABLE_WHITELIST:
        exe = get_foreground_exe_name()
        if not exe or exe not in WHITELIST:
            send(HOTKEY)
            return

    print("Start generate...")
    character_name = get_current_character(state)
    ensure_character_prepared(character_name)

    expr, bg = get_random_expr_bg(state)
    baseimage_file = cache_file(character_name, expr, bg)
    print(f"角色：{character_name}，表情：{expr}，背景：{bg}")

    rect_top_left = TEXT_ST_POS
    rect_bottom_right = TEXT_ED_POS

    text = cut_all_and_get_text()
    image = try_get_image()

    if (not text) and image is None:
        print("no text or image")
        return

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
        print("Generate image failed:", e)
        return

    copy_png_bytes_to_clipboard(png_bytes)

    if AUTO_PASTE_IMAGE:
        send(PASTE_HOTKEY)
        time.sleep(0.3)
        if AUTO_SEND_IMAGE:
            send(SEND_HOTKEY)


def main() -> None:
    state = State()
    _print_banner()
    show_current_character(state)
    ensure_character_prepared(get_current_character(state))

    bind_all(state, start_callback=lambda: _start_callback(state))

    suppress_flag = (BLOCK_HOTKEY or HOTKEY == SEND_HOTKEY)
    # 重新绑定主热键以遵循 suppress 策略（bindings 默认 suppress=True 已注册，此处仅保证一致性）
    try:
        import keyboard  # local import to avoid import-order issues in script mode
        keyboard.remove_hotkey(HOTKEY)
        keyboard.add_hotkey(HOTKEY, lambda: _start_callback(state), suppress=suppress_flag)
    except Exception:
        pass

    try:
        import keyboard
        keyboard.wait("Esc")
    except Exception:
        pass


if __name__ == "__main__":
    main()
