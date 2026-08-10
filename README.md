# Naruto-mcp-V2 — Minimal README

This repository is a Naruto-themed RPG simulation engine that uses local LLM (Ollama) only for narrative output. Game logic (engine/*.py) is the source of truth; the AI only narrates results.

Quick start (local):

1. Create a Python 3 virtual environment and activate it:

   python3 -m venv venv
   source venv/bin/activate

2. Install dependencies:

   pip install -r requirements.txt

3. (Optional) If you use Ollama locally, ensure it is running and the model `deepseek-coder-v2:16b-lite-instruct-q4_K_M` is available. If using environment variables, copy `.env.example` to `.env` and edit.

4. Run the app:

   python app.py

Notes:
- The game uses `memory/` JSON files as its lightweight datastore. A sample `memory/player.json` is provided.
- Do not let the LLM decide game state — engines under `engine/` compute results; the AI only narrates via `ai/`.
