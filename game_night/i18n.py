from __future__ import annotations


DEFAULT_LOCALE = "en"
LOCALES = ("de", "en")


TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "app.title": "Game Night Scoreboard",
        "nav.language": "DE | EN",
        "nav.view": "View",
        "nav.scoreboard": "Scoreboard",
        "nav.teams": "Teams",
        "nav.simple_game": "Add Simple Game",
        "nav.multi_round_game": "Add Multi-Round Game",
        "nav.cutting_game": "Add Cutting Game",
        "nav.history": "Game History",
        "scoreboard.empty": "Add teams before the first game.",
        "scoreboard.current_leader": "Current leader",
        "scoreboard.leader_points": "{points} points",
        "scoreboard.row_meta": "{wins} wins · {played} played",
        "scoreboard.compact_title": "Evening Scoreboard",
        "scoreboard.rank": "Rank",
        "scoreboard.name": "Name",
        "scoreboard.points": "Points",
        "teams.saved_warning": (
            "Games have already been saved. Team setup should normally stay "
            "fixed after the evening starts."
        ),
        "teams.name": "Team name",
        "teams.color": "Team color",
        "teams.add": "Add team",
        "teams.configured": "Configured teams",
        "teams.none": "No teams yet.",
        "teams.color_collapsed": "Color",
        "teams.remove": "Remove",
        "teams.reset_title": "Session Reset",
        "teams.reset_caption": (
            "Use this if you want to clear saved results or start the evening "
            "from scratch."
        ),
        "teams.reset_button": "Reset Game Night Session",
        "teams.name_empty": "Team name cannot be empty.",
        "teams.name_unique": "Team names must be unique.",
        "teams.added": "Team added.",
        "game.need_two_teams": (
            "Add at least two teams before saving game results."
        ),
        "game.input_mode": "Input mode",
        "game.input_points": "Point Mode",
        "game.input_rank": "Rank Mode",
        "game.point_scoring": "Point scoring",
        "game.score_points": "Score Points",
        "game.penalty_points": "Penalty Points",
        "game.penalty_caption": (
            "Lower penalty points rank higher."
        ),
        "game.score_caption": (
            "Higher score points rank higher."
        ),
        "game.tie_pattern_caption": (
            "Ties are allowed with skipped places, for example 1, 2, 2, 4."
        ),
        "game.name": "Game name",
        "game.save_result": "Save result",
        "game.rounds": "Rounds",
        "game.current_round": "Current round",
        "game.round_label": "Round {number}",
        "game.round_inputs": "Round inputs",
        "game.final_ranking_caption": (
            "Use this if the game directly produces a ranking and input only this ranking."
        ),
        "game.end_and_save": "End Game and Save Result",
        "game.name_empty": "Game name cannot be empty.",
        "game.invalid_ranking_input": "Invalid ranking input.",
        "game.invalid_round_input": "Invalid round input.",
        "game.invalid_point_scoring_input": "Invalid point scoring input.",
        "cutting.default_name": "Cutting Challenge",
        "cutting.objects_rounds": "Objects / rounds",
        "cutting.live_performance": "Live Cutting Performance",
        "cutting.game_totals": "Game totals",
        "cutting.object": "Object",
        "cutting.object_default": "Object {number}",
        "cutting.part_a_weight": "Part A weight",
        "cutting.part_b_weight": "Part B weight",
        "cutting.round_heading": "Round {number}: {object_name}",
        "cutting.round_winner_points": "{points} round-winner points",
        "cutting.balance_label": "Cut balance",
        "cutting.points_short": "pts",
        "cutting.invalid_weights": "Round {number} has invalid weight data.",
        "cutting.missing_weights": (
            "Round {number} needs both part weights for every team before "
            "saving."
        ),
        "history.empty": "No games have been saved yet.",
        "history.mode_caption": "Mode: {mode} / {input_mode} input{suffix}",
        "history.game_points": "game points",
        "history.evening_points": "evening points",
        "history.remove_entry": "Remove this entry",
        "history.point_direction_penalty": " / penalty points",
        "history.point_direction_score": " / score points",
        "history.mode.simple": "simple",
        "history.mode.multi_round": "multi round",
        "history.mode.cutting": "cutting",
        "history.mode.direct_ranking": "direct ranking",
        "history.input_mode.rank": "rank",
        "history.input_mode.points": "points",
        "dialog.close": "Close",
        "dialog.cancel": "Cancel",
        "dialog.delete_game_title": "Remove Game History Entry",
        "dialog.delete_missing": "This game entry no longer exists.",
        "dialog.delete_question": (
            "Remove `{game_name}` from the game history?"
        ),
        "dialog.delete_warning": (
            "This will also remove this game's contribution from the evening "
            "scoreboard."
        ),
        "dialog.delete_confirm": "Remove entry",
        "dialog.reset_title": "Reset Game Night Session",
        "dialog.reset_choice": "Choose what to reset.",
        "dialog.reset_continue": "Continue with current game night",
        "dialog.reset_results": "Reset results and keep teams",
        "dialog.reset_all": "Reset whole session including teams",
        "dialog.reset_results_warning": (
            "All game history and evening points will be removed. Teams stay "
            "configured."
        ),
        "dialog.reset_all_warning": (
            "All teams, game history, and evening points will be removed."
        ),
        "dialog.reset_none_info": "No saved data will be changed.",
        "dialog.apply_selection": "Apply selection",
        "dialog.tie_title": "Tie detected",
        "dialog.tie_intro": (
            "This game result contains at least one tie. You can keep the tie "
            "scoring, enter the result of a tie-break, or abort the save."
        ),
        "dialog.tie_handling": "Tie handling",
        "dialog.tie_use_scoring": "Use tie scoring",
        "dialog.tie_resolve": "Resolve tied teams after tie-break",
        "dialog.tie_abort_return": "Abort save and return to game",
        "dialog.tie_same_points": (
            "The tied teams will receive the same evening points."
        ),
        "dialog.tie_save_with_ties": "Save with ties",
        "dialog.tie_no_save": "No game result will be saved.",
        "dialog.tie_abort_save": "Abort save",
        "dialog.tie_for_rank": "Tie for rank #{rank}",
        "dialog.tie_assign_caption": (
            "Assign each tied team a unique tie-break place. Place 1 is the "
            "best team within this tied group."
        ),
        "dialog.tie_place": "{place}. within tied group",
        "dialog.tie_duplicate_places": (
            "Each tied team needs a unique tie-break place."
        ),
        "dialog.tie_save_resolved": "Save resolved order",
        "validation.add_team_first": "Add at least one team first.",
        "validation.missing_rank": "Every team needs a rank.",
        "validation.unknown_teams": "Ranking contains unknown teams.",
        "validation.rank_range": "Ranks must be between 1 and {team_count}.",
        "validation.tie_pattern": (
            "Invalid tie pattern. Use competition ranking such as 1, 2, 2, 4."
        ),
        "validation.ranking_valid": "Ranking is valid.",
        "validation.tie_break_missing": (
            "Tie-break places must cover the tied teams."
        ),
        "validation.tie_break_unique": (
            "Tie-break places must be unique and consecutive."
        ),
    },
    "de": {
        "app.title": "Spieleabend-Punktestand",
        "nav.language": "DE | EN",
        "nav.view": "Ansicht",
        "nav.scoreboard": "Punktestand",
        "nav.teams": "Teams",
        "nav.simple_game": "Einfaches Spiel",
        "nav.multi_round_game": "Mehrrundiges Spiel",
        "nav.cutting_game": "Schneidespiel",
        "nav.history": "Spielverlauf",
        "scoreboard.empty": "Füge vor dem ersten Spiel Teams hinzu.",
        "scoreboard.current_leader": "Aktuelle Führung",
        "scoreboard.leader_points": "{points} Punkte",
        "scoreboard.row_meta": "{wins} Siege · {played} Spiele",
        "scoreboard.compact_title": "Gesamter Abend",
        "scoreboard.rank": "Platz",
        "scoreboard.name": "Name",
        "scoreboard.points": "Punkte",
        "teams.saved_warning": (
            "Es wurden bereits Spiele gespeichert. Die Teamkonfiguration "
            "sollte nach Beginn des Abends unverändert bleiben."
        ),
        "teams.name": "Teamname",
        "teams.color": "Teamfarbe",
        "teams.add": "Team hinzufügen",
        "teams.configured": "Konfigurierte Teams",
        "teams.none": "Noch keine Teams.",
        "teams.color_collapsed": "Farbe",
        "teams.remove": "Entfernen",
        "teams.reset_title": "Sitzung zurücksetzen",
        "teams.reset_caption": (
            "Hier kannst du gespeicherte Ergebnisse löschen oder den "
            "Spieleabend neu starten."
        ),
        "teams.reset_button": "Spieleabend zurücksetzen",
        "teams.name_empty": "Der Teamname darf nicht leer sein.",
        "teams.name_unique": "Teamnamen müssen eindeutig sein.",
        "teams.added": "Team hinzugefügt.",
        "game.need_two_teams": (
            "Füge mindestens zwei Teams hinzu, bevor du Ergebnisse speicherst."
        ),
        "game.input_mode": "Eingabemodus",
        "game.input_points": "Punktemodus",
        "game.input_rank": "Platzierungsmodus",
        "game.point_scoring": "Punktewertung",
        "game.score_points": "Pluspunkte",
        "game.penalty_points": "Strafpunkte",
        "game.penalty_caption": (
            "Weniger Strafpunkte ergeben eine bessere Platzierung."
        ),
        "game.score_caption": (
            "Mehr Pluspunkte ergeben eine bessere Platzierung."
        ),
        "game.tie_pattern_caption": (
            "Gleichstände werden mit übersprungenen Plätzen gewertet. Dies führt zum "
            "Beispiel zu 1, 2, 2, 4."
        ),
        "game.name": "Spielname",
        "game.save_result": "Ergebnis speichern",
        "game.rounds": "Runden",
        "game.current_round": "Aktuelle Runde",
        "game.round_label": "Runde {number}",
        "game.round_inputs": "Rundeneingaben",
        "game.final_ranking_caption": (
            "Trage direkt die Platzierung ein, wenn das Spiel direkt Platzierungen produziert und nur diese eingegeben werden soll."
        ),
        "game.end_and_save": "Spiel beenden und Ergebnis speichern",
        "game.name_empty": "Der Spielname darf nicht leer sein.",
        "game.invalid_ranking_input": "Ungültige Platzierungseingabe.",
        "game.invalid_round_input": "Ungültige Rundeneingabe.",
        "game.invalid_point_scoring_input": "Ungültige Punktewertung.",
        "cutting.default_name": "Schneide-Challenge",
        "cutting.objects_rounds": "Objekte / Runden",
        "cutting.live_performance": "Live-Schneideleistung",
        "cutting.game_totals": "Gesamtergebnis",
        "cutting.object": "Objekt",
        "cutting.object_default": "Objekt {number}",
        "cutting.part_a_weight": "Gewicht Teil A",
        "cutting.part_b_weight": "Gewicht Teil B",
        "cutting.round_heading": "Runde {number}: {object_name}",
        "cutting.round_winner_points": "{points} Rundensiegerpunkte",
        "cutting.balance_label": "Schnittabweichung",
        "cutting.points_short": "Pkt.",
        "cutting.invalid_weights": (
            "Runde {number} enthält ungültige Gewichtsdaten."
        ),
        "cutting.missing_weights": (
            "Runde {number} benötigt beide Teilgewichte für jedes Team, bevor "
            "gespeichert werden kann."
        ),
        "history.empty": "Es wurden noch keine Spiele gespeichert.",
        "history.mode_caption": "Modus: {mode} / Eingabe: {input_mode}{suffix}",
        "history.game_points": "Spielpunkte",
        "history.evening_points": "Punkte für die Gesamtwertung",
        "history.remove_entry": "Diesen Eintrag entfernen",
        "history.point_direction_penalty": " / Strafpunkte",
        "history.point_direction_score": " / Pluspunkte",
        "history.mode.simple": "einfach",
        "history.mode.multi_round": "mehrrundig",
        "history.mode.cutting": "Schneiden",
        "history.mode.direct_ranking": "direkte Platzierungen",
        "history.input_mode.rank": "Platz",
        "history.input_mode.points": "Punkte",
        "dialog.close": "Schließen",
        "dialog.cancel": "Abbrechen",
        "dialog.delete_game_title": "Spielverlauf-Eintrag entfernen",
        "dialog.delete_missing": "Dieser Spieleintrag existiert nicht mehr.",
        "dialog.delete_question": (
            "`{game_name}` aus dem Spielverlauf entfernen?"
        ),
        "dialog.delete_warning": (
            "Dadurch wird auch der Beitrag dieses Spiels zum Punktestand des "
            "Abends entfernt."
        ),
        "dialog.delete_confirm": "Eintrag entfernen",
        "dialog.reset_title": "Spieleabend zurücksetzen",
        "dialog.reset_choice": "Wähle aus, was zurückgesetzt werden soll.",
        "dialog.reset_continue": "Mit aktuellem Spieleabend fortfahren",
        "dialog.reset_results": "Ergebnisse zurücksetzen und Teams behalten",
        "dialog.reset_all": "Ganze Sitzung inklusive Teams zurücksetzen",
        "dialog.reset_results_warning": (
            "Der gesamte Spielverlauf und alle Abendpunkte werden entfernt. "
            "Die Teams bleiben konfiguriert."
        ),
        "dialog.reset_all_warning": (
            "Alle Teams, der gesamte Spielverlauf und alle Abendpunkte werden "
            "entfernt."
        ),
        "dialog.reset_none_info": "Gespeicherte Daten werden nicht geändert.",
        "dialog.apply_selection": "Auswahl anwenden",
        "dialog.tie_title": "Gleichstand erkannt",
        "dialog.tie_intro": (
            "Dieses Spielergebnis enthält mindestens einen Gleichstand. Du "
            "kannst die Gleichstandswertung behalten, das Ergebnis eines "
            "Tie-Breaks eintragen oder das Speichern abbrechen."
        ),
        "dialog.tie_handling": "Umgang mit Gleichstand",
        "dialog.tie_use_scoring": "Standard Gleichstandswertung verwenden",
        "dialog.tie_resolve": "Gleichstand nach Tie-Break auflösen",
        "dialog.tie_abort_return": "Speichern abbrechen und zurück zum Spiel",
        "dialog.tie_same_points": (
            "Die Teams mit Gleichstand erhalten dieselben Abendpunkte."
        ),
        "dialog.tie_save_with_ties": "Mit Gleichständen speichern",
        "dialog.tie_no_save": "Es wird kein Spielergebnis gespeichert.",
        "dialog.tie_abort_save": "Speichern abbrechen",
        "dialog.tie_for_rank": "Gleichstand auf Platz #{rank}",
        "dialog.tie_assign_caption": (
            "Weise jedem Team mit Gleichstand einen eindeutigen Tie-Break-"
            "Platz zu. Platz 1 ist das beste Team innerhalb dieser Gruppe."
        ),
        "dialog.tie_place": "{place}. innerhalb der Gleichstandsgruppe",
        "dialog.tie_duplicate_places": (
            "Jedes Team mit Gleichstand benötigt einen eindeutigen Tie-Break-"
            "Platz."
        ),
        "dialog.tie_save_resolved": "Aufgelöste Reihenfolge speichern",
        "validation.add_team_first": "Füge zuerst mindestens ein Team hinzu.",
        "validation.missing_rank": "Jedes Team benötigt eine Platzierung.",
        "validation.unknown_teams": "Die Platzierungsliste enthält unbekannte Teams.",
        "validation.rank_range": (
            "Platzierungen müssen zwischen 1 und {team_count} liegen."
        ),
        "validation.tie_pattern": (
            "Ungültiges Gleichstandsmuster. Nutze Wettkampfplatzierungen wie "
            "1, 2, 2, 4."
        ),
        "validation.ranking_valid": "Die Platzierungsliste ist gültig.",
        "validation.tie_break_missing": (
            "Tie-Break-Plätze müssen alle Teams mit Gleichstand abdecken."
        ),
        "validation.tie_break_unique": (
            "Tie-Break-Plätze müssen eindeutig und fortlaufend sein."
        ),
    },
}


def normalize_locale(locale: str | None) -> str:
    if locale in LOCALES:
        return locale

    return DEFAULT_LOCALE


def t(locale: str | None, key: str, **values: object) -> str:
    locale = normalize_locale(locale)
    text = TRANSLATIONS.get(locale, {}).get(key)

    if text is None:
        text = TRANSLATIONS[DEFAULT_LOCALE].get(key, key)

    return text.format(**values)
