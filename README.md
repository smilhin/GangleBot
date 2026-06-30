# GangleBot

A Telegram bot that recommends movies and food based on your mood, powered by an LLM (via Groq's OpenAI-compatible API).

## Features

- **Mood-based recommendations** — pick from Happy, Sad, Nostalgic, or Angry, and the bot tailors a suggestion to match.
- **Genre selection** — choose between Movie, Anime, Cartoon, or Series.
- **AI-generated picks** — uses an LLM (`llama-3.3-70b-versatile` via Groq) to generate a creative, spoiler-light recommendation with a title, year, and description.
- **Poster lookup** — automatically fetches a poster image for the recommended title and sends it alongside the description.
- **Keep the recommendations coming** — after each suggestion, the bot asks if you'd like another, and avoids repeating movies it's already recommended in the session.
- **Simple command interface**

## Commands

| Command | Description |
|---|---|
| `/start` | Start the bot |
| `/help` | Show available commands |
| `/recommend_movie` | Start a guided mood + genre flow to get a movie recommendation |
| `/recommend_food` | *(planned)* Food recommendations |

## How it works

1. User runs `/recommend_movie`.
2. Bot asks for the user's current mood (reply-keyboard buttons).
3. Bot asks what type of content they want (movie, anime, cartoon, series).
4. The mood + genre are sent to the LLM with a prompt asking for a single creative recommendation in JSON format (title, year, description, poster URL).
5. The bot fetches a poster image and replies with the recommendation.
6. The bot asks if the user wants another recommendation, repeating the flow while excluding previously suggested titles.

## Project structure

```
.
├── main.py     # Bot entrypoint, command/message handler registration
├── movie.py    # Movie recommendation conversation flow + LLM integration
├── helpers.py  # Helper utilities (e.g. poster image lookup)
└── config.py   # Shared API client configuration
```

## Setup

### Prerequisites

- Python 3.10+
- A Telegram bot token ([create one via @BotFather](https://t.me/BotFather))
- A Groq API key ([console.groq.com](https://console.groq.com))

### Installation

```bash
git clone https://github.com/smilhin/GangleBot.git
cd GangleBot
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
TELEGRAM_BOT_TOKEN=...
GROQ_API_KEY=...
TMDB_API_KEY=...
```

### Running the bot

```bash
python main.py
```

## License

MIT (or update to match your preferred license)