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
    <meta
      name=\"viewport\"
      content=\"width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no\"
    />
    <title>OpenBlackJack Arcade</title>
    <style>
      :root {
        color-scheme: dark;
        --bg: #020617;
        --bg-secondary: #041621;
        --panel: rgba(4, 17, 34, 0.85);
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
        --shadow: rgba(7, 11, 27, 0.55);
      }

      html {
        height: 100%;
      }

      * {
        box-sizing: border-box;
      }

      body {
        margin: 0;
        font-family: \"Inter\", \"Segoe UI\", system-ui, -apple-system, sans-serif;
        background: radial-gradient(circle at 20% 20%, rgba(14, 116, 144, 0.25), transparent 55%),
          radial-gradient(circle at 80% 0%, rgba(17, 94, 89, 0.3), transparent 40%),
          linear-gradient(150deg, #001219 0%, #020617 55%, #010409 100%);
        color: var(--text-primary);
        min-height: 100vh;
        height: 100vh;
        display: flex;
        flex-direction: column;
      }

      .app-shell {
        width: min(1160px, 100%);
        margin: 0 auto;
        padding: clamp(1rem, 3vw, 2.5rem);
        display: flex;
        flex-direction: column;
        gap: 1.75rem;
        flex: 1 1 auto;
      }

      .app-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem 2rem;
      }

      h1 {
        margin: 0;
        font-size: clamp(2rem, 6vw, 3.1rem);
        letter-spacing: 0.1em;
        text-transform: uppercase;
        font-weight: 800;
      }

      .tagline {
        margin: 0.35rem 0 0;
        color: var(--text-muted);
        font-size: clamp(0.95rem, 2.5vw, 1.05rem);
        letter-spacing: 0.03em;
      }

      .status-badge {
        padding: 0.85rem 1.4rem;
        border-radius: 999px;
        border: 1px solid rgba(148, 163, 184, 0.3);
        background: rgba(14, 116, 144, 0.12);
        font-size: 0.95rem;
        letter-spacing: 0.02em;
        transition: background 0.25s ease, border 0.25s ease, transform 0.25s ease;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-height: 46px;
        text-align: center;
      }

      .status-badge[data-tone='success'] {
        color: var(--success);
        border-color: rgba(52, 211, 153, 0.35);
        background: rgba(52, 211, 153, 0.12);
      }

      .status-badge[data-tone='error'] {
        color: var(--danger);
        border-color: rgba(248, 113, 113, 0.35);
        background: rgba(248, 113, 113, 0.12);
      }

      .status-badge[data-tone='warning'] {
        color: var(--warning);
        border-color: rgba(251, 191, 36, 0.35);
        background: rgba(251, 191, 36, 0.12);
      }

      main.layout {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        flex: 1 1 auto;
      }

      .panel {
        background: var(--panel);
        border-radius: 24px;
        border: 1px solid var(--panel-border);
        padding: clamp(1.25rem, 3vw, 1.75rem);
        backdrop-filter: blur(18px);
        box-shadow: 0 35px 75px var(--shadow);
        display: flex;
        flex-direction: column;
        gap: 1.4rem;
      }

      .panel h2 {
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 1.05rem;
      }

      .balance {
        font-weight: 600;
        font-size: 1.05rem;
      }

      .table-surface {
        position: relative;
        min-height: 420px;
        border-radius: 24px;
        padding: clamp(1.25rem, 4vw, 2rem);
        border: 1px solid rgba(148, 163, 184, 0.2);
        background: radial-gradient(circle at 50% 15%, rgba(45, 212, 191, 0.25), transparent 55%),
          radial-gradient(circle at 50% 100%, rgba(14, 165, 233, 0.18), transparent 45%),
          linear-gradient(160deg, rgba(4, 30, 49, 0.82), rgba(1, 27, 43, 0.88));
        overflow: hidden;
        display: flex;
        flex-direction: column;
      }

      #phaser-stage {
        width: 100%;
        height: 100%;
        flex: 1 1 auto;
      }

      .table-overlay {
        position: absolute;
        inset: 0;
        pointer-events: none;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: clamp(1rem, 3vw, 1.75rem);
      }

      .overlay-top {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        flex-wrap: wrap;
        pointer-events: none;
      }

      .overlay-bottom {
        display: flex;
        flex-direction: column;
        gap: 0.85rem;
        pointer-events: none;
      }

      .hand-meta {
        display: flex;
        flex-direction: column;
        gap: 0.35rem;
        align-items: flex-start;
      }

      .hand-meta h3 {
        margin: 0;
        font-size: 0.95rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
      }

      .hand-total {
        font-size: 0.95rem;
        font-weight: 600;
        letter-spacing: 0.05em;
      }

      .hand-meta .hand-status {
        color: var(--text-muted);
        font-size: 0.8rem;
        letter-spacing: 0.02em;
      }

      .player-hands-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
        gap: 0.85rem;
        pointer-events: none;
      }

      .player-hand-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(148, 163, 184, 0.25);
        border-radius: 18px;
        padding: 0.75rem 1rem;
        display: flex;
        flex-direction: column;
        gap: 0.35rem;
      }

      .player-hand-card--active {
        border-color: rgba(34, 211, 238, 0.6);
        box-shadow: 0 12px 32px rgba(14, 165, 233, 0.18);
      }

      .player-hand-card h3 {
        margin: 0;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--text-muted);
      }

      .player-hand-card .hand-total {
        font-size: 0.95rem;
        font-weight: 600;
      }

      .player-hand-card .hand-status {
        font-size: 0.75rem;
        color: var(--text-muted);
      }

      .bet-spots {
        display: flex;
        justify-content: center;
        gap: 0.8rem;
        flex-wrap: wrap;
        pointer-events: none;
      }

      .bet-spot {
        pointer-events: auto;
        border: 2px dashed rgba(34, 211, 238, 0.4);
        border-radius: 999px;
        padding: 0.7rem 1.4rem;
        background: rgba(14, 165, 233, 0.12);
        color: var(--accent);
        font-weight: 600;
        letter-spacing: 0.05em;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.25rem;
        transition: transform 0.2s ease, background 0.2s ease, border 0.2s ease;
      }

      .bet-spot:hover {
        background: rgba(14, 165, 233, 0.2);
        transform: translateY(-1px);
      }

      .bet-spot:focus-visible {
        outline: none;
        border-color: var(--accent-strong);
        box-shadow: 0 0 0 3px rgba(34, 211, 238, 0.25);
      }

      .bet-spot--locked {
        cursor: not-allowed;
        opacity: 0.6;
        pointer-events: none;
      }

      .bet-spot__label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
      }

      .bet-spot__amount {
        font-size: 1rem;
        font-weight: 600;
      }

      .sidebet-summary {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        pointer-events: none;
      }

      .sidebet-chip {
        background: rgba(15, 23, 42, 0.55);
        border-radius: 14px;
        border: 1px solid rgba(148, 163, 184, 0.25);
        padding: 0.45rem 0.75rem;
        font-size: 0.75rem;
        letter-spacing: 0.04em;
      }

      .sidebet-chip[data-result='win'] {
        border-color: rgba(52, 211, 153, 0.5);
        color: var(--success);
      }

      .sidebet-chip[data-result='loss'] {
        border-color: rgba(248, 113, 113, 0.45);
        color: var(--danger);
      }

      .sidebet-chip[data-result='inactive'] {
        color: var(--text-muted);
      }

      .hand-meta.hand--concealed .hand-total {
        color: rgba(226, 232, 240, 0.75);
      }

      .session-id {
        align-self: center;
        font-family: \"Fira Code\", \"Source Code Pro\", monospace;
        font-size: 0.85rem;
        letter-spacing: 0.04em;
        color: var(--text-muted);
        padding: 0.4rem 1rem;
        border-radius: 999px;
        background: rgba(15, 23, 42, 0.55);
        border: 1px solid rgba(148, 163, 184, 0.2);
      }

      .session-id span {
        color: var(--accent);
      }

      .table-footer {
        display: flex;
        flex-direction: column;
        gap: 1.25rem;
      }

      .outcome {
        font-weight: 700;
        font-size: 1.05rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        color: var(--text-muted);
      }

      .outcome.outcome--win {
        color: var(--win);
      }

      .outcome.outcome--loss {
        color: var(--loss);
      }

      .outcome.outcome--push {
        color: var(--push);
      }

      form {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
      }

      .bet-controls {
        display: flex;
        flex-wrap: wrap;
        gap: 0.85rem;
        align-items: flex-end;
      }

      .bet-controls label {
        flex: 1 1 220px;
        min-width: 180px;
      }

      label {
        font-size: 0.88rem;
        font-weight: 600;
        display: flex;
        flex-direction: column;
        gap: 0.4rem;
      }

      input {
        padding: 0.7rem 0.85rem;
        border-radius: 12px;
        border: 1px solid rgba(148, 163, 184, 0.35);
        background: rgba(2, 6, 23, 0.35);
        color: inherit;
        font-size: 1rem;
        transition: border 0.2s ease, box-shadow 0.2s ease;
        touch-action: manipulation;
      }

      input:focus {
        outline: none;
        border-color: var(--accent);
        box-shadow: 0 0 0 3px rgba(34, 211, 238, 0.25);
      }

      button {
        cursor: pointer;
        border: none;
        border-radius: 14px;
        padding: 0.8rem 1.3rem;
        font-weight: 600;
        font-size: 1rem;
        letter-spacing: 0.03em;
        display: inline-flex;
        justify-content: center;
        align-items: center;
        gap: 0.45rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease, background 0.2s ease, opacity 0.2s ease;
        touch-action: manipulation;
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
        box-shadow: 0 16px 36px rgba(14, 165, 233, 0.35);
      }

      button.primary:hover:not(:disabled) {
        transform: translateY(-1px);
        box-shadow: 0 20px 42px rgba(34, 211, 238, 0.4);
      }

      button.secondary {
        background: rgba(15, 23, 42, 0.45);
        color: var(--text-primary);
        border: 1px solid rgba(148, 163, 184, 0.18);
      }

      button.secondary:hover:not(:disabled) {
        background: rgba(15, 23, 42, 0.65);
      }

      .chip-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
      }

      .chip-button {
        border-radius: 999px;
        padding: 0.6rem 0.95rem;
        font-size: 0.95rem;
        border: 1px solid rgba(34, 211, 238, 0.45);
        background: rgba(14, 165, 233, 0.16);
        color: var(--accent);
        transition: transform 0.2s ease, background 0.2s ease;
      }

      .chip-button:hover:not(:disabled) {
        background: rgba(14, 165, 233, 0.26);
        transform: translateY(-1px);
      }

      .chip-button--active {
        background: linear-gradient(135deg, rgba(34, 211, 238, 0.85), rgba(14, 165, 233, 0.85));
        color: #001219;
        box-shadow: 0 12px 30px rgba(14, 165, 233, 0.35);
      }

      .action-buttons {
        display: flex;
        flex-wrap: wrap;
        gap: 0.75rem;
      }

      .action-buttons button {
        flex: 1 1 160px;
      }

      .aux-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 0.65rem;
      }

      .aux-actions button {
        flex: 1 1 160px;
      }

      .muted {
        color: var(--text-muted);
        font-size: 0.85rem;
      }

      .session-actions {
        display: flex;
        flex-wrap: wrap;
        gap: 0.65rem;
      }

      .session-actions button {
        flex: 1 1 180px;
      }

      .hidden {
        display: none !important;
      }

      .auth-overlay {
        position: absolute;
        inset: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: clamp(1rem, 4vw, 2rem);
        background: rgba(2, 6, 23, 0.65);
        backdrop-filter: blur(18px);
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.25s ease;
      }

      .auth-overlay--active {
        opacity: 1;
        pointer-events: auto;
      }

      .auth-card {
        width: min(420px, 100%);
        background: rgba(4, 17, 34, 0.92);
        border: 1px solid var(--panel-border);
        border-radius: 20px;
        padding: clamp(1.25rem, 4vw, 1.75rem);
        box-shadow: 0 30px 60px var(--shadow);
        display: flex;
        flex-direction: column;
        gap: 1.1rem;
      }

      .auth-card h3 {
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 0.95rem;
      }

      .auth-tabs {
        display: inline-flex;
        align-self: center;
        background: rgba(15, 23, 42, 0.55);
        border-radius: 999px;
        padding: 0.25rem;
        gap: 0.35rem;
      }

      .auth-tab {
        flex: 1 1 0;
        border: none;
        background: transparent;
        color: var(--text-muted);
        font-weight: 600;
        letter-spacing: 0.03em;
        border-radius: 999px;
        padding: 0.55rem 1.1rem;
        cursor: pointer;
        transition: background 0.2s ease, color 0.2s ease, box-shadow 0.2s ease;
      }

      .auth-tab--active {
        background: linear-gradient(135deg, var(--accent), var(--accent-strong));
        color: #001219;
        box-shadow: 0 10px 28px rgba(14, 165, 233, 0.35);
      }

      .auth-form {
        display: none;
        flex-direction: column;
        gap: 0.75rem;
      }

      .auth-form--active {
        display: flex;
      }

      .auth-close {
        align-self: center;
        background: transparent;
        border: none;
        color: var(--text-muted);
        font-size: 0.85rem;
        cursor: pointer;
        letter-spacing: 0.03em;
      }

      .auth-close:hover {
        color: var(--text-primary);
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
        .table-surface {
          min-height: 420px;
        }
      }

      @media (orientation: portrait) and (max-width: 1024px) {
        .table-surface {
          min-height: clamp(480px, 75vh, 640px);
          aspect-ratio: 3 / 4;
        }

        .table-overlay {
          padding: clamp(1rem, 5vw, 1.75rem);
        }
      }

      @media (max-width: 640px) {
        body {
          font-size: 16px;
        }

        .app-shell {
          padding: 1rem 1rem 2rem;
          gap: 1.25rem;
        }

        .app-header {
          flex-direction: column;
          align-items: flex-start;
          gap: 0.75rem;
        }

        h1 {
          font-size: clamp(1.85rem, 8vw, 2.4rem);
        }

        .tagline {
          font-size: 0.95rem;
        }

        .status-badge {
          width: 100%;
        }

        main.layout {
          gap: 1rem;
        }

        .panel {
          padding: 1rem 1.1rem;
          border-radius: 18px;
          gap: 1rem;
        }

        .table-surface {
          min-height: 360px;
          padding: 1rem;
          border-radius: 18px;
          aspect-ratio: 2 / 3;
        }

        .table-overlay {
          padding: 0.75rem 0.85rem 1rem;
          gap: 0.85rem;
        }

        .table-footer {
          gap: 0.85rem;
        }

        .bet-controls {
          flex-direction: column;
          align-items: stretch;
        }

        .bet-controls label {
          width: 100%;
        }

        .action-buttons {
          flex-direction: column;
          width: 100%;
        }

        .session-actions,
        .action-buttons {
          width: 100%;
        }

        .session-actions button,
        .action-buttons button {
          width: 100%;
        }

        .chip-row {
          justify-content: center;
        }

        .auth-card {
          padding: 1.1rem;
        }

        footer {
          font-size: 0.8rem;
        }
      }

      @media (max-width: 420px) {
        .app-shell {
          padding: 0.75rem 0.85rem 1.5rem;
        }

        .status-badge {
          padding: 0.75rem 1rem;
        }

        .panel {
          padding: 0.9rem;
        }

        .table-surface {
          padding: 0.9rem;
        }

        .hand-meta h3 {
          font-size: 0.85rem;
        }

        .hand-total {
          font-size: 0.9rem;
        }

        input {
          font-size: 0.95rem;
        }

        button {
          font-size: 0.95rem;
          padding: 0.75rem 1rem;
        }
      }
    </style>
    <script src=\"https://cdn.jsdelivr.net/npm/phaser@3.60.0/dist/phaser.min.js\"></script>
  </head>
  <body>
    <div class=\"app-shell\">
      <header class=\"app-header\">
        <div>
          <h1>OpenBlackJack</h1>
          <p class=\"tagline\">Arcade-style single player blackjack.</p>
        </div>
        <div id=\"status\" class=\"status-badge\" data-tone=\"info\" role=\"status\">
          Chargement de la table…
        </div>
      </header>

      <div class=\"balance\" id=\"balance\">Mode invité — mises désactivées.</div>

      <main class=\"layout\">
        <section class=\"panel panel--table\">
          <div class=\"table-surface\">
            <div id=\"phaser-stage\" aria-hidden=\"true\"></div>
            <div class=\"table-overlay\">
              <div class=\"overlay-top\">
                <div class=\"hand-meta\" id=\"dealer-info\">
                  <h3>DEALER</h3>
                  <p class=\"hand-total\">En attente…</p>
                  <span class=\"hand-status\"></span>
                </div>
                <div class=\"sidebet-summary\" id=\"sidebet-summary\" aria-live=\"polite\"></div>
              </div>
              <div class=\"bet-spots\" role=\"group\" aria-label=\"Zones de mise\">
                <button type=\"button\" class=\"bet-spot\" data-spot=\"main\">
                  <span class=\"bet-spot__label\">Mise principale</span>
                  <span class=\"bet-spot__amount\" data-spot-amount=\"main\">0</span>
                </button>
                <button type=\"button\" class=\"bet-spot\" data-spot=\"pair\">
                  <span class=\"bet-spot__label\">Paire</span>
                  <span class=\"bet-spot__amount\" data-spot-amount=\"pair\">0</span>
                </button>
                <button type=\"button\" class=\"bet-spot\" data-spot=\"suited_pair\">
                  <span class=\"bet-spot__label\">Paire assortie</span>
                  <span class=\"bet-spot__amount\" data-spot-amount=\"suited_pair\">0</span>
                </button>
              </div>
              <div class=\"overlay-bottom\">
                <div class=\"player-hands-grid\" id=\"player-hands-info\"></div>
                <div class=\"session-id\" id=\"session-info\">Session <span>—</span></div>
              </div>
            </div>
            <div class=\"auth-overlay\" id=\"auth-overlay\" aria-hidden=\"true\">
              <div class=\"auth-card\">
                <div class=\"auth-tabs\" role=\"tablist\">
                  <button type=\"button\" class=\"auth-tab auth-tab--active\" data-auth-tab=\"login\" role=\"tab\" aria-selected=\"true\">
                    Connexion
                  </button>
                  <button type=\"button\" class=\"auth-tab\" data-auth-tab=\"signup\" role=\"tab\" aria-selected=\"false\">
                    Inscription
                  </button>
                </div>
                <form id=\"login-form\" class=\"auth-form auth-form--active\" autocomplete=\"on\">
                  <h3>Connexion</h3>
                  <label>Nom d'utilisateur
                    <input id=\"login-username\" autocomplete=\"username\" required />
                  </label>
                  <label>Mot de passe
                    <input id=\"login-password\" type=\"password\" autocomplete=\"current-password\" required />
                  </label>
                  <button class=\"primary\" type=\"submit\">Se connecter</button>
                </form>
                <form id=\"signup-form\" class=\"auth-form\" autocomplete=\"on\">
                  <h3>Inscription</h3>
                  <label>Nom d'utilisateur
                    <input id=\"signup-username\" autocomplete=\"username\" required />
                  </label>
                  <label>Mot de passe
                    <input id=\"signup-password\" type=\"password\" autocomplete=\"new-password\" required />
                  </label>
                  <button class=\"primary\" type=\"submit\">Créer un compte</button>
                </form>
                <button type=\"button\" class=\"auth-close\" id=\"auth-close\">Continuer en invité</button>
              </div>
            </div>
          </div>

          <div class=\"table-footer\">
            <div class=\"outcome\" id=\"outcome\">Lancez une main pour commencer.</div>

            <form id=\"start-form\">
              <div class=\"bet-controls\">
                <label for=\"bet\">Mise principale
                  <input id=\"bet\" type=\"number\" min=\"0\" step=\"10\" value=\"0\" readonly />
                </label>
                <div class=\"chip-row\">
                  <button type=\"button\" class=\"chip-button\" data-chip=\"10\">10</button>
                  <button type=\"button\" class=\"chip-button\" data-chip=\"25\">25</button>
                  <button type=\"button\" class=\"chip-button\" data-chip=\"50\">50</button>
                  <button type=\"button\" class=\"chip-button\" data-chip=\"100\">100</button>
                </div>
              </div>
              <div class=\"action-buttons\">
                <button class=\"primary\" type=\"submit\">Distribuer</button>
                <button class=\"secondary\" type=\"button\" id=\"hit-button\" disabled>Carte !</button>
                <button class=\"secondary\" type=\"button\" id=\"stand-button\" disabled>Rester</button>
                <button class=\"secondary\" type=\"button\" id=\"double-button\" disabled>Double</button>
                <button class=\"secondary\" type=\"button\" id=\"split-button\" disabled>Séparer</button>
              </div>
              <div class=\"aux-actions\">
                <button class=\"secondary\" type=\"button\" id=\"clear-bets\">Réinitialiser les mises</button>
                <button class=\"secondary\" type=\"button\" id=\"fullscreen-button\">Plein écran</button>
              </div>
            </form>

            <div class=\"session-actions\">
              <button class=\"secondary\" type=\"button\" id=\"auth-open\">Connexion / Inscription</button>
              <button class=\"secondary\" type=\"button\" id=\"guest-button\">Jouer en invité</button>
              <button class=\"secondary hidden\" type=\"button\" id=\"logout-button\" disabled>Se déconnecter</button>
            </div>
            <p class=\"muted\">
              Sélectionnez un jeton puis cliquez sur une zone de mise pour placer vos crédits. Clic droit retire le jeton actif. Les comptes sauvegardent vos crédits et permettent les mises. En invité, les mises sont bloquées.
            </p>
          </div>
        </section>
      </main>

      <footer>
        OpenBlackJack propulsé par <code>FastAPI</code> et un rendu Phaser côté client.
      </footer>
    </div>

    <script>
      class BlackjackAnimator {
        constructor(mountId) {
          this.mountId = mountId;
          this.scene = null;
          this.cardSprites = {};
          this.pendingState = null;
          if (!window.Phaser) {
            return;
          }
          const viewportWidth = window.innerWidth || window.screen.width || 720;
          const viewportHeight = window.innerHeight || window.screen.height || 720;
          const isPortrait = viewportHeight > viewportWidth;
          const baseWidth = isPortrait ? 540 : 720;
          const baseHeight = isPortrait ? 720 : 360;
          const animator = this;
          this.game = new Phaser.Game({
            type: Phaser.AUTO,
            parent: mountId,
            transparent: true,
            scale: {
              mode: Phaser.Scale.FIT,
              autoCenter: Phaser.Scale.CENTER_BOTH,
              width: baseWidth,
              height: baseHeight,
            },
            scene: {
              create() {
                animator.scene = this;
                animator.buildTable();
                if (animator.pendingState) {
                  const { playerHands, dealer, options } = animator.pendingState;
                  animator.updateHands(playerHands, dealer, options);
                  animator.pendingState = null;
                }
              },
            },
          });

        }

        buildTable() {
          const scene = this.scene;
          if (!scene) {
            return;
          }
          const { width, height } = scene.scale;
          const table = scene.add.rectangle(width / 2, height / 2, width * 0.9, height * 0.8, 0x083344, 0.75);
          table.setStrokeStyle(2, 0x22d3ee, 0.3);
          const glow = scene.add.ellipse(width / 2, height / 2, width * 0.6, height * 0.35, 0x0ea5e9, 0.15);
          scene.tweens.add({
            targets: glow,
            scaleX: 1.08,
            scaleY: 1.12,
            alpha: 0.18,
            yoyo: true,
            duration: 2400,
            repeat: -1,
            ease: 'Sine.easeInOut',
          });
          this.deckPosition = new Phaser.Math.Vector2(width - 80, height / 2);
          this.createFloatingChips();
        }

        createFloatingChips() {
          const scene = this.scene;
          if (!scene) {
            return;
          }
          const colors = [0x22d3ee, 0xfacc15, 0x34d399];
          colors.forEach((color, index) => {
            const chip = scene.add.circle(90 + index * 60, scene.scale.height - 60, 18, color, 0.8);
            chip.setStrokeStyle(3, 0xffffff, 0.6);
            scene.tweens.add({
              targets: chip,
              y: chip.y - 12,
              duration: 1600 + index * 180,
              yoyo: true,
              repeat: -1,
              ease: 'Sine.easeInOut',
            });
          });
        }

        ensureSceneReady(playerHands, dealer, options) {
          if (!this.scene) {
            this.pendingState = { playerHands, dealer, options };
            return false;
          }
          return true;
        }

        populateCard(container, card, hidden) {
          const scene = this.scene;
          if (!scene) {
            return;
          }
          container.removeAll(true);
          if (hidden) {
            const bg = scene.add.rectangle(0, 0, 92, 128, 0x052527, 0.95);
            bg.setStrokeStyle(2, 0x22d3ee, 0.5);
            const inner = scene.add.rectangle(0, 0, 72, 108, 0x0b3740, 0.95);
            inner.setStrokeStyle(2, 0xffffff, 0.25);
            const emblem = scene.add.text(0, 0, 'OB', {
              fontFamily: 'Inter, sans-serif',
              fontSize: '28px',
              fontStyle: '700',
              color: '#22d3ee',
            });
            emblem.setOrigin(0.5, 0.5);
            container.add([bg, inner, emblem]);
          } else {
            const bg = scene.add.rectangle(0, 0, 92, 128, 0xf8fafc, 0.96);
            bg.setStrokeStyle(2, 0x0f172a, 0.18);
            const suitSymbols = { Hearts: '♥', Diamonds: '♦', Clubs: '♣', Spades: '♠' };
            const suitSymbol = suitSymbols[card.suit] || card.suit.charAt(0);
            const rankLabel = card.rank.length > 2 ? card.rank.charAt(0) : card.rank;
            const isRed = card.suit === 'Hearts' || card.suit === 'Diamonds';
            const color = isRed ? '#dc2626' : '#0f172a';
            const suit = scene.add.text(0, 18, suitSymbol, {
              fontFamily: 'Georgia, serif',
              fontSize: '36px',
              color,
            });
            suit.setOrigin(0.5, 0.5);
            const rank = scene.add.text(0, -22, rankLabel, {
              fontFamily: 'Inter, sans-serif',
              fontSize: '28px',
              fontStyle: '700',
              color,
            });
            rank.setOrigin(0.5, 0.5);
            const cornerTop = scene.add.text(-28, -46, `${rankLabel}${suitSymbol}`, {
              fontFamily: 'Inter, sans-serif',
              fontSize: '14px',
              fontStyle: '600',
              color,
            });
            cornerTop.setOrigin(0, 0);
            const cornerBottom = scene.add.text(28, 46, `${rankLabel}${suitSymbol}`, {
              fontFamily: 'Inter, sans-serif',
              fontSize: '14px',
              fontStyle: '600',
              color,
            });
            cornerBottom.setOrigin(1, 1);
            container.add([bg, suit, rank, cornerTop, cornerBottom]);
          }
          container.setData('card', card);
          container.setData('hidden', hidden);
        }

        updateHands(playerHands, dealer, options = {}) {
          if (!this.ensureSceneReady(playerHands, dealer, options)) {
            return;
          }
          this.syncHand('dealer', dealer.cards, { hideHoleCard: options.hideHoleCard, y: 110 });
          const activeKeys = new Set();
          playerHands.forEach((hand, index) => {
            const key = `player-${index}`;
            activeKeys.add(key);
            const rowSpacing = 110;
            const baseY = this.scene ? this.scene.scale.height - 110 : 0;
            const y = baseY - index * rowSpacing;
            this.syncHand(key, hand.cards, { hideHoleCard: false, y });
          });
          Object.keys(this.cardSprites)
            .filter((key) => key.startsWith('player-') && !activeKeys.has(key))
            .forEach((key) => this.teardownHand(key));
        }

        syncHand(owner, cards, config) {
          const scene = this.scene;
          if (!scene) {
            return;
          }
          const spacing = 110;
          const baseX = scene.scale.width / 2 - ((cards.length - 1) * spacing) / 2;
          const existing = this.cardSprites[owner] || [];
          this.cardSprites[owner] = existing;
          while (existing.length > cards.length) {
            const sprite = existing.pop();
            if (sprite.container) {
              scene.tweens.add({
                targets: sprite.container,
                y: sprite.container.y + 60,
                alpha: 0,
                duration: 240,
                ease: 'Quad.easeIn',
                onComplete: () => {
                  sprite.container.removeAll(true);
                  sprite.container.destroy();
                },
              });
            }
          }
          cards.forEach((card, index) => {
            const isHole = config.hideHoleCard && index === 1;
            const targetX = baseX + index * spacing;
            let sprite = existing[index];
            if (!sprite) {
              const container = scene.add.container(this.deckPosition.x, this.deckPosition.y);
              container.setSize(92, 128);
              container.alpha = 0;
              this.populateCard(container, card, isHole);
              scene.tweens.add({
                targets: container,
                x: targetX,
                y: config.y,
                alpha: 1,
                angle: Phaser.Math.Between(-5, 5),
                duration: 420,
                ease: 'Cubic.easeOut',
                delay: index * 100,
              });
              scene.tweens.add({
                targets: container,
                scaleX: 1.02,
                scaleY: 1.02,
                yoyo: true,
                duration: 400,
                repeat: -1,
                ease: 'Sine.easeInOut',
                delay: 600 + index * 120,
              });
              existing[index] = { container };
              sprite = existing[index];
            } else {
              scene.tweens.add({
                targets: sprite.container,
                x: targetX,
                y: config.y,
                angle: Phaser.Math.Between(-5, 5),
                duration: 280,
                ease: 'Cubic.easeOut',
              });
              const wasHidden = sprite.container.getData('hidden');
              if (wasHidden && !isHole) {
                this.revealCard(sprite.container, card);
              } else if (!wasHidden) {
                const previous = sprite.container.getData('card');
                if (!previous || previous.rank !== card.rank || previous.suit !== card.suit) {
                  this.populateCard(sprite.container, card, false);
                }
              }
            }
            sprite.container.setData('card', card);
            sprite.container.setData('hidden', isHole);
          });
        }

        teardownHand(owner) {
          const scene = this.scene;
          const sprites = this.cardSprites[owner];
          if (!scene || !sprites) {
            return;
          }
          sprites.forEach((sprite) => {
            if (sprite.container) {
              sprite.container.removeAll(true);
              sprite.container.destroy();
            }
          });
          delete this.cardSprites[owner];
        }

        revealCard(container, card) {
          const scene = this.scene;
          if (!scene) {
            return;
          }
          scene.tweens.add({
            targets: container,
            scaleX: 0,
            duration: 160,
            ease: 'Quad.easeIn',
            onComplete: () => {
              this.populateCard(container, card, false);
              scene.tweens.add({
                targets: container,
                scaleX: 1,
                duration: 180,
                ease: 'Quad.easeOut',
              });
            },
          });
        }
      }

      const statusEl = document.getElementById('status');
      const balanceEl = document.getElementById('balance');
      const sessionInfoEl = document.getElementById('session-info');
      const outcomeEl = document.getElementById('outcome');
      const dealerInfoEl = document.getElementById('dealer-info');
      const playerHandsContainer = document.getElementById('player-hands-info');
      const sidebetSummaryEl = document.getElementById('sidebet-summary');
      const betInput = document.getElementById('bet');
      const hitButton = document.getElementById('hit-button');
      const standButton = document.getElementById('stand-button');
      const doubleButton = document.getElementById('double-button');
      const splitButton = document.getElementById('split-button');
      const clearBetsButton = document.getElementById('clear-bets');
      const fullscreenButton = document.getElementById('fullscreen-button');
      const betSpotButtons = Array.from(document.querySelectorAll('.bet-spot'));
      const logoutButton = document.getElementById('logout-button');
      const guestButton = document.getElementById('guest-button');
      const authOpenButton = document.getElementById('auth-open');
      const authOverlay = document.getElementById('auth-overlay');
      const authCloseButton = document.getElementById('auth-close');
      const authTabButtons = Array.from(document.querySelectorAll('[data-auth-tab]'));
      const authForms = {
        login: document.getElementById('login-form'),
        signup: document.getElementById('signup-form'),
      };
      const chipButtons = Array.from(document.querySelectorAll('.chip-button'));
      const animator = window.Phaser ? new BlackjackAnimator('phaser-stage') : null;
      if (!animator) {
        document.getElementById('phaser-stage').innerHTML = '<p class=\"muted\">Chargement Phaser impossible. Les cartes seront statiques.</p>';
      }

      let token = window.localStorage.getItem('openblackjack_token');
      let profile = null;
      let sessionId = null;
      let lastState = null;
      let bettingLocked = false;
      let selectedChip = null;
      const betSpotsState = {
        main: 0,
        pair: 0,
        suited_pair: 0,
      };

      function persistToken(value) {
        if (!value) {
          window.localStorage.removeItem('openblackjack_token');
        } else {
          window.localStorage.setItem('openblackjack_token', value);
        }
      }

      function authHeaders() {
        if (!token) {
          return {};
        }
        return { Authorization: `Bearer ${token}` };
      }

      function updateBetSpotDisplays() {
        betInput.value = betSpotsState.main;
        betSpotButtons.forEach((button) => {
          const spot = button.dataset.spot;
          const amountLabel = button.querySelector('[data-spot-amount]');
          const amount = betSpotsState[spot] || 0;
          if (amountLabel) {
            amountLabel.textContent = formatCurrency(amount);
          }
          button.classList.toggle('bet-spot--locked', bettingLocked);
        });
      }

      function resetBetSpots() {
        betSpotsState.main = 0;
        betSpotsState.pair = 0;
        betSpotsState.suited_pair = 0;
        updateBetSpotDisplays();
        selectedChip = null;
        clearChipSelection();
      }

      function setBettingLocked(lock) {
        bettingLocked = lock;
        updateBetSpotDisplays();
      }

      function formatCurrency(value) {
        return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'USD' }).format(value);
      }

      function setStatus(message, tone = 'info') {
        statusEl.textContent = message;
        statusEl.dataset.tone = tone;
        statusEl.animate(
          [
            { transform: 'scale(0.98)', opacity: 0.6 },
            { transform: 'scale(1)', opacity: 1 },
          ],
          { duration: 220, easing: 'ease-out' }
        );
      }

      let activeAuthTab = 'login';

      function setActiveAuthTab(tab) {
        if (!authForms[tab]) {
          return;
        }
        activeAuthTab = tab;
        authTabButtons.forEach((button) => {
          const isActive = button.dataset.authTab === tab;
          button.classList.toggle('auth-tab--active', isActive);
          button.setAttribute('aria-selected', String(isActive));
        });
        Object.entries(authForms).forEach(([name, form]) => {
          const isActive = name === tab;
          form.classList.toggle('auth-form--active', isActive);
          if (isActive) {
            const focusTarget = form.querySelector('input');
            window.requestAnimationFrame(() => focusTarget && focusTarget.focus({ preventScroll: true }));
          }
        });
      }

      function hideAuthOverlay() {
        if (!authOverlay) {
          return;
        }
        authOverlay.classList.remove('auth-overlay--active');
        authOverlay.setAttribute('aria-hidden', 'true');
      }

      function showAuthOverlay(tab = activeAuthTab || 'login') {
        if (!authOverlay || profile) {
          return;
        }
        setActiveAuthTab(tab);
        authOverlay.classList.add('auth-overlay--active');
        authOverlay.setAttribute('aria-hidden', 'false');
      }

      function updateOutcomeTone(outcome) {
        outcomeEl.classList.remove('outcome--win', 'outcome--loss', 'outcome--push');
        if (!outcome) {
          return;
        }
        const tone = {
          player_blackjack: 'outcome--win',
          player_win: 'outcome--win',
          dealer_bust: 'outcome--win',
          dealer_blackjack: 'outcome--loss',
          dealer_win: 'outcome--loss',
          player_bust: 'outcome--loss',
          push: 'outcome--push',
          mixed: 'outcome--push',
        }[outcome];
        if (tone) {
          outcomeEl.classList.add(tone);
        }
      }

      function clearChipSelection() {
        chipButtons.forEach((button) => button.classList.remove('chip-button--active'));
        selectedChip = null;
      }

      function updateAuthUI() {
        if (profile) {
          balanceEl.textContent = `Connecté en tant que ${profile.username} — Solde : ${formatCurrency(profile.balance)}`;
          logoutButton.disabled = false;
          logoutButton.classList.remove('hidden');
          betInput.disabled = false;
          setBettingLocked(false);
          if (authOpenButton) {
            authOpenButton.classList.add('hidden');
            authOpenButton.disabled = true;
          }
          if (guestButton) {
            guestButton.disabled = true;
            guestButton.classList.add('hidden');
          }
          hideAuthOverlay();
        } else {
          balanceEl.textContent = 'Mode invité — mises désactivées.';
          logoutButton.disabled = true;
          logoutButton.classList.add('hidden');
          betInput.value = '0';
          betInput.disabled = true;
          resetBetSpots();
          setBettingLocked(true);
          if (authOpenButton) {
            authOpenButton.classList.remove('hidden');
            authOpenButton.disabled = false;
          }
          if (guestButton) {
            guestButton.disabled = false;
            guestButton.classList.remove('hidden');
          }
          if (authOverlay && !authOverlay.classList.contains('auth-overlay--active')) {
            authOverlay.setAttribute('aria-hidden', 'true');
          }
        }
      }

      function updateDealerInfo(hand, options = {}) {
        if (!dealerInfoEl) {
          return;
        }
        const totalEl = dealerInfoEl.querySelector('.hand-total');
        const statusEl = dealerInfoEl.querySelector('.hand-status');
        if (!totalEl || !statusEl) {
          return;
        }
        if (!hand.cards.length) {
          totalEl.textContent = 'En attente…';
          statusEl.textContent = '';
          dealerInfoEl.classList.remove('hand--concealed');
          return;
        }
        if (options.hideHoleCard) {
          totalEl.textContent = 'Total : ??';
          statusEl.textContent = 'Le croupier cache une carte.';
          dealerInfoEl.classList.add('hand--concealed');
        } else {
          totalEl.textContent = `Total : ${hand.value}`;
          statusEl.textContent = '';
          dealerInfoEl.classList.remove('hand--concealed');
        }
      }

      function renderPlayerHands(hands) {
        if (!playerHandsContainer) {
          return;
        }
        playerHandsContainer.innerHTML = '';
        if (!hands.length) {
          const placeholder = document.createElement('div');
          placeholder.className = 'player-hand-card';
          placeholder.innerHTML = '<h3>JOUEUR</h3><div class="hand-total">En attente…</div>';
          playerHandsContainer.appendChild(placeholder);
          return;
        }
        hands.forEach((hand, index) => {
          const card = document.createElement('div');
          card.className = 'player-hand-card';
          if (hand.is_active) {
            card.classList.add('player-hand-card--active');
          }
          const title = document.createElement('h3');
          title.textContent = `Main ${index + 1}`;
          const total = document.createElement('div');
          total.className = 'hand-total';
          total.textContent = `Total : ${hand.value}`;
          const bet = document.createElement('div');
          bet.className = 'hand-status';
          const betLabel = hand.is_doubled ? 'Mise (doublée)' : 'Mise';
          bet.textContent = `${betLabel} : ${formatCurrency(hand.bet)}`;
          if (hand.result) {
            const resultMap = {
              player_blackjack: 'Blackjack !',
              player_win: 'Victoire',
              dealer_bust: 'Croupier saute',
              dealer_win: 'Défaite',
              dealer_blackjack: 'Blackjack du croupier',
              player_bust: 'Buste',
              push: 'Égalité',
            };
            const result = document.createElement('div');
            result.className = 'hand-status';
            result.textContent = `Résultat : ${resultMap[hand.result] || hand.result.replace('_', ' ')}`;
            card.append(title, total, bet, result);
          } else {
            card.append(title, total, bet);
          }
          playerHandsContainer.appendChild(card);
        });
      }

      function renderSideBets(sideBets) {
        if (!sidebetSummaryEl) {
          return;
        }
        sidebetSummaryEl.innerHTML = '';
        const entries = Object.entries(sideBets || {});
        if (!entries.length) {
          return;
        }
        entries.forEach(([key, info]) => {
          if (!info || (!info.bet && info.result === 'inactive')) {
            return;
          }
          const chip = document.createElement('span');
          chip.className = 'sidebet-chip';
          chip.dataset.result = info.result || 'inactive';
          const label = info.label || key;
          const amount = formatCurrency(info.bet || 0);
          const payout = info.payout ? formatCurrency(info.payout) : null;
          if (info.description) {
            chip.title = info.description;
          }
          chip.textContent = payout && info.result === 'win'
            ? `${label}: ${amount} → ${payout}`
            : `${label}: ${amount}`;
          sidebetSummaryEl.appendChild(chip);
        });
      }

      function formatOutcome(outcome, isOver) {
        if (!outcome) {
          return isOver ? 'Main terminée.' : 'Main en cours — jouez !';
        }
        const mapping = {
          player_blackjack: 'Blackjack ! Vous gagnez 3:2.',
          player_win: 'Vous gagnez !',
          dealer_bust: 'Le croupier saute — victoire !',
          dealer_blackjack: 'Blackjack du croupier.',
          dealer_win: 'Le croupier gagne.',
          player_bust: 'Vous dépassez 21 — perdu.',
          push: "Egalité — la mise est rendue.",
          mixed: 'Résultats mixtes — vérifiez chaque main.',
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
          let message = 'Requête échouée.';
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
            throw new Error('Impossible de récupérer le profil.');
          }
          profile = await response.json();
          updateAuthUI();
          setStatus('Connexion réussie.', 'success');
        } catch (error) {
          token = null;
          profile = null;
          persistToken(null);
          updateAuthUI();
          setStatus(error.message, 'error');
        }
      }

      function handleGameState(data) {
        sessionId = data.session_id;
        lastState = data;
        const shortId = sessionId ? sessionId.slice(0, 8) : '—';
        const sideBetTotal = Object.values(data.side_bets || {}).reduce((sum, entry) => sum + (entry.bet || 0), 0);
        const totalWager = (data.bet || 0) + sideBetTotal;
        const betLabel = totalWager ? ` • Mises : ${formatCurrency(totalWager)}` : '';
        sessionInfoEl.innerHTML = `Session <span>${shortId}${sessionId ? '…' : ''}</span>${betLabel}`;
        const hideDealerCard = !data.is_over && data.dealer_hand.cards.length > 1;
        updateDealerInfo(data.dealer_hand, { hideHoleCard: hideDealerCard });
        renderPlayerHands(data.player_hands || []);
        renderSideBets(data.side_bets || {});
        if (animator) {
          animator.updateHands(data.player_hands || [], data.dealer_hand, { hideHoleCard: hideDealerCard });
        }
        outcomeEl.textContent = formatOutcome(data.outcome, data.is_over);
        updateOutcomeTone(data.outcome);
        if (typeof data.balance === 'number' && profile) {
          profile.balance = data.balance;
          updateAuthUI();
        }
        const activeHand =
          typeof data.active_hand_index === 'number' && data.player_hands
            ? data.player_hands[data.active_hand_index]
            : null;
        const canAct = Boolean(activeHand) && !activeHand.result && !data.is_over;
        hitButton.disabled = !canAct;
        standButton.disabled = !canAct;
        doubleButton.disabled = !canAct || !activeHand?.can_double || !profile;
        splitButton.disabled = !canAct || !activeHand?.can_split || !profile;
        setBettingLocked(profile ? !data.is_over : true);
        return data;
      }

      document.getElementById('signup-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const username = document.getElementById('signup-username').value.trim();
        const password = document.getElementById('signup-password').value.trim();
        if (!username || !password) {
          setStatus('Veuillez indiquer un nom et un mot de passe.', 'error');
          return;
        }
        try {
          const data = await postJson('/signup', { username, password });
          token = data.token;
          persistToken(token);
          await fetchProfile();
          hideAuthOverlay();
          setStatus('Compte créé ! Une nouvelle main vous attend.', 'success');
        } catch (error) {
          setStatus(error.message, 'error');
        }
      });

      document.getElementById('login-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        const username = document.getElementById('login-username').value.trim();
        const password = document.getElementById('login-password').value.trim();
        if (!username || !password) {
          setStatus('Entrez vos identifiants pour vous connecter.', 'error');
          return;
        }
        try {
          const data = await postJson('/login', { username, password });
          token = data.token;
          persistToken(token);
          await fetchProfile();
          hideAuthOverlay();
          setStatus('Connexion réussie. Bonne chance !', 'success');
        } catch (error) {
          setStatus(error.message, 'error');
        }
      });

      if (guestButton) {
        guestButton.addEventListener('click', () => {
          token = null;
          profile = null;
          persistToken(null);
          hideAuthOverlay();
          updateAuthUI();
          setStatus('Mode invité activé. Les mises sont à zéro.', 'info');
        });
      }

      logoutButton.addEventListener('click', () => {
        token = null;
        profile = null;
        persistToken(null);
        updateAuthUI();
        showAuthOverlay('login');
        setStatus('Vous êtes déconnecté.', 'info');
      });

      document.getElementById('start-form').addEventListener('submit', async (event) => {
        event.preventDefault();
        if (lastState && !lastState.is_over) {
          setStatus('Terminez la main actuelle avant de redistribuer.', 'warning');
          return;
        }
        const mainBet = betSpotsState.main || 0;
        const sideBetsPayload = {};
        ['pair', 'suited_pair'].forEach((key) => {
          const value = betSpotsState[key];
          if (value) {
            sideBetsPayload[key] = value;
          }
        });
        const total = mainBet + Object.values(sideBetsPayload).reduce((sum, value) => sum + value, 0);
        if (!profile && total > 0) {
          setStatus('Les invités doivent laisser la mise à 0.', 'error');
          return;
        }
        try {
          const data = await postJson('/game/start', { bet: mainBet, side_bets: sideBetsPayload });
          handleGameState(data);
          clearChipSelection();
          setStatus('Cartes distribuées — bonne chance !', 'success');
        } catch (error) {
          setStatus(error.message, 'error');
        }
      });

      hitButton.addEventListener('click', async () => {
        if (!sessionId || !lastState || typeof lastState.active_hand_index !== 'number') {
          setStatus('Commencez une main avant de tirer.', 'error');
          return;
        }
        try {
          const data = await postJson('/game/hit', {
            session_id: sessionId,
            hand_index: lastState.active_hand_index,
          });
          handleGameState(data);
          setStatus('Carte piochée.', 'info');
        } catch (error) {
          setStatus(error.message, 'error');
        }
      });

      standButton.addEventListener('click', async () => {
        if (!sessionId || !lastState || typeof lastState.active_hand_index !== 'number') {
          setStatus('Commencez une main avant de rester.', 'error');
          return;
        }
        try {
          const data = await postJson('/game/stand', {
            session_id: sessionId,
            hand_index: lastState.active_hand_index,
          });
          handleGameState(data);
          setStatus('Main résolue.', 'info');
        } catch (error) {
          setStatus(error.message, 'error');
        }
      });

      doubleButton.addEventListener('click', async () => {
        if (!sessionId || !lastState || typeof lastState.active_hand_index !== 'number') {
          setStatus('Aucune main active à doubler.', 'error');
          return;
        }
        try {
          const data = await postJson('/game/double', {
            session_id: sessionId,
            hand_index: lastState.active_hand_index,
          });
          handleGameState(data);
          setStatus('Double appliqué.', 'info');
        } catch (error) {
          setStatus(error.message, 'error');
        }
      });

      splitButton.addEventListener('click', async () => {
        if (!sessionId || !lastState || typeof lastState.active_hand_index !== 'number') {
          setStatus('Aucune main active à séparer.', 'error');
          return;
        }
        try {
          const data = await postJson('/game/split', {
            session_id: sessionId,
            hand_index: lastState.active_hand_index,
          });
          handleGameState(data);
          setStatus('Main séparée.', 'info');
        } catch (error) {
          setStatus(error.message, 'error');
        }
      });

      chipButtons.forEach((button) => {
        button.addEventListener('click', () => {
          const amount = parseInt(button.dataset.chip, 10) || 0;
          if (!profile) {
            setStatus('Connectez-vous pour miser avec des jetons.', 'warning');
            return;
          }
          clearChipSelection();
          selectedChip = amount;
          button.classList.add('chip-button--active');
        });
      });

      betSpotButtons.forEach((button) => {
        button.addEventListener('click', () => {
          if (bettingLocked) {
            setStatus('Les mises sont verrouillées pendant la main en cours.', 'warning');
            return;
          }
          if (!profile) {
            setStatus('Connectez-vous pour placer des mises.', 'warning');
            return;
          }
          if (!selectedChip) {
            setStatus('Choisissez un jeton avant de miser.', 'warning');
            return;
          }
          const spot = button.dataset.spot;
          betSpotsState[spot] = (betSpotsState[spot] || 0) + selectedChip;
          updateBetSpotDisplays();
        });
        button.addEventListener('contextmenu', (event) => {
          event.preventDefault();
          if (bettingLocked) {
            setStatus('Les mises sont verrouillées pendant la main en cours.', 'warning');
            return;
          }
          const spot = button.dataset.spot;
          if (!selectedChip) {
            betSpotsState[spot] = 0;
          } else {
            betSpotsState[spot] = Math.max(0, (betSpotsState[spot] || 0) - selectedChip);
          }
          updateBetSpotDisplays();
        });
      });

      if (clearBetsButton) {
        clearBetsButton.addEventListener('click', () => {
          if (bettingLocked) {
            setStatus('Attendez la fin de la main pour ajuster vos mises.', 'warning');
            return;
          }
          resetBetSpots();
          setStatus('Mises réinitialisées.', 'info');
        });
      }

      if (fullscreenButton) {
        const updateFullscreenLabel = () => {
          fullscreenButton.textContent = document.fullscreenElement
            ? 'Quitter le plein écran'
            : 'Plein écran';
        };
        fullscreenButton.addEventListener('click', () => {
          if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen?.();
          } else {
            document.exitFullscreen?.();
          }
        });
        document.addEventListener('fullscreenchange', updateFullscreenLabel);
        updateFullscreenLabel();
      }

      authTabButtons.forEach((button) => {
        button.addEventListener('click', () => {
          const tab = button.dataset.authTab;
          if (tab) {
            setActiveAuthTab(tab);
          }
        });
      });

      if (authOpenButton) {
        authOpenButton.addEventListener('click', () => {
          showAuthOverlay('login');
          setStatus('Connectez-vous ou créez un compte pour miser.', 'info');
        });
      }

      if (authCloseButton) {
        authCloseButton.addEventListener('click', () => {
          hideAuthOverlay();
          setStatus('Vous pouvez jouer en invité ou miser en vous connectant.', 'info');
        });
      }

      if (authOverlay) {
        authOverlay.addEventListener('click', (event) => {
          if (event.target === authOverlay) {
            hideAuthOverlay();
          }
        });
      }

      document.addEventListener('keydown', (event) => {
        if (!authOverlay) {
          return;
        }
        if (event.key === 'Escape' && authOverlay.classList.contains('auth-overlay--active')) {
          hideAuthOverlay();
        }
      });

      document.addEventListener('gesturestart', (event) => {
        event.preventDefault();
      });

      document.addEventListener('dblclick', (event) => {
        if (event.target.closest('button, input')) {
          event.preventDefault();
        }
      });

      updateBetSpotDisplays();
      renderPlayerHands([]);
      renderSideBets({});
      updateAuthUI();
      if (token) {
        fetchProfile();
      } else {
        showAuthOverlay('login');
        setStatus('Jouez en invité ou connectez-vous pour miser.');
      }
    </script>
  </body>
</html>
"""


@router.get("/", response_class=HTMLResponse)
def index() -> str:
    """Serve the responsive Blackjack frontend."""
    return INDEX_HTML

