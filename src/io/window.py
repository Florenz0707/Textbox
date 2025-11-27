from __future__ import annotations

from pathlib import Path

import psutil
from win32 import win32gui
from win32 import win32process


def get_foreground_exe_name() -> str | None:
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        exe_path = process.exe()
        return Path(exe_path).name
    except Exception as e:
        print(f"获取文件名时发生错误：{e}")
        return None
