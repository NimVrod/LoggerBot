![Discord Bots](https://top.gg/api/widget/1271203231888052354.svg)

A bot made using discord.py

Installation
======
Install dependencies with uv:

`uv sync`

Add a `.env` file with `TOKEN` field containg your discord bot token

Run:

`uv run python main.py`

Docker
======
Build:

`docker build -t loggerbot .`

Run:

`docker run --rm --env-file .env loggerbot`

Features
=========
- Voicelogs
- Chatlogs
- Auditlogs
- Joinlogs
