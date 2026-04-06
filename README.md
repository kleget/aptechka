# Aptechka Bot

## Setup

1. Создайте виртуальное окружение.
2. Установите зависимости: `pip install -r requirements.txt`
3. Скопируйте `.env.example` в `.env` или задайте те же переменные окружения другим способом.
4. Запустите `python main.py`

## Required Environment Variables

- `TELEGRAM_BOT_TOKEN`
- `BOT_ADMIN_ID`
- `YOOMONEY_TOKEN`
- `YOOMONEY_RECEIVER`
- `YOOMONEY_CLIENT_ID`
- `YOOMONEY_REDIRECT_URI`
- `AUDIO_ONE_FILE_ID`
- `AUDIO_TWO_FILE_ID`
- `AUDIO_THREE_FILE_ID`
- `AUDIO_FOUR_FILE_ID`
- `AUDIO_FIVE_FILE_ID`

Локальные базы `db_main.db` и `ras.db` создаются автоматически при первом запуске и не должны попадать в git.
