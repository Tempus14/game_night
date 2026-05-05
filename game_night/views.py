from __future__ import annotations

from dataclasses import replace
from html import escape

import streamlit as st

from game_night.models import AppState, GameResult, Team
from game_night.scoring import (
    award_points,
    build_scoreboard,
    team_name_by_id,
    validate_competition_ranking,
)
from game_night.storage import load_state, save_state


TEAM_COLORS = [
    "#2F80ED",
    "#EB5757",
    "#27AE60",
    "#F2C94C",
    "#9B51E0",
    "#F2994A",
    "#00A7A7",
    "#4F4F4F",
    "#D81B60",
    "#6D4C41",
]


def run_app() -> None:
    st.set_page_config(
        page_title="Game Night Scoreboard",
        layout="wide",
    )
    _apply_styles()
    _ensure_state()

    page = st.sidebar.radio(
        "View",
        ["Scoreboard", "Teams", "Add Game Result", "Game History"],
    )

    if page == "Scoreboard":
        render_scoreboard(st.session_state.app_state)
    elif page == "Teams":
        render_teams(st.session_state.app_state)
    elif page == "Add Game Result":
        render_add_game_result(st.session_state.app_state)
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
        team_color = escape(row.team_color)
        st.markdown(
            f"""
            <div class="score-row">
                <div class="rank">#{row.rank}</div>
                <div class="team">
                    <span class="color-dot"
                        style="background: {team_color};"></span>
                    <span style="color: black;">{team_name}</span>
                </div>
                <div class="points" style="color: {team_color};">
                    {row.total_points} Points
                </div>
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


def render_add_game_result(state: AppState) -> None:
    st.title("Add Game Result")

    if len(state.teams) < 2:
        st.info("Add at least two teams before saving game results.")
        return

    st.caption(
        "Direct ranking supports ties with skipped places, for example "
        "1, 2, 2, 4."
    )

    with st.form("direct_ranking_game"):
        game_name = st.text_input("Game name")
        ranks = {}

        for team in state.teams:
            ranks[team.id] = st.number_input(
                team.name,
                min_value=1,
                max_value=len(state.teams),
                value=1,
                step=1,
                key=f"rank_{team.id}",
            )

        submitted = st.form_submit_button("Save result")

    if submitted:
        _save_direct_ranking_game(state, game_name, ranks)


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
                st.write(
                    f"#{rank} - {names.get(team_id, team_id)} - "
                    f"{points} points"
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


def _save_direct_ranking_game(
    state: AppState,
    game_name: str,
    ranks: dict[str, int],
) -> None:
    normalized_name = game_name.strip()

    if not normalized_name:
        st.error("Game name cannot be empty.")
        return

    validation = validate_competition_ranking(
        ranks,
        [team.id for team in state.teams],
    )

    if not validation.is_valid:
        st.error(validation.message)
        return

    points = award_points(ranks, len(state.teams))
    game = GameResult.create_direct_ranking(
        normalized_name,
        ranks,
        points,
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
                background: #101828;
                color: white;
                padding: 1.5rem 1.8rem;
                border-radius: 8px;
                margin-bottom: 1rem;
            }

            .leader-label {
                color: #b7c0d1;
                font-size: 0.95rem;
                text-transform: uppercase;
            }

            .leader-name {
                font-size: 3rem;
                font-weight: 800;
                line-height: 1.1;
            }

            .leader-points {
                font-size: 1.3rem;
                color: #e5e7eb;
            }

            .score-row {
                display: grid;
                grid-template-columns: 5rem 1fr 8rem 11rem;
                align-items: center;
                gap: 1rem;
                background: white;
                border: 1px solid #e6e8ee;
                border-radius: 8px;
                padding: 1rem 1.2rem;
                margin-bottom: 0.7rem;
                box-shadow: 0 4px 14px rgba(16, 24, 40, 0.06);
            }

            .rank {
                font-size: 1.7rem;
                font-weight: 800;
                color: #101828;
            }

            .team {
                display: flex;
                align-items: center;
                gap: 0.8rem;
                font-size: 1.6rem;
                font-weight: 700;
                min-width: 0;
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
            }

            .points {
                font-size: 2rem;
                font-weight: 800;
                text-align: right;
            }

            .meta {
                color: #667085;
                text-align: right;
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
