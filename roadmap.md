🏒 ХОККЕЙНЫЙ BOT: Парсинг pfo.fhr.ru → БД → Telegram
═══════════════════════════════════════════════════════════════

📁 СТРУКТУРА ПРОЕКТА

    hockeybot/
        ├── pyproject.toml        
        ├── README.md        
        ├── conftest.py
        ├── hockeybot/
        │   ├── core/            
        │   │   ├── models.py    
        │   │   └── enums.py
        │   ├── parsers/         
        │   │   ├── player.py    
        │   │   ├── team.py
        │   ├── storage/
        │   │   ├── database.py
        │   │   ├── models.py
        │   │   └── repository.py
        │   └── bot/             
        │       ├── handlers.py  
        │       └── main.py
        ├── tests/
        │   └── data/
        └── migrations/

🚀 МVP (5 ДНЕЙ)

День 1: Poetry + Models + SQLite

День 2-3: TeamParser + TournamentParser  

День 4: Telegram Bot (/player /team /top)

День 5: Тесты + Docker + Railway


📦 DEPENDENCIES

poetry add requests bs4 python-telegram-bot sqlalchemy alembic

poetry add -G dev pytest pytest-mock pytest-asyncio pytest-cov 


🤖 КОМАНДЫ БОТА (MVP)

✅ /player <url>     # Парсинг игрока + сохранение

✅ /team <url>       # Топ-10 игроков команды

✅ /top_players      # Лидеры по очкам сезона

✅ /search <name>    # Поиск игроков


🗄️ БД СХЕМА

players: id, name, position, height, weight, grip, school, player_id

teams: id, name, tournament_id, team_id

player_stats: player_id, game_id, goals, assists, +/-, pim

─────────────────────────────────────────────────────────

СТАРТ: poetry new --src hockeybot && poetry install --with dev

═══════════════════════════════════════════════════════════════
