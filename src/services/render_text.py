from __future__ import annotations

from pathlib import Path
from typing import Tuple

from ..config.text_configs import text_configs_dict
from ..utils.text_draw import draw_text_auto


def render_text_to_bytes(
    base_image: Path,
    rect_top_left: Tuple[int, int],
    rect_bottom_right: Tuple[int, int],
    text: str,
    font_path: Path,
    role_name: str,
) -> bytes:
    return draw_text_auto(
        image_source=base_image,
        image_overlay=None,
        top_left=rect_top_left,
        bottom_right=rect_bottom_right,
        text=text,
        align="left",
        valign="top",
        color=(255, 255, 255),
        max_font_height=145,
        font_path=font_path,
        role_name=role_name,
        text_configs_dict=text_configs_dict,
    )
