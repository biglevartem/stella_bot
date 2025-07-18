# Stella Tech Telegram Bot

This repository contains a sample implementation of a Telegram bot that parses products from `stella-tech.ru`, stores them in a local database and answers user questions. The bot can also be extended with AI features using OpenAI.

## Features

- Parse product catalog pages and store product information (name, article, category, link, description, image).
- Telegram bot built with [aiogram](https://docs.aiogram.dev/) that responds to product queries.
- Logs user interactions and stores interests in a SQLite database.
- Simple admin panel built with Flask to view users and trigger parsing.

## Setup

1. Create and activate a virtual environment (optional):

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and set the following variables:

```
TELEGRAM_TOKEN=your-telegram-bot-token
OPENAI_API_KEY=your-openai-key
ADMIN_IDS=123456789
```

4. Run the parser to populate the database:

```bash
python -m stella_bot.parser
```

5. Start the bot and admin panel:

```bash
python -m stella_bot.bot
python -m stella_bot.admin
```

The bot listens for product-related questions and uses the stored catalog data to recommend items.

> **Warning**: This project is provided for demonstration purposes and does not cover the full functionality described in the specification. Use at your own risk.

