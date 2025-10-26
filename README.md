# OpenBlackJack

OpenBlackJack is a single-player Blackjack API built with FastAPI. It supports guest games, account creation with automatic $1000 credit, and persistent balances backed by SQLite. Automatic backups are created inside the container while the service is running.

## Features

- Standard 52-card Blackjack simulation with hit and stand actions
- Optional authentication with username and password (no email required)
- Automatic $1000 credit on signup and balance tracking for authenticated users
- Guest games without signup or login
- Automatic SQLite backups created every minute
- Dockerized deployment with persistent volume for data and backups

## Getting started

1. Build and start the service:

   ```bash
   docker-compose up --build
   ```

2. The API will be available at `http://localhost:8000`. Interactive documentation is provided at `http://localhost:8000/docs`.

## API overview

- `POST /signup` – Create a new account and receive an access token
- `POST /login` – Obtain a token for an existing account
- `GET /me` – Retrieve the authenticated user's profile and balance
- `POST /game/start` – Start a new Blackjack session (optional bet when authenticated)
- `POST /game/hit` – Draw another card in the active session
- `POST /game/stand` – Finish the hand and resolve the bet
- `GET /game/{session_id}` – Retrieve the current state of a session
- `GET /health` – Lightweight health check

Include the `Authorization: Bearer <token>` header for authenticated endpoints. Guest sessions should omit this header.

## Data persistence and backups

Player data is stored in `data/blackjack.db` inside the container. Backups are written to `data/backups/` every 60 seconds. When using Docker Compose, these files are kept in the `blackjack_data` volume so they persist across restarts.
