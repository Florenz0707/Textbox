from __future__ import annotations
from typing import Any

# Load overrides from config/settings.yaml if present
try:
    from .loader import load_settings
    _ov: dict[str, Any] = load_settings()
except Exception:
    _ov = {}


def _g(key: str, default: Any) -> Any:
    # support lower/upper case keys in yaml
    return _ov.get(key, _ov.get(key.lower(), default))

# 热键与行为控制
HOTKEY: str = _g("HOTKEY", "enter")
SELECT_ALL_HOTKEY: str = _g("SELECT_ALL_HOTKEY", "ctrl+a")
CUT_HOTKEY: str = _g("CUT_HOTKEY", "ctrl+x")
PASTE_HOTKEY: str = _g("PASTE_HOTKEY", "ctrl+v")
SEND_HOTKEY: str = _g("SEND_HOTKEY", "enter")

BLOCK_HOTKEY: bool = bool(_g("BLOCK_HOTKEY", False))  # 生成热键是否阻塞
DELAY: float = float(_g("DELAY", 0.1))                 # 操作间隔（秒）
AUTO_PASTE_IMAGE: bool = bool(_g("AUTO_PASTE_IMAGE", True))
AUTO_SEND_IMAGE: bool = bool(_g("AUTO_SEND_IMAGE", True))

# 白名单（前台窗口进程名）
WHITELIST: list[str] = list(_g("WHITELIST", ["TIM.exe", "WeChat.exe", "Weixin.exe", "WeChatApp.exe", "QQ.exe"]))
ENABLE_WHITELIST: bool = bool(_g("ENABLE_WHITELIST", True))

# 资源与生成
BACKGROUND_NUM: int = int(_g("BACKGROUND_NUM", 16))

# 文本区域（像素坐标）
_tsp = _g("TEXT_ST_POS", (728, 355))
TEXT_ST_POS: tuple[int, int] = tuple(_tsp) if isinstance(_tsp, (list, tuple)) else (728, 355)
_tep = _g("TEXT_ED_POS", (2339, 800))
TEXT_ED_POS: tuple[int, int] = tuple(_tep) if isinstance(_tep, (list, tuple)) else (2339, 800)
