"""Frontend page served by FastAPI for playing Blackjack."""
from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

INDEX_HTML = """
<!DOCTYPE html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
    <title>OpenBlackJack</title>
    <style>
      :root {
        color-scheme: light dark;
        --bg: #0b132b;
        --panel: rgba(255, 255, 255, 0.08);
        --text: #f0f4f8;
        --accent: #1c92ff;
        --accent-dark: #1474c8;
        --danger: #ff5c5c;
        --success: #60d394;
        --shadow: rgba(0, 0, 0, 0.35);
      }

      * {
        box-sizing: border-box;
      }

      body {
        margin: 0;
        font-family: \"Inter\", \"Segoe UI\", Roboto, sans-serif;
        background: linear-gradient(160deg, #000428, #004e92);
        color: var(--text);
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 1.5rem;
      }

      header {
        width: min(100%, 1100px);
        text-align: center;
        margin-bottom: 1.5rem;
      }

      h1 {
        font-size: clamp(2rem, 5vw, 3rem);
        margin-bottom: 0.25rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
      }

      p.tagline {
        margin-top: 0;
        color: rgba(240, 244, 248, 0.75);
        font-size: 1rem;
      }

      main {
        width: min(100%, 1100px);
        display: grid;
        gap: 1.25rem;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        align-items: stretch;
      }

      .card {
        background: rgba(10, 20, 40, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.25rem;
        backdrop-filter: blur(12px);
        box-shadow: 0 18px 40px var(--shadow);
        display: flex;
        flex-direction: column;
        gap: 1rem;
      }

      .card h2 {
        margin: 0;
        font-size: 1.25rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
      }

      form {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
      }

      label {
        font-size: 0.95rem;
        font-weight: 600;
        display: flex;
        flex-direction: column;
        gap: 0.35rem;
        text-align: left;
      }

      input {
        padding: 0.65rem 0.8rem;
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        background: rgba(0, 0, 0, 0.3);
        color: inherit;
        font-size: 1rem;
      }

      input:focus {
        outline: 2px solid var(--accent);
        outline-offset: 2px;
      }

      button {
        cursor: pointer;
        border: none;
        border-radius: 999px;
        padding: 0.7rem 1.2rem;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.03em;
        display: inline-flex;
        justify-content: center;
        align-items: center;
        gap: 0.4rem;
        transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease;
      }

      button.primary {
        background: linear-gradient(135deg, var(--accent), #6dd5fa);
        color: #061220;
        box-shadow: 0 8px 20px rgba(28, 146, 255, 0.35);
      }

      button.primary:hover {
        transform: translateY(-1px);
        box-shadow: 0 16px 30px rgba(28, 146, 255, 0.4);
      }

      button.secondary {
        background: rgba(255, 255, 255, 0.12);
        color: var(--text);
      }

      button.secondary:hover {
        background: rgba(255, 255, 255, 0.18);
      }

      button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
      }

      .status {
        min-height: 1.5rem;
        font-size: 0.95rem;
        font-weight: 600;
        letter-spacing: 0.03em;
      }

      .status.success {
        color: var(--success);
      }

      .status.error {
        color: var(--danger);
      }

      .status.info {
        color: rgba(240, 244, 248, 0.85);
      }

      .auth-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        justify-content: flex-start;
      }

      .balance {
        font-size: 1.1rem;
        font-weight: 600;
      }

      .session-id {
        font-family: \"Fira Code\", \"Source Code Pro\", monospace;
        font-size: 0.85rem;
        word-break: break-all;
        opacity: 0.7;
      }

      .hand {
        background: rgba(0, 0, 0, 0.25);
        border-radius: 14px;
        padding: 1rem;
        box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.05);
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
      }

      .hand h3 {
        margin: 0;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        font-size: 1rem;
      }

      .card-tiles {
        display: flex;
        gap: 0.65rem;
        flex-wrap: wrap;
      }

      .card-tile {
        background: rgba(255, 255, 255, 0.12);
        border-radius: 12px;
        padding: 0.75rem 0.9rem;
        min-width: 4.8rem;
        text-align: center;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
      }

      .card-tile span {
        display: block;
      }

      .card-tile .rank {
        font-size: 1.15rem;
        font-weight: 700;
      }

      .card-tile .suit {
        font-size: 0.85rem;
        opacity: 0.8;
      }

      .hand-total {
        font-size: 0.9rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        opacity: 0.85;
      }

      .game-controls {
        display: flex;
        flex-direction: column;
        gap: 1rem;
      }

      .action-buttons {
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
      }

      .outcome {
        font-weight: 700;
        font-size: 1.05rem;
      }

      .muted {
        opacity: 0.65;
        font-size: 0.9rem;
      }

      footer {
        margin-top: auto;
        padding: 1rem 0 0;
        text-align: center;
        color: rgba(240, 244, 248, 0.55);
        font-size: 0.85rem;
      }

      @media (max-width: 900px) {
        main {
          grid-template-columns: 1fr;
        }
      }

      @media (max-width: 540px) {
        body {
          padding: 1rem;
        }

        .card {
          padding: 1rem;
        }

        .action-buttons {
          flex-direction: column;
        }

        button {
          width: 100%;
        }
      }
    </style>
  </head>
  <body>
    <header>
      <h1>OpenBlackJack</h1>
      <p class=\"tagline\">Single-player Blackjack with optional accounts and instant play.</p>
    </header>
    <main>
      <section class=\"card\>
        <h2>Account</h2>
        <div class=\"status info\" id=\"status\"></div>
        <div class=\"balance\" id=\"balance-area\">Guest mode — betting disabled.</div>
        <div class=\"session-id\" id=\"session-info\"></div>
        <form id=\"signup-form\">
          <h3>Sign up</h3>
          <label>
            Username
            <input id=\"signup-username\" name=\"username\" minlength=\"3\" maxlength=\"30\" required />
          </label>
          <label>
            Password
            <input id=\"signup-password\" name=\"password\" type=\"password\" minlength=\"6\" required />
          </label>
          <button class=\"primary\" type=\"submit\">Create account</button>
          <p class=\"muted\">New accounts start with a $1000 balance.</p>
        </form>
        <form id=\"login-form\">
          <h3>Log in</h3>
          <label>
            Username
            <input id=\"login-username\" name=\"username\" required />
          </label>
          <label>
            Password
            <input id=\"login-password\" name=\"password\" type=\"password\" required />
          </label>
          <button class=\"primary\" type=\"submit\">Log in</button>
        </form>
        <div class=\"auth-actions\">
          <button class=\"secondary\" type=\"button\" id=\"guest-button\">Continue as guest</button>
          <button class=\"secondary\" type=\"button\" id=\"logout-button\" disabled>Log out</button>
        </div>
      </section>
      <section class=\"card\">
        <h2>Game table</h2>
        <div class=\"game-controls\">
          <form id=\"start-form\">
            <label>
              Bet amount (USD)
              <input id=\"bet-input\" name=\"bet\" type=\"number\" min=\"0\" step=\"50\" value=\"0\" />
            </label>
            <button class=\"primary\" type=\"submit\">Deal a new hand</button>
          </form>
          <div class=\"action-buttons\">
            <button class=\"secondary\" type=\"button\" id=\"hit-button\" disabled>Hit</button>
            <button class=\"secondary\" type=\"button\" id=\"stand-button\" disabled>Stand</button>
          </div>
          <div class=\"outcome\" id=\"outcome\">Start a hand to begin playing.</div>
          <div class=\"hand\" id=\"player-hand\">
            <h3>Player</h3>
            <div class=\"card-tiles\"></div>
            <div class=\"hand-total\"></div>
          </div>
          <div class=\"hand\" id=\"dealer-hand\">
            <h3>Dealer</h3>
            <div class=\"card-tiles\"></div>
            <div class=\"hand-total\"></div>
          </div>
        </div>
      </section>
    </main>
    <footer>API available at <code>/docs</code> for integrations.</footer>
    <script>
      const statusEl = document.getElementById('status');
      const balanceEl = document.getElementById('balance-area');
      const sessionInfoEl = document.getElementById('session-info');
      const outcomeEl = document.getElementById('outcome');
      const playerHandEl = document.getElementById('player-hand');
      const dealerHandEl = document.getElementById('dealer-hand');
      const betInput = document.getElementById('bet-input');
      const hitButton = document.getElementById('hit-button');
      const standButton = document.getElementById('stand-button');
      const logoutButton = document.getElementById('logout-button');

      let token = null;
      let profile = null;
      let sessionId = null;

      function setStatus(message, tone = 'info') {
        statusEl.textContent = message;
        statusEl.className = `status ${tone}`;
      }

      function authHeaders() {
        return token ? { Authorization: `Bearer ${token}` } : {};
      }

      function updateAuthUI() {
        if (profile) {
          balanceEl.textContent = `Logged in as ${profile.username} — Balance: $${profile.balance}`;
          logoutButton.disabled = false;
          betInput.disabled = false;
        } else {
          balanceEl.textContent = 'Guest mode — betting disabled.';
          logoutButton.disabled = true;
          betInput.value = '0';
          betInput.disabled = true;
        }
      }

      function formatOutcome(outcome, isOver) {
        if (!outcome) {
          return isOver ? 'Hand complete.' : 'Hand in progress — take your action!';
        }
        const mapping = {
          player_blackjack: 'Blackjack! You win 3:2.',
          player_win: 'You win!',
          dealer_bust: 'Dealer busts — you win!',
          dealer_blackjack: 'Dealer has blackjack.',
          dealer_win: 'Dealer wins.',
          player_bust: 'Bust! Dealer wins.',
          push: 'Push — it\'s a tie.',
        };
        return mapping[outcome] || outcome.replace('_', ' ');
      }

      function renderHand(element, hand) {
        const tiles = hand.cards
          .map((card) => `
            <div class=\"card-tile\">
              <span class=\"rank\">${card.rank}</span>
              <span class=\"suit\">${card.suit}</span>
            </div>
          `)
          .join('');
        element.querySelector('.card-tiles').innerHTML = tiles || '<p class=\"muted\">Waiting for deal…</p>';
        element.querySelector('.hand-total').textContent = hand.cards.length ? `Total: ${hand.value}` : '';
      }

      function handleGameState(data) {
        sessionId = data.session_id;
        sessionInfoEl.textContent = `Session: ${sessionId}`;
        renderHand(playerHandEl, data.player_hand);
        renderHand(dealerHandEl, data.dealer_hand);
        outcomeEl.textContent = formatOutcome(data.outcome, data.is_over);
        if (typeof data.balance === 'number' && profile) {
          profile.balance = data.balance;
          updateAuthUI();
        }
        const actionEnabled = !data.is_over;
        hitButton.disabled = !actionEnabled;
        standButton.disabled = !actionEnabled;
        return data;
      }

      async function postJson(path, body, headers = {}) {
        const response = await fetch(path, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', ...authHeaders(), ...headers },
          body: JSON.stringify(body),
        });
        if (!response.ok) {
          let message = 'Request failed.';
          try {
            const payload = await response.json();
            message = payload.detail || JSON.stringify(payload);
          } catch (err) {
            message = response.statusText;
          }
          throw new Error(message);
        }
        return response.json();
      }

      async function fetchProfile() {
        if (!token) {
          profile = null;
          updateAuthUI();
          return;
        }
        try {
          const response = await fetch('/me', { headers: { ...authHeaders() } });
          if (!response.ok) {
            throw new Error('Unable to fetch profile.');
          }
          profile = await response.json();
          updateAuthUI();
          setStatus('Logged in successfully.', 'success');
        } catch (error) {
          token = null;
          profile = null;
          updateAuthUI();
          setStatus(error.message, 'error');
        }
      }

      document.getElementById('signup-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const username = document.getElementById('signup-username').value.trim();
        const password = document.getElementById('signup-password').value.trim();
        if (!username || !password) {
          setStatus('Please provide a username and password.', 'error');
          return;
        }
        try {
          const data = await postJson('/signup', { username, password });
          token = data.token;
          await fetchProfile();
          setStatus('Account created! A new hand awaits.', 'success');
        } catch (error) {
          setStatus(error.message, 'error');
        }
      });

      document.getElementById('login-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const username = document.getElementById('login-username').value.trim();
        const password = document.getElementById('login-password').value.trim();
        if (!username || !password) {
          setStatus('Enter username and password to log in.', 'error');
          return;
        }
        try {
          const data = await postJson('/login', { username, password });
          token = data.token;
          await fetchProfile();
          setStatus('Logged in. Ready to wager!', 'success');
        } catch (error) {
          setStatus(error.message, 'error');
        }
      });

      document.getElementById('guest-button').addEventListener('click', () => {
        token = null;
        profile = null;
        updateAuthUI();
        setStatus('Guest mode activated. Bets are disabled, but play on!', 'info');
      });

      logoutButton.addEventListener('click', () => {
        token = null;
        profile = null;
        updateAuthUI();
        setStatus('You have logged out.', 'info');
      });

      document.getElementById('start-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const bet = parseInt(betInput.value, 10) || 0;
        if (!profile && bet > 0) {
          setStatus('Guests must leave the bet at $0.', 'error');
          return;
        }
        try {
          const data = await postJson('/game/start', { bet });
          handleGameState(data);
          setStatus('Hand dealt — good luck!', 'success');
        } catch (error) {
          setStatus(error.message, 'error');
        }
      });

      hitButton.addEventListener('click', async () => {
        if (!sessionId) {
          setStatus('Start a hand first.', 'error');
          return;
        }
        try {
          const data = await postJson('/game/hit', { session_id: sessionId });
          handleGameState(data);
          setStatus('Card drawn.', 'info');
        } catch (error) {
          setStatus(error.message, 'error');
        }
      });

      standButton.addEventListener('click', async () => {
        if (!sessionId) {
          setStatus('Start a hand first.', 'error');
          return;
        }
        try {
          const data = await postJson('/game/stand', { session_id: sessionId });
          handleGameState(data);
          setStatus('Hand resolved.', 'info');
        } catch (error) {
          setStatus(error.message, 'error');
        }
      });

      updateAuthUI();
      setStatus('Play as a guest or sign in to start betting.');
    </script>
  </body>
</html>
"""


@router.get("/", response_class=HTMLResponse)
def index() -> str:
    """Serve the responsive Blackjack frontend."""
    return INDEX_HTML
