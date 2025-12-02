from __future__ import annotations

from pathlib import Path
from typing import Tuple

from PIL import Image

from ..config.text_configs import text_configs_dict
from ..utils.image_paste import paste_image_auto


def paste_image_to_bytes(
    base_image: Path,
    rect_top_left: Tuple[int, int],
    rect_bottom_right: Tuple[int, int],
    content_image: Image.Image,
    *,
    allow_upscale: bool = True,
    keep_alpha: bool = True,
    role_name: str,
) -> bytes:
    return paste_image_auto(
        image_source=base_image,
        image_overlay=None,
        top_left=rect_top_left,
        bottom_right=rect_bottom_right,
        content_image=content_image,
        align="center",
        valign="middle",
        padding=12,
        allow_upscale=allow_upscale,
        keep_alpha=keep_alpha,
        role_name=role_name,
        text_configs_dict=text_configs_dict,
    )
