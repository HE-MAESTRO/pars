# pars

Парсер пользовательских имён из платформы Fragment.

Собирает и анализирует данные об участниках/пользователях с возможность извлечения стоимости.

## Стек

Python · aiogram 3 · SQLite

## Структура

```
pars/
├── bot.py          — основная логика парсинга
├── storage.py      — работа с SQLite
├── config.py       — загрузка переменных окружения
├── messages.db     — база данных
├── .env.example   — пример конфига
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

Копируем `.env.example` → `.env`, заполняем токены.

## Запуск

```powershell
python bot.py
```

---

[GitHub](https://github.com/HE-MAESTRO) · [Telegram](https://t.me/HE_MAESTRO)
