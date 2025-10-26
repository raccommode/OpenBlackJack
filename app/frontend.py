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
        color-scheme: dark;
        --bg: #020617;
        --bg-secondary: #052527;
        --panel: rgba(6, 15, 32, 0.85);
        --panel-border: rgba(148, 163, 184, 0.18);
        --text-primary: #f8fafc;
        --text-muted: rgba(226, 232, 240, 0.75);
        --accent: #22d3ee;
        --accent-strong: #0ea5e9;
        --success: #34d399;
        --danger: #f87171;
        --warning: #fbbf24;
        --win: #4ade80;
        --loss: #f87171;
        --push: #facc15;
        --shadow: rgba(7, 11, 27, 0.6);
      }

      * {
        box-sizing: border-box;
      }

      body {
        margin: 0;
        font-family: \"Inter\", \"Segoe UI\", system-ui, -apple-system, sans-serif;
        background: radial-gradient(circle at 20% 20%, rgba(14, 116, 144, 0.25), transparent 55%),
          radial-gradient(circle at 80% 0%, rgba(17, 94, 89, 0.3), transparent 40%),
          linear-gradient(160deg, #001219 0%, #020617 45%, #010409 100%);
        color: var(--text-primary);
        min-height: 100vh;
      }

      .app-shell {
        width: min(1150px, 100%);
        margin: 0 auto;
        padding: 1.5rem clamp(1rem, 4vw, 2.5rem) 2.5rem;
        display: flex;
        flex-direction: column;
        gap: 1.75rem;
        min-height: 100vh;
      }

      .app-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        flex-wrap: wrap;
        gap: 1rem 2rem;
      }

      h1 {
        margin: 0;
        font-size: clamp(2rem, 6vw, 3.1rem);
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

      .tagline {
        margin: 0.4rem 0 0;
        color: var(--text-muted);
        font-size: clamp(0.95rem, 2.5vw, 1.05rem);
      }

      .status-badge {
        padding: 0.85rem 1.4rem;
        border-radius: 999px;
        border: 1px solid rgba(148, 163, 184, 0.3);
        background: rgba(14, 116, 144, 0.12);
        font-size: 0.95rem;
        letter-spacing: 0.02em;
        transition: background 0.2s ease, border 0.2s ease, color 0.2s ease;
      }

      .status--info {
        color: var(--accent);
        background: rgba(34, 211, 238, 0.12);
        border-color: rgba(34, 211, 238, 0.35);
      }

      .status--success {
        color: var(--success);
        background: rgba(52, 211, 153, 0.12);
        border-color: rgba(52, 211, 153, 0.35);
      }

      .status--error {
        color: var(--danger);
        background: rgba(248, 113, 113, 0.12);
        border-color: rgba(248, 113, 113, 0.35);
      }

      .status--warning {
        color: var(--warning);
        background: rgba(251, 191, 36, 0.12);
        border-color: rgba(251, 191, 36, 0.35);
      }

      main.layout {
        display: grid;
        grid-template-columns: minmax(0, 340px) minmax(0, 1fr);
        gap: 1.5rem;
        align-items: stretch;
      }

      .panel {
        background: var(--panel);
        border-radius: 22px;
        border: 1px solid var(--panel-border);
        padding: clamp(1.25rem, 3vw, 1.75rem);
        backdrop-filter: blur(18px);
        box-shadow: 0 30px 70px var(--shadow);
        display: flex;
        flex-direction: column;
        gap: 1.4rem;
      }

      .panel h2 {
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 1.1rem;
      }

      .panel--auth .panel-section {
        display: flex;
        flex-direction: column;
        gap: 1rem;
      }

      .panel--auth .forms {
        gap: 1.25rem;
      }

      .balance {
        font-weight: 600;
        font-size: 1.05rem;
      }

      .session-id {
        font-family: \"Fira Code\", \"Source Code Pro\", monospace;
        font-size: 0.85rem;
        letter-spacing: 0.03em;
        color: var(--text-muted);
      }

      .session-id span {
        color: var(--accent);
      }

      form {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
      }

      .form-card {
        padding: 1rem;
        border-radius: 16px;
        background: rgba(15, 23, 42, 0.4);
        border: 1px solid rgba(148, 163, 184, 0.12);
      }

      .form-card h3 {
        margin: 0;
        font-size: 1.05rem;
      }

      label {
        font-size: 0.9rem;
        font-weight: 600;
        display: flex;
        flex-direction: column;
        gap: 0.35rem;
      }

      input {
        padding: 0.65rem 0.8rem;
        border-radius: 10px;
        border: 1px solid rgba(148, 163, 184, 0.35);
        background: rgba(2, 6, 23, 0.35);
        color: inherit;
        font-size: 1rem;
        transition: border 0.2s ease, box-shadow 0.2s ease;
      }

      input:focus {
        outline: none;
        border-color: var(--accent);
        box-shadow: 0 0 0 3px rgba(34, 211, 238, 0.25);
      }

      button {
        cursor: pointer;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.2rem;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.03em;
        display: inline-flex;
        justify-content: center;
        align-items: center;
        gap: 0.45rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease, opacity 0.2s ease;
      }

      button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
      }

      button.primary {
        background: linear-gradient(135deg, var(--accent), var(--accent-strong));
        color: #001219;
        box-shadow: 0 12px 30px rgba(14, 165, 233, 0.35);
      }

      button.primary:hover:not(:disabled) {
        transform: translateY(-1px);
        box-shadow: 0 16px 36px rgba(34, 211, 238, 0.4);
      }

      button.secondary {
        background: rgba(15, 23, 42, 0.45);
        color: var(--text-primary);
        border: 1px solid rgba(148, 163, 184, 0.18);
      }

      button.secondary:hover:not(:disabled) {
        background: rgba(15, 23, 42, 0.65);
      }

      .auth-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 0.65rem;
      }

      .muted {
        color: var(--text-muted);
        font-size: 0.85rem;
      }

      .panel--table {
        gap: 1.5rem;
      }

      .table-surface {
        background: radial-gradient(circle, rgba(6, 78, 59, 0.6) 0%, rgba(2, 44, 34, 0.55) 55%, rgba(1, 22, 39, 0.65) 100%);
        border-radius: 22px;
        padding: clamp(1.25rem, 4vw, 2rem);
        border: 1px solid rgba(148, 163, 184, 0.18);
        position: relative;
        overflow: hidden;
      }

      .table-surface::before {
        content: \"\";
        position: absolute;
        inset: 0;
        background: radial-gradient(circle at 50% 0%, rgba(34, 211, 238, 0.15), transparent 55%);
        pointer-events: none;
      }

      .table-row {
        display: flex;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
      }

      .hand-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.9rem;
        padding: 0.75rem;
        text-align: center;
      }

      .hand-wrapper h3 {
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-size: 0.95rem;
      }

      .card-tiles {
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
        justify-content: center;
        min-height: 110px;
      }

      .card-tile {
        position: relative;
        width: 72px;
        height: 104px;
        border-radius: 14px;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border: 1px solid rgba(15, 23, 42, 0.15);
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.4);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        color: #0f172a;
        overflow: hidden;
      }

      .card-tile.red {
        color: #dc2626;
      }

      .card-tile.black {
        color: #0f172a;
      }

      .card-tile .corner {
        position: absolute;
        font-size: 0.72rem;
        font-weight: 600;
      }

      .card-tile .corner--top {
        top: 8px;
        left: 8px;
      }

      .card-tile .corner--bottom {
        bottom: 8px;
        right: 8px;
        transform: rotate(180deg);
      }

      .card-tile .symbol {
        font-size: 2.15rem;
        line-height: 1;
      }

      .card-tile .rank {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        opacity: 0.65;
      }

      .card-back {
        background: repeating-linear-gradient(45deg, rgba(2, 44, 34, 0.85), rgba(2, 44, 34, 0.85) 8px, rgba(15, 118, 110, 0.85) 8px, rgba(15, 118, 110, 0.85) 16px);
        border: 1px solid rgba(34, 211, 238, 0.4);
      }

      .card-back::after {
        content: \"\";
        position: absolute;
        inset: 12px;
        border-radius: 10px;
        border: 1px dashed rgba(226, 232, 240, 0.35);
      }

      .hand-total {
        font-size: 0.9rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: rgba(226, 232, 240, 0.9);
      }

      .hand-wrapper.hand--concealed .hand-total {
        color: rgba(226, 232, 240, 0.65);
      }

      .hand-wrapper.hand--concealed .hand-total::after {
        content: \" • dealer is hiding a card\";
        text-transform: none;
        font-size: 0.75rem;
        letter-spacing: 0;
      }

      .table-footer {
        display: flex;
        flex-direction: column;
        gap: 1.1rem;
      }

      .outcome {
        font-weight: 700;
        font-size: 1.1rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: var(--text-muted);
      }

      .outcome--win {
        color: var(--win);
      }

      .outcome--loss {
        color: var(--loss);
      }

      .outcome--push {
        color: var(--push);
      }

      .bet-controls {
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
        align-items: flex-end;
      }

      .bet-controls label {
        flex: 1;
        min-width: 180px;
      }

      .bet-controls input[type=\"number\"] {
        max-width: 220px;
      }

      .chip-row {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
      }

      .chip-button {
        border-radius: 999px;
        padding: 0.55rem 0.9rem;
        font-size: 0.95rem;
        border: 1px solid rgba(34, 211, 238, 0.45);
        background: rgba(14, 165, 233, 0.16);
        color: var(--accent);
      }

      .chip-button:hover:not(:disabled) {
        background: rgba(14, 165, 233, 0.26);
      }

      .chip-button--active {
        background: linear-gradient(135deg, rgba(34, 211, 238, 0.85), rgba(14, 165, 233, 0.85));
        color: #001219;
      }

      .action-buttons {
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
      }

      footer {
        margin-top: auto;
        text-align: center;
        color: var(--text-muted);
        font-size: 0.85rem;
      }

      footer code {
        color: var(--accent);
      }

      @media (max-width: 1024px) {
        main.layout {
          grid-template-columns: 1fr;
        }

        .panel--auth {
          order: 2;
        }

        .panel--table {
          order: 1;
        }
      }

      @media (max-width: 640px) {
        .app-shell {
          padding: 1.25rem 1rem 2rem;
        }

        .app-header {
          flex-direction: column;
          align-items: flex-start;
        }

        .card-tile {
          width: 62px;
          height: 94px;
        }
      }

      @media (max-width: 480px) {
        .bet-controls label {
          min-width: 100%;
        }

        .bet-controls {
          flex-direction: column;
          align-items: stretch;
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
    <div class=\"app-shell\">
      <header class=\"app-header\">
        <div>
          <h1>OpenBlackJack</h1>
          <p class=\"tagline\">Casino-style single-player blackjack with instant play.</p>
        </div>
        <div class=\"status-badge status--info\" id=\"status\">Play as a guest or sign in to start betting.</div>
      </header>
      <main class=\"layout\">
        <aside class=\"panel panel--auth\">
          <div class=\"panel-section\">
            <h2>Account</h2>
            <p class=\"balance\" id=\"balance-area\">Guest mode — betting disabled.</p>
            <p class=\"session-id\" id=\"session-info\"></p>
          </div>
          <div class=\"panel-section forms\">
            <form id=\"signup-form\" class=\"form-card\">
              <h3>Create an account</h3>
              <label>
                Username
                <input id=\"signup-username\" name=\"username\" minlength=\"3\" maxlength=\"30\" autocomplete=\"username\" required />
              </label>
              <label>
                Password
                <input id=\"signup-password\" name=\"password\" type=\"password\" minlength=\"6\" autocomplete=\"new-password\" required />
              </label>
              <button class=\"primary\" type=\"submit\">Create account</button>
              <p class=\"muted\">New accounts instantly receive a $1000 bankroll.</p>
            </form>
            <form id=\"login-form\" class=\"form-card\">
              <h3>Log in</h3>
              <label>
                Username
                <input id=\"login-username\" name=\"username\" autocomplete=\"username\" required />
              </label>
              <label>
                Password
                <input id=\"login-password\" name=\"password\" type=\"password\" autocomplete=\"current-password\" required />
              </label>
              <button class=\"primary\" type=\"submit\">Log in</button>
            </form>
            <div class=\"auth-actions\">
              <button class=\"secondary\" type=\"button\" id=\"guest-button\">Play as guest</button>
              <button class=\"secondary\" type=\"button\" id=\"logout-button\" disabled>Log out</button>
            </div>
          </div>
        </aside>
        <section class=\"panel panel--table\">
          <div class=\"table-surface\">
            <div class=\"table-row\">
              <div class=\"hand-wrapper\" id=\"dealer-hand\">
                <h3>Dealer</h3>
                <div class=\"card-tiles\"></div>
                <div class=\"hand-total\"></div>
              </div>
            </div>
            <div class=\"table-row\">
              <div class=\"hand-wrapper\" id=\"player-hand\">
                <h3>Player</h3>
                <div class=\"card-tiles\"></div>
                <div class=\"hand-total\"></div>
              </div>
            </div>
          </div>
          <div class=\"table-footer\">
            <div class=\"outcome\" id=\"outcome\">Start a hand to begin playing.</div>
            <form id=\"start-form\" class=\"bet-controls\">
              <label>
                Bet amount (USD)
                <input id=\"bet-input\" name=\"bet\" type=\"number\" min=\"0\" step=\"50\" value=\"0\" />
              </label>
              <div class=\"chip-row\">
                <button class=\"chip-button\" type=\"button\" data-chip=\"50\">$50</button>
                <button class=\"chip-button\" type=\"button\" data-chip=\"100\">$100</button>
                <button class=\"chip-button\" type=\"button\" data-chip=\"250\">$250</button>
                <button class=\"chip-button\" type=\"button\" data-chip=\"500\">$500</button>
              </div>
              <button class=\"primary\" type=\"submit\">Deal a new hand</button>
            </form>
            <div class=\"action-buttons\">
              <button class=\"secondary\" type=\"button\" id=\"hit-button\" disabled>Hit</button>
              <button class=\"secondary\" type=\"button\" id=\"stand-button\" disabled>Stand</button>
            </div>
          </div>
        </section>
      </main>
      <footer>Need the API? Explore the interactive docs at <code>/docs</code>.</footer>
    </div>
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
      const chipButtons = Array.from(document.querySelectorAll('[data-chip]'));

      let token = null;
      let profile = null;
      let sessionId = null;

      function setStatus(message, tone = 'info') {
        statusEl.textContent = message;
        statusEl.className = `status-badge status--${tone}`;
      }

      function authHeaders() {
        return token ? { Authorization: `Bearer ${token}` } : {};
      }

      function formatCurrency(value) {
        const amount = Number(value || 0);
        return `$${amount.toLocaleString('en-US')}`;
      }

      function updateOutcomeTone(outcome) {
        const tone = {
          player_blackjack: 'outcome--win',
          player_win: 'outcome--win',
          dealer_bust: 'outcome--win',
          dealer_blackjack: 'outcome--loss',
          dealer_win: 'outcome--loss',
          player_bust: 'outcome--loss',
          push: 'outcome--push',
        }[outcome] || 'outcome--neutral';
        outcomeEl.className = `outcome ${tone}`;
      }

      function clearChipSelection() {
        chipButtons.forEach((button) => button.classList.remove('chip-button--active'));
      }

      function updateAuthUI() {
        if (profile) {
          balanceEl.textContent = `Logged in as ${profile.username} — Balance: ${formatCurrency(profile.balance)}`;
          logoutButton.disabled = false;
          betInput.disabled = false;
        } else {
          balanceEl.textContent = 'Guest mode — betting disabled.';
          logoutButton.disabled = true;
          betInput.value = '0';
          betInput.disabled = true;
          clearChipSelection();
        }
      }

      function renderHand(element, hand, options = {}) {
        const { hideHoleCard = false } = options;
        const tilesContainer = element.querySelector('.card-tiles');
        const totalEl = element.querySelector('.hand-total');
        if (!tilesContainer || !totalEl) {
          return;
        }

        if (!hand.cards.length) {
          tilesContainer.innerHTML = '<p class=\"muted\">Waiting for deal…</p>';
          totalEl.textContent = '';
          element.classList.remove('hand--concealed');
          return;
        }

        const suitIcons = {
          Hearts: '♥',
          Diamonds: '♦',
          Clubs: '♣',
          Spades: '♠',
        };

        const html = hand.cards
          .map((card, index) => {
            const isHole = hideHoleCard && index === 1;
            if (isHole) {
              return '<div class=\"card-tile card-back\"></div>';
            }
            const suit = card.suit;
            const suitIcon = suitIcons[suit] || suit;
            const suitClass = suit === 'Hearts' || suit === 'Diamonds' ? 'red' : 'black';
            const rankLabel = card.rank === '10' ? '10' : card.rank.charAt(0);
            return `
              <div class=\"card-tile ${suitClass}\">
                <span class=\"corner corner--top\">${rankLabel}${suitIcon}</span>
                <span class=\"symbol\" aria-hidden=\"true\">${suitIcon}</span>
                <span class=\"rank\">${card.rank}</span>
                <span class=\"corner corner--bottom\">${rankLabel}${suitIcon}</span>
              </div>
            `;
          })
          .join('');

        tilesContainer.innerHTML = html;
        if (hideHoleCard) {
          element.classList.add('hand--concealed');
          totalEl.textContent = 'Total: ??';
        } else {
          element.classList.remove('hand--concealed');
          totalEl.textContent = `Total: ${hand.value}`;
        }
      }

      function handleGameState(data) {
        sessionId = data.session_id;
        const shortId = sessionId.slice(0, 8);
        const betLabel = data.bet ? ` • Bet: ${formatCurrency(data.bet)}` : '';
        sessionInfoEl.innerHTML = `Session <span>${shortId}…</span>${betLabel}`;
        renderHand(playerHandEl, data.player_hand);
        const hideDealerCard = !data.is_over && data.dealer_hand.cards.length > 1;
        renderHand(dealerHandEl, data.dealer_hand, { hideHoleCard: hideDealerCard });
        outcomeEl.textContent = formatOutcome(data.outcome, data.is_over);
        updateOutcomeTone(data.outcome);
        if (typeof data.balance === 'number' && profile) {
          profile.balance = data.balance;
          updateAuthUI();
        }
        const actionEnabled = !data.is_over;
        hitButton.disabled = !actionEnabled;
        standButton.disabled = !actionEnabled;
        return data;
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
          push: "Push — it's a tie.",
        };
        return mapping[outcome] || outcome.replace('_', ' ');
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
          clearChipSelection();
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

      chipButtons.forEach((button) => {
        button.addEventListener('click', () => {
          const amount = parseInt(button.dataset.chip, 10) || 0;
          if (!profile) {
            setStatus('Sign in to wager with chips.', 'warning');
            return;
          }
          betInput.value = amount;
          clearChipSelection();
          button.classList.add('chip-button--active');
        });
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
