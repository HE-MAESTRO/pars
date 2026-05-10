"""Telegram-Р±РѕС‚: СЃРѕСЂС‚РёСЂСѓРµС‚ СЃРѕРѕР±С‰РµРЅРёСЏ Рё С„Р°Р№Р»С‹ РїРѕ РїРѕР»СЊР·РѕРІР°С‚РµР»СЋ РІ РіСЂСѓРїРїРµ.

РљР°Рє СЂР°Р±РѕС‚Р°РµС‚:
    1. Р‘РѕС‚Р° РґРѕР±Р°РІР»СЏСЋС‚ РІ РіСЂСѓРїРїРѕРІРѕР№ С‡Р°С‚ (Рё РІС‹РґР°СЋС‚ РїСЂР°РІРѕ С‡РёС‚Р°С‚СЊ СЃРѕРѕР±С‰РµРЅРёСЏ вЂ”
       РїРѕ СѓРјРѕР»С‡Р°РЅРёСЋ Сѓ Р±РѕС‚РѕРІ РІ РіСЂСѓРїРїР°С… РІРєР»СЋС‡С‘РЅ Privacy Mode, РµРіРѕ РЅСѓР¶РЅРѕ
       РѕС‚РєР»СЋС‡РёС‚СЊ РІ @BotFather в†’ /setprivacy в†’ Disable).
    2. РќР° РєР°Р¶РґРѕРµ РЅРѕРІРѕРµ СЃРѕРѕР±С‰РµРЅРёРµ Р±РѕС‚ СЃРѕС…СЂР°РЅСЏРµС‚ РµРіРѕ РІ SQLite.
    3. РљРѕРјР°РЅРґР° /sort @username вЂ” РѕС‚РґР°С‘С‚ РІСЃРµ С‚РµРєСЃС‚РѕРІС‹Рµ СЃРѕРѕР±С‰РµРЅРёСЏ СЌС‚РѕРіРѕ
       РїРѕР»СЊР·РѕРІР°С‚РµР»СЏ СЃРїРёСЃРєРѕРј Рё РїРµСЂРµСЃС‹Р»Р°РµС‚ РµРіРѕ РјРµРґРёР°.

РљРѕРјР°РЅРґС‹:
    /start, /help   - СЃРїСЂР°РІРєР°
    /sort @user     - СЃРѕР±СЂР°С‚СЊ СЃРѕРѕР±С‰РµРЅРёСЏ Рё С„Р°Р№Р»С‹ РїРѕР»СЊР·РѕРІР°С‚РµР»СЏ
    /stats          - С‚РѕРї Р°РІС‚РѕСЂРѕРІ РІ СЌС‚РѕРј С‡Р°С‚Рµ
    /ping           - РїСЂРѕРІРµСЂРёС‚СЊ РїРёРЅРі
"""
from __future__ import annotations

import asyncio
import html
import logging
import sys
import time
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ChatType, ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, TelegramObject

import config
from storage import Storage, StoredMessage

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
log = logging.getLogger("bot")


HELP_TEXT = (
    "<b>Message Sorter Bot</b>\n\n"
    "РЎРѕС…СЂР°РЅСЏСЋ РІСЃРµ СЃРѕРѕР±С‰РµРЅРёСЏ РіСЂСѓРїРїС‹ Рё РїРѕ Р·Р°РїСЂРѕСЃСѓ РІС‹РґР°СЋ РІСЃС‘, С‡С‚Рѕ РЅР°РїРёСЃР°Р» "
    "РєРѕРЅРєСЂРµС‚РЅС‹Р№ РїРѕР»СЊР·РѕРІР°С‚РµР»СЊ, РІРєР»СЋС‡Р°СЏ С„Р°Р№Р»С‹.\n\n"
    "<b>РљРѕРјР°РЅРґС‹:</b>\n"
    "/sort @username вЂ” СЃРѕРѕР±С‰РµРЅРёСЏ Рё С„Р°Р№Р»С‹ РїРѕР»СЊР·РѕРІР°С‚РµР»СЏ\n"
    "/stats вЂ” С‚РѕРї Р°РІС‚РѕСЂРѕРІ РІ С‡Р°С‚Рµ\n"
    "/ping вЂ” РїРёРЅРі\n\n"
    "<b>РЈСЃС‚Р°РЅРѕРІРєР° РІ РіСЂСѓРїРїСѓ:</b>\n"
    "1. Р”РѕР±Р°РІСЊ РјРµРЅСЏ РІ РіСЂСѓРїРїСѓ.\n"
    "2. Р’ @BotFather в†’ /setprivacy в†’ Disable "
    "(С‡С‚РѕР±С‹ СЏ РІРёРґРµР» РІСЃРµ СЃРѕРѕР±С‰РµРЅРёСЏ, Р° РЅРµ С‚РѕР»СЊРєРѕ РєРѕРјР°РЅРґС‹).\n"
    "3. РЇ РЅР°С‡РЅСѓ СЃРѕР±РёСЂР°С‚СЊ СЃРѕРѕР±С‰РµРЅРёСЏ СЃ СЌС‚РѕРіРѕ РјРѕРјРµРЅС‚Р°."
)


