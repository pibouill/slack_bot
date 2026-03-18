# ⚠️ Slack Blindtest Bot (WORK IN PROGRESS) ⚠️

> **Note:** This project is currently in early development. Some features may be unstable, incomplete, or undergoing significant refactoring. Use at your own risk.

A Slack bot built with the [Bolt for Python](https://slack.dev/bolt-python/tutorial/getting-started) framework that handles blindtest submissions and manages a leaderboard.

## Features
*   **Leaderboard**: Track user scores for correct submissions.
*   **Slash Commands**:
    *   `/leaderboard`: Display the top 5 ranking users.
    *   `/get_rank <user_login>`: Get the specific rank and score of a user.
*   **Interactive Mentions**: Responds to @mentions for submissions.
*   **Socket Mode**: Easy setup without needing a public URL/ngrok for development.

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone git@github.com:pibouill/slack_bot.git
cd slack_bot
```

### 2. Create and Activate Virtual Environment
Using a virtual environment (`venv`) keeps your project dependencies isolated.

**On Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Slack Configuration

To run this bot, you need to create a Slack App and obtain two specific tokens.

### How to get Slack Tokens
1.  Go to [Slack API: Your Apps](https://api.slack.com/apps) and click **Create New App** (from scratch).
2.  **Bot User Token (`SLACK_BOT_TOKEN`)**:
    *   Go to **OAuth & Permissions**.
    *   Under **Scopes**, add `app_mentions:read`, `chat:write`, `commands`, and `users:read`.
    *   Install the app to your workspace.
    *   Copy the **Bot User OAuth Token** (starts with `xoxb-`).
3.  **App-Level Token (`SLACK_APP_TOKEN`)**:
    *   Go to **Settings > Basic Information**.
    *   Under **App-Level Tokens**, click **Generate Token and Scopes**.
    *   Name it (e.g., `socket_mode`) and add the `connections:write` scope.
    *   Copy the generated token (starts with `xapp-`).
4.  **Enable Socket Mode**:
    *   Go to **Settings > Socket Mode** and toggle **Enable Socket Mode** to ON.
5.  **Enable Event Subscriptions**:
    *   Toggle **Enable Events** to ON.
    *   Under **Subscribe to bot events**, add `app_mention` and `message.channels`.
6.  **Slash Commands**:
    *   Go to **Slash Commands** and create `/leaderboard` and `/get_rank`.

---

## Environment Variables

Create a `.env` file in the root directory (this file is ignored by Git for security):

```env
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token
```

---

## Running the Bot

Ensure your virtual environment is activated, then run:

```bash
python app.py
```

The bot will prompt for a `valid_input` (the correct answer for the blindtest) in the terminal and then start listening for Slack events.
