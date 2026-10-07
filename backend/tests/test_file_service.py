import pytest

from app.services.file_service import read_sequences_from_file
from app.services.validation_service import ValidationError


def test_read_txt_file():
    content = b"ACGTAC\nACGTTC\n"

    seq1, seq2 = read_sequences_from_file(
        "sequences.txt",
        content
    )

    assert seq1 == "ACGTAC"
    assert seq2 == "ACGTTC"


def test_read_txt_file_lowercase():
    content = b"acgtac\nacgttc\n"

    seq1, seq2 = read_sequences_from_file(
        "sequences.txt",
        content
    )

    assert seq1 == "ACGTAC"
    assert seq2 == "ACGTTC"


def test_read_fasta_file():
    content = (
        b">Seq1\n"
        b"ACGTAC\n"
        b">Seq2\n"
        b"ACGTTC\n"
    )

    seq1, seq2 = read_sequences_from_file(
        "sequences.fasta",
        content
    )

    assert seq1 == "ACGTAC"
    assert seq2 == "ACGTTC"


def test_fasta_multiple_lines():
    content = (
        b">Seq1\n"
        b"ACGT\n"
        b"AC\n"
        b">Seq2\n"
        b"ACGT\n"
        b"TC\n"
    )

    seq1, seq2 = read_sequences_from_file(
        "sequences.fasta",
        content
    )

    assert seq1 == "ACGTAC"
    assert seq2 == "ACGTTC"


def test_file_with_wrong_number_of_sequences():
    content = b"ACGTAC\nACGTTC\nGGGG\n"

    with pytest.raises(ValidationError):
        read_sequences_from_file(
            "sequences.txt",
            content
        )


def test_invalid_extension():
    content = b"ACGTAC\nACGTTC\n"

    with pytest.raises(ValidationError):
        read_sequences_from_file(
            "sequences.csv",
            content
        )


def test_invalid_dna_in_file():
    content = b"ACGTAX\nACGTTC\n"

    with pytest.raises(ValidationError):
        read_sequences_from_file(
            "sequences.txt",
            content
        )