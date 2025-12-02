from __future__ import annotations

import io
import time
from typing import Optional, Tuple

import pyperclip
from PIL import Image
from win32 import win32clipboard

from ..config.settings import CUT_HOTKEY, DELAY, SELECT_ALL_HOTKEY
from .keys import send


def _open_clipboard_with_retry(retries: int = 15, delay: float = 0.08) -> bool:
    """Try to open the clipboard with retry/backoff to avoid ERROR_ACCESS_DENIED (5)."""
    for _ in range(max(1, retries)):
        try:
            win32clipboard.OpenClipboard()
            return True
        except Exception:
            time.sleep(delay)
    return False


def copy_png_bytes_to_clipboard(png_bytes: bytes) -> None:
    """将 PNG 字节写入剪贴板（以 DIB/BMP 方式）。"""
    image = Image.open(io.BytesIO(png_bytes))
    with io.BytesIO() as output:
        image.convert("RGB").save(output, "BMP")
        bmp_data = output.getvalue()[14:]

    if not _open_clipboard_with_retry():
        print("无法打开剪贴板以写入数据（被占用）。")
        return
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, bmp_data)
    finally:
        try:
            win32clipboard.CloseClipboard()
        except Exception:
            pass


def cut_all_and_get_text() -> str:
    """模拟 Ctrl+A / Ctrl+X 剪切全部文本，并返回剪切得到的内容。会还原剪贴板。"""
    old_clip = pyperclip.paste()
    pyperclip.copy("")

    send(SELECT_ALL_HOTKEY)
    send(CUT_HOTKEY)
    time.sleep(max(0.12, DELAY))  # 稍微放大以避免剪贴板竞争

    new_clip = pyperclip.paste()
    pyperclip.copy(old_clip)
    return new_clip


def try_get_image() -> Optional[Image.Image]:
    """尝试从剪贴板获取图像，如果没有图像则返回 None（仅支持 Windows）。"""
    if not _open_clipboard_with_retry():
        print("无法从剪贴板获取图像：剪贴板正被占用")
        return None
    try:
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
            data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
            if data:
                bmp_data = data
                header = (
                    b"BM"
                    + (len(bmp_data) + 14).to_bytes(4, "little")
                    + b"\x00\x00\x00\x00\x36\x00\x00\x00"
                )
                image = Image.open(io.BytesIO(header + bmp_data))
                return image
    except Exception as e:
        print("无法从剪贴板获取图像：", e)
    finally:
        try:
            win32clipboard.CloseClipboard()
        except Exception:
            pass
    return None


def cut_all_capture() -> Tuple[str, Optional[Image.Image]]:
    """
    剪切前台输入框的全部内容并捕获剪贴板当前内容（文本或图像），不恢复原剪贴板。
    返回: (text, image)，二者至少一个有值；若都无，则均为空/None。
    """
    # 清空文本通道，避免读到旧文本
    try:
        pyperclip.copy("")
    except Exception:
        pass

    # 发送 Ctrl+A / Ctrl+X
    send(SELECT_ALL_HOTKEY)
    send(CUT_HOTKEY)
    time.sleep(max(0.12, DELAY))

    # 优先尝试图像
    image = None
    if _open_clipboard_with_retry():
        try:
            if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
                data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
                if data:
                    bmp_data = data
                    header = (
                        b"BM"
                        + (len(bmp_data) + 14).to_bytes(4, "little")
                        + b"\x00\x00\x00\x00\x36\x00\x00\x00"
                    )
                    image = Image.open(io.BytesIO(header + bmp_data))
        except Exception:
            image = None
        finally:
            try:
                win32clipboard.CloseClipboard()
            except Exception:
                pass

    # 再读取文本
    text = ""
    try:
        text = pyperclip.paste() or ""
    except Exception:
        text = ""

    return text, image
