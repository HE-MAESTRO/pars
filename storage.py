"""SQLite-С…СЂР°РЅРёР»РёС‰Рµ РґР»СЏ СЃРѕРѕР±С‰РµРЅРёР№ РіСЂСѓРїРїС‹.

РўР°Р±Р»РёС†С‹:
    messages вЂ” РїРѕ РѕРґРЅРѕР№ СЃС‚СЂРѕРєРµ РЅР° РєР°Р¶РґРѕРµ СЃРѕС…СЂР°РЅС‘РЅРЅРѕРµ СЃРѕРѕР±С‰РµРЅРёРµ

РЎС…РµРјР°:
    id              INTEGER PRIMARY KEY AUTOINCREMENT
    chat_id         INTEGER  вЂ” id РіСЂСѓРїРїС‹
    message_id      INTEGER  вЂ” message_id РІ СЌС‚РѕР№ РіСЂСѓРїРїРµ
    user_id         INTEGER  вЂ” id Р°РІС‚РѕСЂР°
    username        TEXT     вЂ” @username (lower), Р±РµР· @; NULL РµСЃР»Рё РЅРµС‚
    full_name       TEXT     вЂ” РёРјСЏ РґР»СЏ РѕС‚РѕР±СЂР°Р¶РµРЅРёСЏ
    date            INTEGER  вЂ” unix timestamp
    text            TEXT     вЂ” С‚РµРєСЃС‚ РёР»Рё caption
    media_type      TEXT     вЂ” NULL | 'photo' | 'video' | 'document' | 'audio'
                               | 'voice' | 'video_note' | 'animation' | 'sticker'
    file_name       TEXT     вЂ” РёРјСЏ С„Р°Р№Р»Р° (РµСЃР»Рё РµСЃС‚СЊ)

UNIQUE(chat_id, message_id) вЂ” Р·Р°С‰РёС‚Р° РѕС‚ РґСѓР±Р»РёРєР°С‚РѕРІ.
"""
from __future__ import annotations

import asyncio
import sqlite3
import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class StoredMessage:
    id: int
    chat_id: int
    message_id: int
    user_id: int
    username: str | None
    full_name: str
    date: int
    text: str | None
    media_type: str | None
    file_name: str | None

    @property
    def has_media(self) -> bool:
        return self.media_type is not None


class Storage:
    """РџСЂРѕСЃС‚РѕР№ thread-safe-РѕР±С‘СЂС‚РєР° РЅР°Рґ sqlite3 СЃ async-С„Р°СЃР°РґРѕРј."""

    def __init__(self, path: str) -> None:
        self._path = path
        self._lock = asyncio.Lock()
        self._init_db()

    # ---------- low-level ----------

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self._path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _init_db(self) -> None:
        with self._conn() as c:
            c.executescript(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id     INTEGER NOT NULL,
                    message_id  INTEGER NOT NULL,
                    user_id     INTEGER NOT NULL,
                    username    TEXT,
                    full_name   TEXT NOT NULL,
                    date        INTEGER NOT NULL,
                    text        TEXT,
                    media_type  TEXT,
                    file_name   TEXT,
                    UNIQUE(chat_id, message_id)
                );
                CREATE INDEX IF NOT EXISTS idx_chat_username
                    ON messages(chat_id, username);
                CREATE INDEX IF NOT EXISTS idx_chat_user
                    ON messages(chat_id, user_id);
                """
            )

    # ---------- async API ----------

    async def save(
        self,
        *,
        chat_id: int,
        message_id: int,
        user_id: int,
        username: str | None,
        full_name: str,
        date: int | None = None,
        text: str | None = None,
        media_type: str | None = None,
        file_name: str | None = None,
    ) -> None:
        """РЎРѕС…СЂР°РЅРёС‚СЊ СЃРѕРѕР±С‰РµРЅРёРµ. Р”СѓР±Р»РёРєР°С‚С‹ РёРіРЅРѕСЂРёСЂСѓСЋС‚СЃСЏ."""
        date = date or int(time.time())
        username_norm = username.lower() if username else None

        def _do() -> None:
            with self._conn() as c:
                c.execute(
                    """
                    INSERT OR IGNORE INTO messages
                    (chat_id, message_id, user_id, username, full_name,
                     date, text, media_type, file_name)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (chat_id, message_id, user_id, username_norm, full_name,
                     date, text, media_type, file_name),
                )

        async with self._lock:
            await asyncio.to_thread(_do)

    async def get_by_username(
        self,
        chat_id: int,
        username: str,
        *,
        limit: int = 50,
        only_media: bool = False,
    ) -> list[StoredMessage]:
        username_norm = username.lstrip("@").lower()

        def _do() -> list[StoredMessage]:
            q = (
                "SELECT * FROM messages "
                "WHERE chat_id = ? AND username = ?"
            )
            params: list = [chat_id, username_norm]
            if only_media:
                q += " AND media_type IS NOT NULL"
            q += " ORDER BY date ASC LIMIT ?"
            params.append(limit)

            with self._conn() as c:
                rows = c.execute(q, params).fetchall()
                return [StoredMessage(**dict(r)) for r in rows]

        async with self._lock:
            return await asyncio.to_thread(_do)

    async def count_by_username(
        self, chat_id: int, username: str
    ) -> tuple[int, int]:
        """Р’РѕР·РІСЂР°С‰Р°РµС‚ (РІСЃРµРіРѕ СЃРѕРѕР±С‰РµРЅРёР№, РёР· РЅРёС… СЃ РјРµРґРёР°)."""
        username_norm = username.lstrip("@").lower()

        def _do() -> tuple[int, int]:
            with self._conn() as c:
                total = c.execute(
                    "SELECT COUNT(*) FROM messages WHERE chat_id=? AND username=?",
                    (chat_id, username_norm),
                ).fetchone()[0]
                media = c.execute(
                    "SELECT COUNT(*) FROM messages "
                    "WHERE chat_id=? AND username=? AND media_type IS NOT NULL",
                    (chat_id, username_norm),
                ).fetchone()[0]
                return total, media

        async with self._lock:
            return await asyncio.to_thread(_do)

    async def stats(self, chat_id: int) -> list[tuple[str, int]]:
        """РўРѕРї РїРѕР»СЊР·РѕРІР°С‚РµР»РµР№ С‡Р°С‚Р° РїРѕ РєРѕР»РёС‡РµСЃС‚РІСѓ СЃРѕРѕР±С‰РµРЅРёР№."""
        def _do() -> list[tuple[str, int]]:
            with self._conn() as c:
                rows = c.execute(
                    "SELECT COALESCE(username, full_name) AS name, COUNT(*) AS n "
                    "FROM messages WHERE chat_id=? "
                    "GROUP BY user_id ORDER BY n DESC LIMIT 10",
                    (chat_id,),
                ).fetchall()
                return [(r["name"], r["n"]) for r in rows]

        async with self._lock:
            return await asyncio.to_thread(_do)
