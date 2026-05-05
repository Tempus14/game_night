from __future__ import annotations

import re
from dataclasses import replace
from html import escape

import streamlit as st

from game_night.models import AppState, GameResult, Team
from game_night.scoring import (
    award_points,
    build_scoreboard,
    ranking_from_scores,
    sum_round_scores,
    team_name_by_id,
    validate_competition_ranking,
)
from game_night.storage import load_state, save_state
from game_night.theme import TEAM_COLORS


def run_app() -> None:
    st.set_page_config(
        page_title="Game Night Scoreboard",
        layout="wide",
    )
    _apply_styles()
    _ensure_state()

    page = st.sidebar.radio(
        "View",
        [
            "Scoreboard",
            "Teams",
            "Add Simple Game Result",
            "Add Multi-Round Game Result",
            "Game History",
        ],
    )

    if page == "Scoreboard":
        render_scoreboard(st.session_state.app_state)
    elif page == "Teams":
        render_teams(st.session_state.app_state)
    elif page == "Add Simple Game Result":
        render_add_simple_game_result(st.session_state.app_state)
    elif page == "Add Multi-Round Game Result":
        render_add_multi_round_game_result(st.session_state.app_state)
    else:
        render_game_history(st.session_state.app_state)


def render_scoreboard(state: AppState) -> None:
    st.title("Scoreboard")

    if not state.teams:
        st.info("Add teams before the first game.")
        return

    rows = build_scoreboard(state)

    if rows:
        leader = rows[0]
        leader_name = escape(leader.team_name)
        st.markdown(
            f"""
            <section class="leader">
                <div class="leader-label">Current leader</div>
                <div class="leader-name">{leader_name}</div>
                <div class="leader-points">{leader.total_points} points</div>
            </section>
            """,
            unsafe_allow_html=True,
        )

    for row in rows:
        team_name = escape(row.team_name)
        team_color = _safe_hex_color(row.team_color)
        rank_class = _rank_class(row.rank)
        st.markdown(
            f"""
            <div class="score-row" style="--team-color: {team_color};">
                <div class="rank {rank_class}">#{row.rank}</div>
                <div class="team">
                    <span class="color-dot"></span>
                    <span>{team_name}</span>
                </div>
                <div class="points">{row.total_points}</div>
                <div class="meta">
                    {row.games_won} wins &middot; {row.games_played} played
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_teams(state: AppState) -> None:
    st.title("Teams")

    if state.games:
        st.warning(
            "Games have already been saved. Team setup should normally stay "
            "fixed after the evening starts."
        )

    with st.form("add_team", clear_on_submit=True):
        name = st.text_input("Team name")
        color = st.color_picker(
            "Team color",
            TEAM_COLORS[len(state.teams) % len(TEAM_COLORS)],
        )
        submitted = st.form_submit_button("Add team")

    if submitted:
        _add_team(state, name, color)

    st.subheader("Configured teams")

    if not state.teams:
        st.caption("No teams yet.")
        return

    for team in state.teams:
        cols = st.columns([0.4, 3, 1])
        cols[0].color_picker(
            "Color",
            value=team.color,
            key=f"color_{team.id}",
            disabled=True,
            label_visibility="collapsed",
        )
        cols[1].markdown(f"### {team.name}")

        if not state.games and cols[2].button("Remove", key=f"remove_{team.id}"):
            _remove_team(state, team.id)
            st.rerun()


def render_add_simple_game_result(state: AppState) -> None:
    st.title("Add Simple Game Result")

    if len(state.teams) < 2:
        st.info("Add at least two teams before saving game results.")
        return

    form_column, scoreboard_column = st.columns([0.62, 0.38], gap="large")

    with form_column:
        input_mode = st.radio(
            "Input mode",
            ["Point Mode", "Rank Mode"],
            horizontal=True,
            key="simple_input_mode",
        )

        with st.form("direct_ranking_game"):
            game_name = st.text_input("Game name")

            if input_mode == "Rank Mode":
                st.caption(
                    "Ties are allowed with skipped places, for example "
                    "1, 2, 2, 4."
                )
                inputs = _ranking_inputs(state, "simple_rank")
            else:
                st.caption(
                    "Higher game points rank higher. Ties produce tied ranks."
                )
                inputs = _point_inputs(state, "simple_points")

            submitted = st.form_submit_button("Save result")

        if submitted:
            _save_simple_game(state, game_name, input_mode, inputs)

    with scoreboard_column:
        render_compact_scoreboard(state)


def render_add_multi_round_game_result(state: AppState) -> None:
    st.title("Add Multi-Round Game Result")

    if len(state.teams) < 2:
        st.info("Add at least two teams before saving game results.")
        return

    form_column, scoreboard_column = st.columns([0.62, 0.38], gap="large")

    with form_column:
        input_mode = st.radio(
            "Input mode",
            ["Point Mode", "Rank Mode"],
            horizontal=True,
            key="round_input_mode",
        )
        round_count = st.number_input(
            "Rounds",
            min_value=1,
            max_value=20,
            value=3,
            step=1,
        )

        with st.form("multi_round_game"):
            game_name = st.text_input("Game name")

            if input_mode == "Point Mode":
                st.caption(
                    "Enter each team's points per round. Round totals are "
                    "summed before the game ranking is calculated."
                )
                rounds = _round_point_inputs(
                    state,
                    "multi_round_points",
                    int(round_count),
                )
                inputs = {"rounds": rounds}
            else:
                st.caption(
                    "Use this if the final game ranking is already known. "
                    "Ties are allowed with skipped places."
                )
                inputs = {
                    "ranking": _ranking_inputs(
                        state,
                        "multi_round_rank",
                    )
                }

            submitted = st.form_submit_button("Save result")

        if submitted:
            _save_multi_round_game(state, game_name, input_mode, inputs)

    with scoreboard_column:
        render_compact_scoreboard(state)


def render_compact_scoreboard(state: AppState) -> None:
    st.subheader("Evening Scoreboard")

    rows = build_scoreboard(state)

    st.markdown(
        """
        <div class="compact-scoreboard compact-scoreboard-header">
            <div>Rank</div>
            <div>Name</div>
            <div>Points</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for row in rows:
        team_name = escape(row.team_name)
        team_color = _safe_hex_color(row.team_color)
        st.markdown(
            f"""
            <div class="compact-scoreboard compact-scoreboard-row"
                style="--team-color: {team_color};">
                <div>#{row.rank}</div>
                <div class="compact-team-name">
                    <span class="compact-color-dot"></span>
                    <span>{team_name}</span>
                </div>
                <div>{row.total_points}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _ranking_inputs(state: AppState, key_prefix: str) -> dict[str, int]:
    ranks = {}

    for team in state.teams:
        ranks[team.id] = st.number_input(
            team.name,
            min_value=1,
            max_value=len(state.teams),
            value=1,
            step=1,
            key=f"{key_prefix}_{team.id}",
        )

    return ranks


def _point_inputs(state: AppState, key_prefix: str) -> dict[str, int]:
    points = {}

    for team in state.teams:
        points[team.id] = st.number_input(
            team.name,
            min_value=0,
            value=0,
            step=1,
            key=f"{key_prefix}_{team.id}",
        )

    return points


def _round_point_inputs(
    state: AppState,
    key_prefix: str,
    round_count: int,
) -> list[dict[str, int]]:
    rounds = []
    tabs = st.tabs([f"Round {number}" for number in range(1, round_count + 1)])

    for index, tab in enumerate(tabs, start=1):
        with tab:
            rounds.append(
                _point_inputs(state, f"{key_prefix}_{index}")
            )

    return rounds


def render_game_history(state: AppState) -> None:
    st.title("Game History")

    if not state.games:
        st.info("No games have been saved yet.")
        return

    names = team_name_by_id(state.teams)

    for game in reversed(state.games):
        with st.expander(game.name, expanded=False):
            rows = sorted(
                game.ranking.items(),
                key=lambda item: (item[1], names.get(item[0], item[0])),
            )

            for team_id, rank in rows:
                points = game.awarded_points.get(team_id, 0)
                game_points = game.game_points.get(team_id)
                detail = ""
                if game_points is not None:
                    detail = f" - game points: {game_points}"

                st.write(
                    f"#{rank} - {names.get(team_id, team_id)} - "
                    f"{points} evening points{detail}"
                )


def _add_team(state: AppState, name: str, color: str) -> None:
    normalized_name = name.strip()

    if not normalized_name:
        st.error("Team name cannot be empty.")
        return

    if any(team.name.lower() == normalized_name.lower() for team in state.teams):
        st.error("Team names must be unique.")
        return

    next_state = replace(
        state,
        teams=[*state.teams, Team.create(normalized_name, color)],
    )
    _persist(next_state)
    st.success("Team added.")
    st.rerun()


def _remove_team(state: AppState, team_id: str) -> None:
    next_state = replace(
        state,
        teams=[team for team in state.teams if team.id != team_id],
    )
    _persist(next_state)


def _save_simple_game(
    state: AppState,
    game_name: str,
    input_mode: str,
    inputs: dict[str, int],
) -> None:
    normalized_name = game_name.strip()

    if not normalized_name:
        st.error("Game name cannot be empty.")
        return

    if input_mode == "Rank Mode":
        ranking = inputs
        validation = validate_competition_ranking(
            ranking,
            [team.id for team in state.teams],
        )

        if not validation.is_valid:
            st.error(validation.message)
            return

        game_points = {}
        stored_input_mode = "rank"
    else:
        ranking = ranking_from_scores(inputs)
        game_points = inputs
        stored_input_mode = "points"

    points = award_points(ranking, len(state.teams))
    game = GameResult.create(
        name=normalized_name,
        mode="simple",
        input_mode=stored_input_mode,
        ranking=ranking,
        game_points=game_points,
        awarded_points=points,
    )
    next_state = replace(state, games=[*state.games, game])
    _persist(next_state)
    st.success("Game result saved.")
    st.rerun()


def _save_multi_round_game(
    state: AppState,
    game_name: str,
    input_mode: str,
    inputs: dict[str, object],
) -> None:
    normalized_name = game_name.strip()
    team_ids = [team.id for team in state.teams]

    if not normalized_name:
        st.error("Game name cannot be empty.")
        return

    if input_mode == "Rank Mode":
        ranking = inputs["ranking"]

        if not isinstance(ranking, dict):
            st.error("Invalid ranking input.")
            return

        validation = validate_competition_ranking(ranking, team_ids)

        if not validation.is_valid:
            st.error(validation.message)
            return

        rounds = []
        game_points = {}
        stored_input_mode = "rank"
    else:
        rounds = inputs["rounds"]

        if not isinstance(rounds, list):
            st.error("Invalid round input.")
            return

        game_points = sum_round_scores(rounds, team_ids)
        ranking = ranking_from_scores(game_points)
        stored_input_mode = "points"

    points = award_points(ranking, len(state.teams))
    game = GameResult.create(
        name=normalized_name,
        mode="multi_round",
        input_mode=stored_input_mode,
        ranking=ranking,
        game_points=game_points,
        rounds=rounds,
        awarded_points=points,
    )
    next_state = replace(state, games=[*state.games, game])
    _persist(next_state)
    st.success("Game result saved.")
    st.rerun()


def _ensure_state() -> None:
    if "app_state" not in st.session_state:
        st.session_state.app_state = load_state()


def _persist(state: AppState) -> None:
    save_state(state)
    st.session_state.app_state = state


def _safe_hex_color(color: str) -> str:
    if re.fullmatch(r"#[0-9a-fA-F]{6}", color):
        return color

    return TEAM_COLORS[0]


def _rank_class(rank: int) -> str:
    if rank == 1:
        return "rank-first"

    if rank == 2:
        return "rank-second"

    if rank == 3:
        return "rank-third"

    return "rank-other"


def _apply_styles() -> None:
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 2rem;
                max-width: 1180px;
            }

            h1 {
                font-size: 3rem;
                margin-bottom: 1.4rem;
            }

            .leader {
                background:
                    var(--blue-background-color, rgba(37, 99, 235, 0.16));
                color: var(--text-color);
                border:
                    1px solid var(--border-color, rgba(148, 163, 184, 0.35));
                border-left:
                    0.5rem solid var(--primary-color, #2563eb);
                padding: 1.5rem 1.8rem;
                border-radius: var(--base-radius, 0.5rem);
                margin-bottom: 1rem;
            }

            .leader-label {
                color: var(--text-color);
                font-size: 0.95rem;
                opacity: 0.72;
                text-transform: uppercase;
            }

            .leader-name {
                font-size: 3rem;
                font-weight: 800;
                line-height: 1.1;
                color: var(--text-color);
            }

            .leader-points {
                font-size: 1.3rem;
                color: var(--text-color);
                opacity: 0.82;
            }

            .score-row {
                display: grid;
                grid-template-columns: 5rem 1fr 8rem 11rem;
                align-items: center;
                gap: 1rem;
                background: var(--secondary-background-color);
                border:
                    1px solid var(--border-color, rgba(148, 163, 184, 0.35));
                border-left: 0.5rem solid var(--team-color);
                border-radius: var(--base-radius, 0.5rem);
                padding: 1rem 1.2rem;
                margin-bottom: 0.7rem;
                color: var(--text-color);
                box-shadow: 0 0.35rem 1.1rem rgba(0, 0, 0, 0.12);
            }

            .rank {
                align-items: center;
                border-radius: var(--base-radius, 0.5rem);
                display: flex;
                font-size: 1.7rem;
                font-weight: 800;
                justify-content: center;
                min-height: 3rem;
            }

            .rank-first {
                background:
                    var(--green-background-color, rgba(22, 163, 74, 0.18));
                color: var(--green-text-color, var(--text-color));
            }

            .rank-second {
                background:
                    var(--blue-background-color, rgba(37, 99, 235, 0.16));
                color: var(--blue-text-color, var(--text-color));
            }

            .rank-third {
                background:
                    var(--orange-background-color, rgba(234, 88, 12, 0.18));
                color: var(--orange-text-color, var(--text-color));
            }

            .rank-other {
                background:
                    var(--gray-background-color, rgba(100, 116, 139, 0.16));
                color: var(--gray-text-color, var(--text-color));
            }

            .team {
                display: flex;
                align-items: center;
                gap: 0.8rem;
                font-size: 1.6rem;
                font-weight: 700;
                min-width: 0;
                color: var(--text-color);
            }

            .team span:last-child {
                overflow-wrap: anywhere;
            }

            .color-dot {
                display: inline-block;
                width: 1.1rem;
                height: 1.1rem;
                border-radius: 50%;
                flex: 0 0 auto;
                background: var(--team-color);
            }

            .points {
                font-size: 2rem;
                font-weight: 800;
                text-align: right;
                color: var(--text-color);
            }

            .meta {
                color: var(--text-color);
                opacity: 0.7;
                text-align: right;
            }

            .compact-scoreboard {
                display: grid;
                grid-template-columns: 4rem minmax(0, 1fr) 4.5rem;
                gap: 0.75rem;
                align-items: center;
            }

            .compact-scoreboard-header {
                color: var(--text-color);
                font-size: 0.8rem;
                font-weight: 700;
                opacity: 0.7;
                padding: 0 0.75rem 0.4rem 1rem;
                text-transform: uppercase;
            }

            .compact-scoreboard-row {
                background: var(--secondary-background-color);
                border:
                    1px solid var(--border-color, rgba(148, 163, 184, 0.35));
                border-left: 0.35rem solid var(--team-color);
                border-radius: var(--base-radius, 0.5rem);
                color: var(--text-color);
                font-weight: 700;
                margin-bottom: 0.45rem;
                padding: 0.65rem 0.75rem 0.65rem 0.75rem;
            }

            .compact-scoreboard-row div:last-child {
                text-align: right;
            }

            .compact-team-name {
                align-items: center;
                display: flex;
                gap: 0.5rem;
                min-width: 0;
            }

            .compact-team-name span:last-child {
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }

            .compact-color-dot {
                background: var(--team-color);
                border-radius: 50%;
                display: inline-block;
                flex: 0 0 auto;
                height: 0.7rem;
                width: 0.7rem;
            }

            @media (max-width: 760px) {
                .score-row {
                    grid-template-columns: 4rem 1fr 5rem;
                }

                .meta {
                    grid-column: 2 / 4;
                    text-align: left;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
