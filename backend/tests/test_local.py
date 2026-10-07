from app.services.local_alignment import smith_waterman


def test_local_matrix_initialization():

    result = smith_waterman(
        seq1="AC",
        seq2="AC",
        match=2,
        mismatch=-1,
        gap=-2
    )

    matrix = result["matrix"]

    assert matrix[0] == [0, 0, 0]

    assert matrix[1][0] == 0
    assert matrix[2][0] == 0


def test_local_identical_sequences():

    result = smith_waterman(
        seq1="AC",
        seq2="AC",
        match=2,
        mismatch=-1,
        gap=-2
    )

    assert result["score"] == 4

    assert result["aligned_seq1"] == "AC"
    assert result["aligned_seq2"] == "AC"

    assert result["markers"] == "||"


def test_local_finds_best_region():

    result = smith_waterman(
        seq1="TTACGTAA",
        seq2="GGACGTCC",
        match=2,
        mismatch=-1,
        gap=-2
    )

    assert result["aligned_seq1"] == "ACGT"
    assert result["aligned_seq2"] == "ACGT"

    assert result["markers"] == "||||"

    assert result["score"] == 8


def test_local_scores_never_go_below_zero():

    result = smith_waterman(
        seq1="AAAA",
        seq2="TTTT",
        match=2,
        mismatch=-1,
        gap=-2
    )

    matrix = result["matrix"]

    for row in matrix:
        for value in row:
            assert value >= 0

    assert result["score"] == 0

def test_local_returns_start_position():
    result = smith_waterman(
        seq1="TTACGTAA",
        seq2="GGACGTCC",
        match=2,
        mismatch=-1,
        gap=-2
    )

    assert result["start_position"] == {
        "row": 6,
        "column": 6
    }

def test_local_traceback_reaches_zero():
    result = smith_waterman(
        seq1="TTACGTAA",
        seq2="GGACGTCC",
        match=2,
        mismatch=-1,
        gap=-2
    )

    traceback = result["traceback"]

    last = traceback[-1]

    row = last.row
    column = last.column

    direction = last.direction

    if direction == "D":
        row -= 1
        column -= 1
    elif direction == "V":
        row -= 1
    elif direction == "H":
        column -= 1

    assert result["matrix"][row][column] == 0