# ---------- helpers ----------

MEDIA_ATTRS: tuple[tuple[str, str], ...] = (
    # (Р°С‚СЂРёР±СѓС‚ Сѓ aiogram.Message, media_type)
    ("photo", "photo"),
    ("video", "video"),
    ("document", "document"),
    ("audio", "audio"),
    ("voice", "voice"),
    ("video_note", "video_note"),
    ("animation", "animation"),
    ("sticker", "sticker"),
)


def extract_media(msg: Message) -> tuple[str | None, str | None]:
    """Р’РѕР·РІСЂР°С‰Р°РµС‚ (media_type, file_name) РёР»Рё (None, None)."""
    for attr, mtype in MEDIA_ATTRS:
        val = getattr(msg, attr, None)
        if val:
            file_name = None
            if isinstance(val, list):  # photo вЂ” СЃРїРёСЃРѕРє PhotoSize
                file_name = None
            else:
                file_name = getattr(val, "file_name", None)
            return mtype, file_name
    return None, None


def user_display_name(user) -> str:
    parts = [user.first_name or ""]
    if user.last_name:
        parts.append(user.last_name)
    name = " ".join(p for p in parts if p).strip()
    return name or (user.username or f"id{user.id}")


# ---------- command handlers ----------

async def cmd_start(message: Message) -> None:
    await message.answer(HELP_TEXT)


async def cmd_help(message: Message) -> None:
    await message.answer(HELP_TEXT)


async def cmd_sort(message: Message, storage: Storage, bot: Bot) -> None:
    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2:
        await message.reply(
            "Р¤РѕСЂРјР°С‚: <code>/sort @username</code>\n"
            "РР»Рё СЂРµРїР»Р°РµРј РЅР° СЃРѕРѕР±С‰РµРЅРёРµ РЅСѓР¶РЅРѕРіРѕ РїРѕР»СЊР·РѕРІР°С‚РµР»СЏ."
        )
        return

    username = parts[1].strip().lstrip("@")
    if not username:
        await message.reply("РќРµ РІРёР¶Сѓ username. РџСЂРёРјРµСЂ: <code>/sort @durov</code>")
        return

    chat_id = message.chat.id
    total, media = await storage.count_by_username(chat_id, username)
    if total == 0:
        await message.reply(
            f"РЈ <b>@{html.escape(username)}</b> РїРѕРєР° РЅРµС‚ СЃРѕС…СЂР°РЅС‘РЅРЅС‹С… СЃРѕРѕР±С‰РµРЅРёР№ "
            f"РІ СЌС‚РѕРј С‡Р°С‚Рµ.\n"
            f"<i>РЇ СЃРѕС…СЂР°РЅСЏСЋ С‚РѕР»СЊРєРѕ С‚Рѕ, С‡С‚Рѕ РїСЂРёС…РѕРґРёС‚ РїРѕСЃР»Рµ РґРѕР±Р°РІР»РµРЅРёСЏ РјРµРЅСЏ РІ РіСЂСѓРїРїСѓ "
            f"(Рё С‚РѕР»СЊРєРѕ СЃ РѕС‚РєР»СЋС‡С‘РЅРЅС‹Рј Privacy Mode).</i>"
        )
        return

    await message.reply(
        f"РќР°С€С‘Р» <b>{total}</b> СЃРѕРѕР±С‰РµРЅРёР№ Сѓ <b>@{html.escape(username)}</b> "
        f"(РёР· РЅРёС… СЃ РјРµРґРёР°: {media}). РћС‚РїСЂР°РІР»СЏСЋвЂ¦"
    )

    rows = await storage.get_by_username(
        chat_id, username, limit=config.SORT_LIMIT
    )

    # 1) С‚РµРєСЃС‚РѕРІС‹Рµ СЃРѕРѕР±С‰РµРЅРёСЏ РѕРґРЅРёРј Р±Р»РѕРєРѕРј (РµСЃР»Рё РёС… РЅРµРјРЅРѕРіРѕ)
    text_rows = [r for r in rows if r.text and not r.has_media]
    if text_rows:
        await _send_texts(message, text_rows)

    # 2) РјРµРґРёР° вЂ” РїРµСЂРµСЃС‹Р»РєРѕР№, С‡С‚РѕР±С‹ Telegram СЃР°Рј РїРѕРєР°Р·Р°Р» С„Р°Р№Р»
    media_rows = [r for r in rows if r.has_media]
    if media_rows:
        await _forward_media(message, bot, media_rows)

    if len(rows) == config.SORT_LIMIT < total:
        await message.answer(
            f"РџРѕРєР°Р·Р°Р» РїРµСЂРІС‹Рµ {config.SORT_LIMIT} РёР· {total}. "
            f"РЈРІРµР»РёС‡СЊ <code>SORT_LIMIT</code> РІ .env, РµСЃР»Рё РЅСѓР¶РЅРѕ Р±РѕР»СЊС€Рµ."
        )
    else:
        await message.answer("\u2705 Р“РѕС‚РѕРІРѕ.")


