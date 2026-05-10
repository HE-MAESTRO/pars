"""Р—Р°РіСЂСѓР·РєР° РєРѕРЅС„РёРіСѓСЂР°С†РёРё РёР· .env."""
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
DB_PATH = os.getenv("DB_PATH", "messages.db").strip()
SORT_LIMIT = int(os.getenv("SORT_LIMIT", "50"))

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN РЅРµ Р·Р°РґР°РЅ РІ .env")
