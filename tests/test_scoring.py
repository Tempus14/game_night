import pytest

from game_night.models import AppState, GameResult, Team
from game_night.scoring import (
    award_points,
    build_scoreboard,
    cutting_penalty,
    cutting_round_winner_points,
    ranking_from_scores,
    resolve_tied_ranking,
    sum_round_scores,
    tied_rank_groups,
    validate_competition_ranking,
)


def test_validate_accepts_plain_ranking() -> None:
    ranks = {"a": 1, "b": 2, "c": 3, "d": 4}

    result = validate_competition_ranking(ranks, ["a", "b", "c", "d"])

    assert result.is_valid


def test_validate_accepts_ties_with_skipped_ranks() -> None:
    ranks = {"a": 1, "b": 2, "c": 2, "d": 4}

    result = validate_competition_ranking(ranks, ["a", "b", "c", "d"])

    assert result.is_valid


def test_validate_rejects_ties_without_skipped_ranks() -> None:
    ranks = {"a": 1, "b": 2, "c": 2, "d": 3}

    result = validate_competition_ranking(ranks, ["a", "b", "c", "d"])

    assert not result.is_valid


def test_validate_rejects_first_place_tie_without_skipped_rank() -> None:
    ranks = {"a": 1, "b": 1, "c": 2, "d": 4}

    result = validate_competition_ranking(ranks, ["a", "b", "c", "d"])

    assert not result.is_valid


def test_validate_rejects_missing_rank_without_tie() -> None:
    ranks = {"a": 1, "b": 3, "c": 4}

    result = validate_competition_ranking(ranks, ["a", "b", "c"])

    assert not result.is_valid


def test_validate_accepts_three_way_first_place_tie() -> None:
    ranks = {"a": 1, "b": 1, "c": 1, "d": 4}

    result = validate_competition_ranking(ranks, ["a", "b", "c", "d"])

    assert result.is_valid


def test_award_points_gives_last_place_zero() -> None:
    ranks = {"a": 1, "b": 2, "c": 2, "d": 4}

    points = award_points(ranks, 4)

    assert points == {"a": 3, "b": 2, "c": 2, "d": 0}


def test_ranking_from_scores_uses_competition_ranking() -> None:
    scores = {"a": 15, "b": 20, "c": 20, "d": 3}

    ranking = ranking_from_scores(scores)

    assert ranking == {"b": 1, "c": 1, "a": 3, "d": 4}


def test_ranking_from_penalty_scores_uses_lower_scores_as_better() -> None:
    scores = {"a": 5, "b": 2, "c": 2, "d": 9}

    ranking = ranking_from_scores(scores, higher_is_better=False)

    assert ranking == {"b": 1, "c": 1, "a": 3, "d": 4}


def test_tied_rank_groups_finds_multiple_ties() -> None:
    ranks = {"a": 1, "b": 1, "c": 3, "d": 4, "e": 4}

    groups = tied_rank_groups(ranks)

    assert groups == [(1, ["a", "b"]), (4, ["d", "e"])]


def test_resolve_tied_ranking_expands_tied_rank_slots() -> None:
    ranks = {"a": 1, "b": 1, "c": 3, "d": 3, "e": 5}

    resolved = resolve_tied_ranking(
        ranks,
        {
            1: {"b": 1, "a": 2},
            3: {"d": 1, "c": 2},
        },
    )

    assert resolved == {"a": 2, "b": 1, "c": 4, "d": 3, "e": 5}


def test_resolve_tied_ranking_rejects_duplicate_places() -> None:
    ranks = {"a": 1, "b": 1, "c": 3}

    with pytest.raises(ValueError):
        resolve_tied_ranking(ranks, {1: {"a": 1, "b": 1}})


def test_sum_round_scores_totals_each_team() -> None:
    rounds = [
        {"a": 2, "b": 4, "c": 0},
        {"a": 5, "b": 1, "c": 3},
    ]

    totals = sum_round_scores(rounds, ["a", "b", "c"])

    assert totals == {"a": 7, "b": 5, "c": 3}


def test_cutting_penalty_is_zero_for_perfect_split() -> None:
    assert cutting_penalty(50, 50) == 0


def test_cutting_penalty_uses_smaller_over_larger_ratio() -> None:
    assert cutting_penalty(40, 60) == pytest.approx(1 / 3)


def test_cutting_round_winner_points_use_lower_penalty_as_better() -> None:
    weights = {
        "a": (50, 50),
        "b": (40, 60),
        "c": (30, 70),
    }

    points = cutting_round_winner_points(weights, 3)

    assert points == {"a": 2, "b": 1, "c": 0}


def test_build_scoreboard_uses_competition_ranking_for_total_ties() -> None:
    teams = [
        Team(id="a", name="Alpha"),
        Team(id="b", name="Beta"),
        Team(id="c", name="Charlie"),
    ]
    game = GameResult(
        id="game_1",
        name="Quiz",
        mode="direct_ranking",
        ranking={"a": 1, "b": 1, "c": 3},
        awarded_points={"a": 2, "b": 2, "c": 0},
    )

    rows = build_scoreboard(AppState(teams=teams, games=[game]))

    assert [(row.team_id, row.rank, row.total_points) for row in rows] == [
        ("a", 1, 2),
        ("b", 1, 2),
        ("c", 3, 0),
    ]
