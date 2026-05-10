
# pars

Parser pol'zovatel'skih imen iz platformy Fragment.

Sobiraet i analiziruet dannye ob uchastnikah s vozmozhnost'yu izvlecheniya stoimosti.

## Stek

Python · aiogram 3 · SQLite

## Struktura

`
pars/
├── bot.py          — osnovnaya logika parsinga
├── storage.py      — rabota s SQLite
├── config.py       — zagruzka peremennyh okruzheniya
├── messages.db     — baza dannyh
├── .env.example   — primer konfiga
└── requirements.txt
`

## Ustanovka

\\\powershell
git clone https://github.com/HE-MAESTRO/pars.git
cd pars
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
\\\

Kopiruem .env.example → .env, zapalnyaem tokeny.

## Zapusk

\\\powershell
python bot.py
\\\

---

[GitHub](https://github.com/HE-MAESTRO) · [Telegram](https://t.me/HE_MAESTRO)