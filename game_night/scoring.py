from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from game_night.models import AppState, Team


@dataclass(frozen=True)
class RankingValidation:
    is_valid: bool
    message: str


@dataclass(frozen=True)
class ScoreboardRow:
    rank: int
    team_id: str
    team_name: str
    team_color: str
    total_points: int
    games_played: int
    games_won: int


def validate_competition_ranking(
    ranks_by_team: dict[str, int],
    team_ids: list[str],
) -> RankingValidation:
    if not team_ids:
        return RankingValidation(False, "Add at least one team first.")

    expected_team_ids = set(team_ids)
    submitted_team_ids = set(ranks_by_team)

    missing = expected_team_ids - submitted_team_ids
    extra = submitted_team_ids - expected_team_ids

    if missing:
        return RankingValidation(False, "Every team needs a rank.")

    if extra:
        return RankingValidation(False, "Ranking contains unknown teams.")

    ranks = list(ranks_by_team.values())
    team_count = len(team_ids)

    if any(rank < 1 or rank > team_count for rank in ranks):
        return RankingValidation(
            False,
            f"Ranks must be between 1 and {team_count}.",
        )

    submitted = sorted(ranks)
    expected = _expected_competition_ranks(submitted)

    if submitted != expected:
        return RankingValidation(
            False,
            "Invalid tie pattern. Use competition ranking such as "
            "1, 2, 2, 4.",
        )

    return RankingValidation(True, "Ranking is valid.")


def award_points(
    ranks_by_team: dict[str, int],
    team_count: int,
) -> dict[str, int]:
    return {
        team_id: max(team_count - rank, 0)
        for team_id, rank in ranks_by_team.items()
    }


def ranking_from_scores(
    scores_by_team: dict[str, int],
    *,
    higher_is_better: bool = True,
) -> dict[str, int]:
    sorted_items = sorted(
        scores_by_team.items(),
        key=lambda item: (
            -item[1] if higher_is_better else item[1],
            item[0],
        ),
    )
    sorted_scores = [score for _, score in sorted_items]
    ranks = competition_ranks_for_scores(
        sorted_scores,
        higher_is_better=higher_is_better,
    )

    return {
        team_id: rank
        for (team_id, _), rank in zip(sorted_items, ranks)
    }


def sum_round_scores(
    rounds: list[dict[str, int]],
    team_ids: list[str],
) -> dict[str, int]:
    totals = {team_id: 0 for team_id in team_ids}

    for round_scores in rounds:
        for team_id in team_ids:
            totals[team_id] += round_scores.get(team_id, 0)

    return totals


def build_scoreboard(state: AppState) -> list[ScoreboardRow]:
    totals = {team.id: 0 for team in state.teams}
    games_played = {team.id: 0 for team in state.teams}
    games_won = {team.id: 0 for team in state.teams}

    for game in state.games:
        for team_id, points in game.awarded_points.items():
            if team_id in totals:
                totals[team_id] += points
                games_played[team_id] += 1

        for team_id, rank in game.ranking.items():
            if team_id in games_won and rank == 1:
                games_won[team_id] += 1

    sorted_teams = sorted(
        state.teams,
        key=lambda team: (-totals[team.id], team.name.lower()),
    )

    ranks = competition_ranks_for_scores(
        [totals[team.id] for team in sorted_teams],
        higher_is_better=True,
    )

    return [
        ScoreboardRow(
            rank=rank,
            team_id=team.id,
            team_name=team.name,
            team_color=team.color,
            total_points=totals[team.id],
            games_played=games_played[team.id],
            games_won=games_won[team.id],
        )
        for team, rank in zip(sorted_teams, ranks)
    ]


def competition_ranks_for_scores(
    scores: list[int],
    *,
    higher_is_better: bool,
) -> list[int]:
    if not scores:
        return []

    ordered_scores = scores
    if higher_is_better:
        ordered_scores = sorted(scores, reverse=True)
    else:
        ordered_scores = sorted(scores)

    ranks_by_score = {}
    position = 1

    for score, count in Counter(ordered_scores).items():
        ranks_by_score[score] = position
        position += count

    return [ranks_by_score[score] for score in scores]


def team_name_by_id(teams: list[Team]) -> dict[str, str]:
    return {team.id: team.name for team in teams}


def _expected_competition_ranks(submitted: list[int]) -> list[int]:
    expected = []
    position = 1

    for rank, count in Counter(submitted).items():
        expected.extend([position] * count)
        position += count

        if rank != expected[-1]:
            break

    return expected