async def _send_texts(message: Message, rows: list[StoredMessage]) -> None:
    """РЁР»С‘С‚ С‚РµРєСЃС‚С‹ РїР°С‡РєР°РјРё, С‡С‚РѕР±С‹ СѓР»РѕР¶РёС‚СЊСЃСЏ РІ Р»РёРјРёС‚ Telegram (~4096 СЃРёРјРІРѕР»РѕРІ)."""
    chunk: list[str] = []
    chunk_len = 0
    MAX = 3500

    async def flush() -> None:
        nonlocal chunk, chunk_len
        if not chunk:
            return
        await message.answer("\n\n".join(chunk), disable_web_page_preview=True)
        chunk = []
        chunk_len = 0

    for r in rows:
        stamp = time.strftime("%d.%m %H:%M", time.localtime(r.date))
        text = html.escape(r.text or "")
        line = f"<b>[{stamp}]</b>\n{text}"
        if chunk_len + len(line) > MAX:
            await flush()
        chunk.append(line)
        chunk_len += len(line) + 2
    await flush()


async def _forward_media(
    message: Message, bot: Bot, rows: list[StoredMessage]
) -> None:
    """РџРµСЂРµСЃС‹Р»Р°РµС‚ РёСЃС…РѕРґРЅС‹Рµ СЃРѕРѕР±С‰РµРЅРёСЏ СЃ РјРµРґРёР° РёР· С‚РѕРіРѕ Р¶Рµ С‡Р°С‚Р°."""
    forwarded = 0
    failed = 0
    for r in rows:
        try:
            await bot.forward_message(
                chat_id=message.chat.id,
                from_chat_id=r.chat_id,
                message_id=r.message_id,
                disable_notification=True,
            )
            forwarded += 1
            # С‡С‚РѕР±С‹ РЅРµ СѓРїРµСЂРµС‚СЊСЃСЏ РІ flood limit Telegram
            await asyncio.sleep(0.05)
        except Exception as e:  # noqa: BLE001
            log.warning("forward_message fail for msg=%s: %s", r.message_id, e)
            failed += 1

    if failed:
        await message.answer(
            f"\u26a0\ufe0f {failed} РјРµРґРёР° РЅРµ СѓРґР°Р»РѕСЃСЊ РїРµСЂРµСЃР»Р°С‚СЊ "
            f"(РІРёРґРёРјРѕ, СѓРґР°Р»РµРЅС‹ РёР»Рё РЅРµРґРѕСЃС‚СѓРїРЅС‹).\n"
            f"РЈСЃРїРµС€РЅРѕ РїРµСЂРµСЃР»Р°РЅРѕ: {forwarded}"
        )


async def cmd_stats(message: Message, storage: Storage) -> None:
    chat_id = message.chat.id
    rows = await storage.stats(chat_id)
    if not rows:
        await message.reply("Р’ СЌС‚РѕРј С‡Р°С‚Рµ РїРѕРєР° РЅРёС‡РµРіРѕ РЅРµ СЃРѕС…СЂР°РЅРµРЅРѕ.")
        return

    lines = ["<b>РўРѕРї Р°РІС‚РѕСЂРѕРІ РІ С‡Р°С‚Рµ:</b>"]
    for i, (name, n) in enumerate(rows, 1):
        safe = html.escape(name)
        lines.append(f"{i}. <b>{safe}</b> вЂ” {n}")
    await message.reply("\n".join(lines))


