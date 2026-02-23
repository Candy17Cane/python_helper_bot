from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value is not None else default

def _env_bool(name: str, default: bool = False) ->  bool:
    raw = (_env(name, "1" if default else "0") or "").strip().lower()
    return raw in {"1", "true", "yes", "y", "on"}

def _env_int_list(name: str, default: str = "") -> list[int]:
    raw = (_env(name, default) or "").strip()
    if not raw:
        return []
    out: list[int] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            out.append(int(part))
        except ValueError:
            continue
    return out

@dataclass(frozen=True)
class Settings:
    bot_token: str
    env: str = "dev"
    log_level: str = "INFO"
    parse_mode: str = "HTML"
    db_path: str = "bot.db"
    admin_ids: list[int] = None
    use_webhook: bool = False

    @staticmethod
    def load() -> "Settings":
        token = _env("BOT_TOKEN")
        if not token:
            raise RuntimeError("BOT_TOKEN is missing in .env")
        
        env = (_env("ENV", "dev") or "dev").strip().lower()
        log_level = (_env("LOG_LEVEL", "INFO") or "INFO").strip().upper()
        parse_mode = (_env("PARSE_MODE", "HTML") or "HTML").strip().upper()
        db_path = (_env("DB_PATH", "bot.db") or "bot.db").strip()
        
        return Settings(
            bot_token=token,
            env=env,
            log_level=log_level,
            parse_mode=parse_mode,
            db_path=db_path,
            admin_ids=_env_int_list("ADMIN_IDS", ""),
            use_webhook=_env_bool("USE_WEBHOOK", False),
        )
    
