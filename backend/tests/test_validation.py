import pytest

from app.services.validation_service import (
    ValidationError,
    validate_score_parameters,
    validate_sequence,
    validate_sequences,
)


def test_sequence_is_converted_to_uppercase():
    result = validate_sequence(
        "acgtac",
        "Seq1"
    )

    assert result == "ACGTAC"


def test_sequence_with_spaces_is_normalized():
    result = validate_sequence(
        "A C G T A C",
        "Seq1"
    )

    assert result == "ACGTAC"


def test_valid_sequences():
    seq1, seq2 = validate_sequences(
        "ACGTAC",
        "ACGTTC"
    )

    assert seq1 == "ACGTAC"
    assert seq2 == "ACGTTC"


def test_empty_sequence():
    with pytest.raises(ValidationError):
        validate_sequence(
            "",
            "Seq1"
        )


def test_invalid_base():
    with pytest.raises(ValidationError):
        validate_sequence(
            "ACGTAXTG",
            "Seq1"
        )


def test_valid_score_parameters():
    result = validate_score_parameters(
        2,
        -1,
        -2
    )

    assert result == (2, -1, -2)


def test_score_parameters_must_be_integers():
    with pytest.raises(ValidationError):
        validate_score_parameters(
            "abc",
            -1,
            -2
        )