async def cmd_ping(message: Message) -> None:
    t0 = time.perf_counter()
    me = await message.bot.get_me()
    api_ms = (time.perf_counter() - t0) * 1000

    t1 = time.perf_counter()
    status = await message.reply("\U0001f3d3 <b>Pong!</b>\n\u2026")
    send_ms = (time.perf_counter() - t1) * 1000

    await status.edit_text(
        "\U0001f3d3 <b>Pong!</b>\n"
        f"\U0001f4e1 Telegram API: <code>{api_ms:.0f} ms</code>\n"
        f"\U0001f4e8 Send: <code>{send_ms:.0f} ms</code>\n"
        f"\U0001f916 Р‘РѕС‚: <code>@{me.username}</code>"
    )


# ---------- message listener ----------

async def on_any_message(message: Message, storage: Storage) -> None:
    """РЎРѕС…СЂР°РЅСЏРµС‚ Р»СЋР±РѕРµ СЃРѕРѕР±С‰РµРЅРёРµ РІ РіСЂСѓРїРїРµ/СЃСѓРїРµСЂРіСЂСѓРїРїРµ."""
    if not message.from_user:
        return  # СЃРµСЂРІРёСЃРЅС‹Рµ/РєР°РЅР°Р»С‹
    if message.from_user.is_bot:
        return  # РёРіРЅРѕСЂРёСЂСѓРµРј Р±РѕС‚РѕРІ

    media_type, file_name = extract_media(message)
    text = message.text or message.caption

    # РµСЃР»Рё РЅРµС‚ РЅРё С‚РµРєСЃС‚Р°, РЅРё РјРµРґРёР° вЂ” РЅРµС‡РµРіРѕ СЃРѕС…СЂР°РЅСЏС‚СЊ
    if not text and not media_type:
        return

    try:
        await storage.save(
            chat_id=message.chat.id,
            message_id=message.message_id,
            user_id=message.from_user.id,
            username=message.from_user.username,
            full_name=user_display_name(message.from_user),
            date=int(message.date.timestamp()) if message.date else None,
            text=text,
            media_type=media_type,
            file_name=file_name,
        )
    except Exception:  # noqa: BLE001
        log.exception("РќРµ СѓРґР°Р»РѕСЃСЊ СЃРѕС…СЂР°РЅРёС‚СЊ СЃРѕРѕР±С‰РµРЅРёРµ %s", message.message_id)


# ---------- middleware / setup ----------

class StorageMiddleware(BaseMiddleware):
    def __init__(self, storage: Storage) -> None:
        self.storage = storage

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["storage"] = self.storage
        return await handler(event, data)


GROUP_TYPES = {ChatType.GROUP, ChatType.SUPERGROUP}


def register_handlers(dp: Dispatcher, storage: Storage) -> None:
    dp.message.middleware(StorageMiddleware(storage))

    # РљРѕРјР°РЅРґС‹
    dp.message.register(cmd_start, CommandStart())
    dp.message.register(cmd_help, Command("help"))
    dp.message.register(cmd_sort, Command("sort"))
    dp.message.register(cmd_stats, Command("stats"))
    dp.message.register(cmd_ping, Command("ping"))

    # РЎР»СѓС€Р°С‚РµР»СЊ РІСЃРµС… РѕСЃС‚Р°Р»СЊРЅС‹С… СЃРѕРѕР±С‰РµРЅРёР№ С‚РѕР»СЊРєРѕ РІ РіСЂСѓРїРїР°С….
    # РЎС‚Р°РІРёРј РїРѕСЃР»РµРґРЅРёРј, С‡С‚РѕР±С‹ РєРѕРјР°РЅРґС‹ СѓС€Р»Рё РІ СЃРІРѕРё С…СЌРЅРґР»РµСЂС‹ СЂР°РЅСЊС€Рµ.
    dp.message.register(
        on_any_message,
        F.chat.type.in_(GROUP_TYPES),
    )


async def main() -> None:
    storage = Storage(config.DB_PATH)

    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())
    register_handlers(dp, storage)

    me = await bot.get_me()
    log.info("Р‘РѕС‚ Р·Р°РїСѓС‰РµРЅ РєР°Рє @%s", me.username)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.info("РћСЃС‚Р°РЅРѕРІР»РµРЅРѕ")
