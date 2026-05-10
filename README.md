# pars

Telegram-бот для поиска красивых юзернеймов на платформе Fragment.

## Что делает

Ищет и фильтрует доступные юзернеймы по заданным критериям — длина, наличие цифр, паттерны, стоимость. Помогает найти имена которые можно перенести на Telegram.

## Стек

Python · aiogram 3 · SQLite

## Структура

```
pars/
├── bot.py          — основная логика
├── storage.py     — SQLite
├── config.py      — .env
├── messages.db    — база
├── .env.example
└── requirements.txt
```

## Установка

```powershell
git clone https://github.com/HE-MAESTRO/pars.git
cd pars
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Копируем `.env.example` → `.env`, вставляем токен бота от [@BotFather](https://t.me/BotFather).

## Запуск

```powershell
python bot.py
```

---

[GitHub](https://github.com/HE-MAESTRO) · [Telegram](https://t.me/HE_MAESTRO)
