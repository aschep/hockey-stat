# HockeyStat 🏒 Telegram Bot

Парсит статистику игроков/команд FHR.ru → DB → Telegram

## 🚀 Quick Start
```bash
poetry install
echo BOT_TOKEN=<telegram bot token> > .env
poetry run alembic upgrade head

# Запуск парсера
poetry run parser tour <tournament name> <tournament url>

# Запуск бота
poetry run bot
```
