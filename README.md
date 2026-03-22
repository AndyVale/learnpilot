# LearnPilot

AI-powered personalised learning lab that adapts to each learner in real time.
Combines natural language processing, adaptive curricula, intelligent tutoring,
and progress tracking to create a dynamic educational experience with interactive
explanations, guided practice, and continuous feedback.

Uses **Cloudflare AI Python Workers** (`@cf/meta/llama-3.1-8b-instruct`).

---

## Architecture

```
Client  ──POST──▶  Cloudflare Python Worker (src/worker.py)
                         │
                         │  env.AI  (Workers AI binding)
                         ▼
              @cf/meta/llama-3.1-8b-instruct
```

The entire application runs at the edge as a single Cloudflare Python Worker.
No server infrastructure, no databases, no external dependencies.

---

## API Endpoints

| Method | Path            | Description                                            |
|--------|-----------------|--------------------------------------------------------|
| POST   | `/ai/chat`      | Continue a real-time tutoring conversation             |
| POST   | `/ai/explain`   | Explain a concept (adapts to skill level + style)      |
| POST   | `/ai/practice`  | Generate a practice question                           |
| POST   | `/ai/evaluate`  | Evaluate a learner's answer (returns score 0–1)        |
| POST   | `/ai/path`      | Generate a personalised ordered learning path          |
| POST   | `/ai/progress`  | Produce AI-driven progress insights                    |
| POST   | `/ai/adapt`     | Recommend a difficulty adjustment from recent scores   |
| POST   | `/ai/summary`   | Summarise a completed tutoring session                 |
| GET    | `/health`       | Liveness check                                         |

---

## Request / Response Examples

### `POST /ai/explain`

```json
// Request
{
  "concept": "recursion",
  "skill_level": "beginner",
  "learning_style": "visual",
  "context": "We are studying Python functions."
}

// Response
"1. **Core Explanation** – Recursion is when a function calls itself…"
```

### `POST /ai/evaluate`

```json
// Request
{
  "question": "What is a Python decorator?",
  "answer": "A function that wraps another function to add behaviour.",
  "topic": "Python Functions"
}

// Response
{
  "score": 0.85,
  "feedback": "Excellent! You captured the core concept. Consider also mentioning…",
  "correct_answer": "A decorator is a higher-order function that takes a function…"
}
```

### `POST /ai/path`

```json
// Request
{
  "topic": "Python Programming",
  "skill_level": "beginner",
  "learning_style": "kinesthetic",
  "goals": "I want to build web apps",
  "available_lessons": [
    {"id": 1, "title": "Variables",  "type": "theory",   "difficulty": "beginner"},
    {"id": 2, "title": "Functions",  "type": "theory",   "difficulty": "beginner"},
    {"id": 3, "title": "Mini-project", "type": "project", "difficulty": "beginner"}
  ]
}

// Response
{
  "ordered_lesson_ids": [1, 2, 3],
  "rationale": "Start with variables to build a foundation, then functions for reuse, then apply both in a mini-project."
}
```

### `POST /ai/adapt`

```json
// Request
{
  "topic": "Python",
  "current_difficulty": "beginner",
  "recent_scores": [0.9, 0.95, 0.88]
}

// Response
{
  "new_difficulty": "intermediate",
  "action": "increase",
  "reasoning": "Consistently high scores indicate readiness for more complex material."
}
```

---

## Project Structure

```
learnpilot/
├── src/
│   ├── worker.py          # Cloudflare Python Worker (Main entry point)
│   └── js_conversion.py   # JavaScript types conversion utilities
├── tests/
│   └── test_worker.py     # End-to-end and unit tests (pytest)
├── wrangler.jsonc         # Cloudflare Workers configuration
├── pyproject.toml         # Python project configuration (uv)
├── uv.lock                # Locked dependencies
├── LICENSE
└── README.md
```

---

## Getting Started

### Prerequisites

- [uv](https://docs.astral.sh/uv/) (Python package manager)
- [Node.js](https://nodejs.org/) ≥ 18
- A [Cloudflare account](https://dash.cloudflare.com/sign-up) with Workers AI enabled

### Deploy

```bash
# Authenticate with Cloudflare
pywrangler login

# Deploy the worker to the edge
uv run pywrangler deploy
```

Wrangler will print the live URL, e.g.
`https://learnpilot-ai.<your-subdomain>.workers.dev`.

### Local Development

```bash
uv run pywrangler dev
```

The worker starts on `http://localhost:8787`. All AI calls are proxied to
Cloudflare's remote AI service automatically during development.

---

## Running Tests

The tests use `pytest` and `requests` to verify the worker's behavior against a running instance (local or remote).

```bash
# Run tests
uv run pytest tests/ -v
```

---

## Environment Variables

Copy `.env.example` to `.env` and fill in your credentials. These are only
needed by the **Wrangler CLI** on your local machine; they are never bundled
into the deployed worker.

| Variable                  | Description                              |
|---------------------------|------------------------------------------|
| `CLOUDFLARE_ACCOUNT_ID`   | Your Cloudflare account ID               |
| `CLOUDFLARE_API_TOKEN`    | API token with Workers AI permission     |


Or you can simple login with `pywrangler login` in your terminal as said above.

---

## License

GNU General Public License v2 – see [LICENSE](LICENSE).
