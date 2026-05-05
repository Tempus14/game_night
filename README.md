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

On Windows you can also run:

```powershell
.\run_streamlit.cmd
```

The app stores its state in `data/state.json` and writes timestamped backups to
`data/backups/` after saves.

## Current Features

- Configure teams at the start of the evening.
- Show a large-screen-friendly overall scoreboard.
- Add direct-ranking game results.
- Allow competition-ranking ties, such as `1, 2, 2, 4`.
- Award game-night points using `num_teams - rank`.
- Keep automatic JSON saves and backups.
