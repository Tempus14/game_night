from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


@dataclass(frozen=True)
class Team:
    id: str
    name: str
    color: str = "#2F80ED"

    @classmethod
    def create(cls, name: str, color: str = "#2F80ED") -> "Team":
        return cls(id=new_id("team"), name=name.strip(), color=color)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Team":
        return cls(
            id=str(data["id"]),
            name=str(data["name"]),
            color=str(data.get("color", "#2F80ED")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "name": self.name, "color": self.color}


@dataclass(frozen=True)
class GameResult:
    id: str
    name: str
    mode: str
    ranking: dict[str, int]
    awarded_points: dict[str, int]
    input_mode: str = "point"
    point_direction: str = "score"
    game_points: dict[str, int] = field(default_factory=dict)
    rounds: list[dict[str, int]] = field(default_factory=list)
    details: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        name: str,
        mode: str,
        ranking: dict[str, int],
        awarded_points: dict[str, int],
        input_mode: str = "point",
        point_direction: str = "score",
        game_points: dict[str, int] | None = None,
        rounds: list[dict[str, int]] | None = None,
        details: dict[str, Any] | None = None,
    ) -> "GameResult":
        return cls(
            id=new_id("game"),
            name=name.strip(),
            mode=mode,
            ranking=ranking,
            awarded_points=awarded_points,
            input_mode=input_mode,
            point_direction=point_direction,
            game_points=game_points or {},
            rounds=rounds or [],
            details=details or {},
        )

    @classmethod
    def create_direct_ranking(
        cls,
        name: str,
        ranking: dict[str, int],
        awarded_points: dict[str, int],
    ) -> "GameResult":
        return cls.create(
            name=name,
            mode="simple",
            ranking=ranking,
            awarded_points=awarded_points,
            input_mode="rank",
            point_direction="score",
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GameResult":
        return cls(
            id=str(data["id"]),
            name=str(data["name"]),
            mode=str(data.get("mode", "direct_ranking")),
            ranking={
                str(team_id): int(rank)
                for team_id, rank in data.get("ranking", {}).items()
            },
            awarded_points={
                str(team_id): int(points)
                for team_id, points in data.get("awarded_points", {}).items()
            },
            input_mode=str(data.get("input_mode", "rank")),
            point_direction=str(data.get("point_direction", "score")),
            game_points={
                str(team_id): int(points)
                for team_id, points in data.get("game_points", {}).items()
            },
            rounds=[
                {
                    str(team_id): int(points)
                    for team_id, points in round_scores.items()
                }
                for round_scores in data.get("rounds", [])
            ],
            details=dict(data.get("details", {})),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "mode": self.mode,
            "input_mode": self.input_mode,
            "point_direction": self.point_direction,
            "ranking": self.ranking,
            "game_points": self.game_points,
            "rounds": self.rounds,
            "details": self.details,
            "awarded_points": self.awarded_points,
        }


@dataclass(frozen=True)
class AppState:
    teams: list[Team] = field(default_factory=list)
    games: list[GameResult] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AppState":
        return cls(
            teams=[Team.from_dict(team) for team in data.get("teams", [])],
            games=[
                GameResult.from_dict(game)
                for game in data.get("games", [])
            ],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "teams": [team.to_dict() for team in self.teams],
            "games": [game.to_dict() for game in self.games],
        }
