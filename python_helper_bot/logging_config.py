import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

def setup_logging(level: str = "INFO", log_dir: str = "logs") -> None:
    lvl = getattr(logging, level.upper(), logging.INFO)

    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_path = Path(log_dir) / "bot.log"

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console = logging.StreamHandler(sys.stdout)
    console.setLevel(lvl)
    console.setFormatter(fmt)

    file_handler = RotatingFileHandler(
        filename=str(log_path),
        maxBytes=5 * 1024 * 1024, # 5 MB
        backupCount=5, # хранить 5 архивных файлов
        encoding="utf-8",
    )
    file_handler.setLevel(lvl)
    file_handler.setFormatter(fmt)

    root = logging.getLogger()
    root.setLevel(lvl)

    # важно: не накапливать хендлеры при перезапуске в одной сессии
    root.handlers.clear()
    root.addHandler(console)
    root.addHandler(file_handler)

    # уменьшаем шум aiogram логов
    logging.getLogger("aiogram").setLevel(max(lvl, logging.INFO))
    logging.getLogger("aiogram.event").setLevel(logging.WARNING)

