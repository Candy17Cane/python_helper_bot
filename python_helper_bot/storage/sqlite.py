from __future__ import annotations
import sqlite3
from storage.base import Storage

class SQLiteStorage(Storage):
    def __init__(self, db_path: str = "bot.db") -> None:
        self.db_path = db_path
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreing_keys = ON;")
        return conn
    
    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS favorites (
                    user_id         INTEGER NOT NULL,
                    section_key     TEXT    NOT NULL,
                    topic_key       TEXT    NOT NULL,
                    created_at      TEXT    NOT NULL DEFAULT (datetime('now')),
                    PRIMARY KEY(user_id, section_key, topic_key)                   
                );
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_fav_user ON favorites(user_id);")

    def add_favorite(self, user_id: int, section_key: str, topic_key: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO favorites(user_id, section_key, topic_key) VALUES (?, ?, ?)",
                (user_id, section_key, topic_key),
            )

    def remove_favorite(self, user_id: int, section_key: str, topic_key: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "DELETE FROM favorites WHERE user_id = ? AND section_key = ? AND topic_key =?",
                (user_id, section_key, topic_key),
            )

    def is_favorite(self, user_id: int, section_key: str, topic_key: str) -> bool:
        with self._connect() as conn:
            cur = conn.execute(
                "SELECT 1 FROM favorites WHERE user_id = ? AND section_key = ? AND topic_key = ? LIMIT 1",
                (user_id, section_key, topic_key),
            )
            return cur.fetchone() is not None
        
    def list_favorites(self, user_id: int) -> list[tuple[str, str]]:
        with self._connect() as conn:
            cur = conn.execute(
                "SELECT section_key, topic_key FROM favorites WHERE user_id = ? ORDER BY created_at DESC",
                (user_id,),
            )
            return [(r[0], r[1]) for r in cur.fetchall()]
        
