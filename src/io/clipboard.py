from __future__ import annotations
import io
import time
from typing import Optional

import pyperclip
from PIL import Image
from win32 import win32clipboard

from ..config.settings import SELECT_ALL_HOTKEY, CUT_HOTKEY, DELAY
from .keys import send


def copy_png_bytes_to_clipboard(png_bytes: bytes) -> None:
    """将 PNG 字节写入剪贴板（以 DIB/BMP 方式）。"""
    image = Image.open(io.BytesIO(png_bytes))
    with io.BytesIO() as output:
        image.convert("RGB").save(output, "BMP")
        bmp_data = output.getvalue()[14:]
    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, bmp_data)
    finally:
        win32clipboard.CloseClipboard()


def cut_all_and_get_text() -> str:
    """模拟 Ctrl+A / Ctrl+X 剪切全部文本，并返回剪切得到的内容。"""
    old_clip = pyperclip.paste()
    pyperclip.copy("")

    send(SELECT_ALL_HOTKEY)
    send(CUT_HOTKEY)
    time.sleep(DELAY)

    new_clip = pyperclip.paste()
    pyperclip.copy(old_clip)
    return new_clip


def try_get_image() -> Optional[Image.Image]:
    """尝试从剪贴板获取图像，如果没有图像则返回 None（仅支持 Windows）。"""
    try:
        win32clipboard.OpenClipboard()
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_DIB):
            data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
            if data:
                bmp_data = data
                header = b'BM' + (len(bmp_data) + 14).to_bytes(4, 'little') + b'\x00\x00\x00\x00\x36\x00\x00\x00'
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
