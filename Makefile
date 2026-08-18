setup:
	uv sync
	test -f .env || cp .env.example .env

start:
	uv run bot.py

test:
	uv run pytest