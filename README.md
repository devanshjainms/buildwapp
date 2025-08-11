# WhatsApp Wedding Messenger (Simplified)

This is a minimal Flask + React implementation for sending WhatsApp messages to wedding guests using your own browser.

## Features

- Import contacts from an Excel `.xlsx` file.
- Generate personalised message templates with placeholders.
- Produce `wa.me` links for safe manual sending.
- SQLite storage via SQLAlchemy.

## Backend Setup

These commands have been tested on macOS (including MacBook Air).

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start the Flask API:

```bash
flask --app app run
```

The backend listens on `http://localhost:5000` and exposes JSON APIs for contacts and messages.

## Frontend Setup (React)

Install Node.js (for example via [Homebrew](https://brew.sh/)):

```bash
brew install node
```

Install dependencies and run the development server:

```bash
cd frontend
npm install
npm run dev
```

This starts a Vite-powered React app at `http://localhost:3000` which communicates with the Flask API.

## Testing

```bash
make test
```

## Excel Format

Columns: `FirstName`, `LastName`, `Phone`, `Tag`, optional `Custom1`, `Custom2`.

Example:

| FirstName | LastName | Phone      | Tag    | Custom1    |
|-----------|----------|------------|--------|------------|
| Alice     | Smith    | 1234567890 | Family | Vegetarian |

