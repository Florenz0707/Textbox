from __future__ import annotations
import keyboard


def send(hotkey: str) -> None:
    keyboard.send(hotkey)
