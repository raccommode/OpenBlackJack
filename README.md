# OpenBlackJack

OpenBlackJack is a single-player Blackjack API built with FastAPI alongside a mobile-first web client. The default interface plays entirely in the browser, saving your bankroll locally for instant, account-free sessions while the API still exposes authentication endpoints for integrations. Automatic backups are created inside the container while the service is running.

## Features

- Casino-style 8-deck Blackjack shoe with hit, stand, double, and split actions
- Responsive web interface served from `/` and tuned for portrait play on iPhone and other mobiles
- Browser-saved bankroll with automatic persistence via local storage—no signup or connection required
- Optional authentication endpoints remain available for API clients that want server-side balance tracking
- Automatic SQLite backups created every minute
- Dockerized deployment with persistent volume for data and backups

## Getting started

1. Build and start the service:

   ```bash
   docker-compose up --build
   ```

2. The API and web client will be available at `http://localhost:3666`. Interactive documentation is provided at `http://localhost:3666/docs`.

## API overview

- `POST /signup` – Create a new account and receive an access token
- `POST /login` – Obtain a token for an existing account
- `GET /me` – Retrieve the authenticated user's profile and balance
- `POST /game/start` – Start a new Blackjack session (bets accepted for all players; authenticated users have server-side balances)
- `POST /game/hit` – Draw another card in the active session
- `POST /game/stand` – Finish the hand and resolve the bet
- `POST /game/double` – Double the stake on the active hand (requires sufficient balance when authenticated)
- `POST /game/split` – Split the active pair into two hands (requires sufficient balance when authenticated)
- `GET /game/{session_id}` – Retrieve the current state of a session
- `GET /health` – Lightweight health check

Include the `Authorization: Bearer <token>` header for authenticated endpoints. Guest sessions should omit this header.

## Data persistence and backups

Player data is stored in `data/blackjack.db` inside the container. Backups are written to `data/backups/` every 60 seconds. When using Docker Compose, these files are kept in the `blackjack_data` volume so they persist across restarts.
