import pytest

from game_night.i18n import DEFAULT_LOCALE, LOCALES, TRANSLATIONS, t
from game_night.scoring import (
    TieBreakValidationError,
    resolve_tied_ranking,
    validate_competition_ranking,
)


def test_locales_have_the_same_translation_keys() -> None:
    expected_keys = set(TRANSLATIONS[DEFAULT_LOCALE])

    for locale in LOCALES:
        assert set(TRANSLATIONS[locale]) == expected_keys


def test_translation_falls_back_to_english_for_unknown_locale() -> None:
    assert t("fr", "nav.scoreboard") == "Scoreboard"


def test_translation_formats_values() -> None:
    assert t("de", "validation.rank_range", team_count=4) == (
        "Ränge müssen zwischen 1 und 4 liegen."
    )


def test_ranking_validation_exposes_translatable_message_key() -> None:
    result = validate_competition_ranking({"a": 5}, ["a"])

    assert not result.is_valid
    assert result.message_key == "validation.rank_range"
    assert result.message_params == {"team_count": 1}
    assert result.message == "Ranks must be between 1 and 1."


def test_tie_break_error_exposes_translatable_message_key() -> None:
    with pytest.raises(TieBreakValidationError) as error:
        resolve_tied_ranking({"a": 1, "b": 1}, {1: {"a": 1}})

    assert error.value.message_key == "validation.tie_break_missing"
