from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path

from game_night.models import AppState


STATE_PATH = Path("data/state.json")
BACKUP_DIR = Path("data/backups")


def load_state(path: Path = STATE_PATH) -> AppState:
    if not path.exists():
        return AppState()

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return AppState.from_dict(data)


def save_state(state: AppState, path: Path = STATE_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(".json.tmp")

    with temp_path.open("w", encoding="utf-8") as file:
        json.dump(state.to_dict(), file, indent=2)
        file.write("\n")

    temp_path.replace(path)
    write_backup(path)


def write_backup(path: Path = STATE_PATH) -> Path | None:
    if not path.exists():
        return None

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    backup_path = BACKUP_DIR / f"state_{timestamp}.json"
    shutil.copy2(path, backup_path)
    return backup_path
