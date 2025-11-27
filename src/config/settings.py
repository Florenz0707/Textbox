from __future__ import annotations

# 热键与行为控制
HOTKEY: str = "enter"
SELECT_ALL_HOTKEY: str = "ctrl+a"
CUT_HOTKEY: str = "ctrl+x"
PASTE_HOTKEY: str = "ctrl+v"
SEND_HOTKEY: str = "enter"

BLOCK_HOTKEY: bool = False  # 生成热键是否阻塞
DELAY: float = 0.1          # 操作间隔（秒）
AUTO_PASTE_IMAGE: bool = True
AUTO_SEND_IMAGE: bool = True

# 白名单（前台窗口进程名）
WHITELIST: list[str] = ["TIM.exe", "WeChat.exe", "Weixin.exe", "WeChatApp.exe", "QQ.exe"]
ENABLE_WHITELIST: bool = True

# 资源与生成
BACKGROUND_NUM: int = 16

# 文本区域（像素坐标）
TEXT_ST_POS: tuple[int, int] = (728, 355)
TEXT_ED_POS: tuple[int, int] = (2339, 800)
