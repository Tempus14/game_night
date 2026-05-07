# Game Night Scoreboard

A Streamlit app for running a team-based game show evening.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```powershell
streamlit run app.py
```

The app stores its state in `data/state.json` and writes timestamped backups to
`data/backups/` after saves.

## Theme

Change app colors in `.streamlit/config.toml`. The custom scoreboard CSS uses
Streamlit's own theme variables, including the basic color palette, so it
follows the configured Streamlit theme.

Use `game_night/theme.py` only for default team colors. The rest is managed in the `.streamlit/config.toml`.

## Current Features

- Configure teams at the start of the evening.
- Show a large-screen-friendly overall scoreboard.
- Add direct-ranking game results.
- Allow competition-ranking ties, such as `1, 2, 2, 4`.
- Award game-night points using `num_teams - rank`.
- Keep automatic JSON saves and backups.
- Support mulit-round games.
- Support rank, score point and penalty point input.
