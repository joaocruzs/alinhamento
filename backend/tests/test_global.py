from app.services.global_alignment import needleman_wunsch


def test_official_global_example():

    result = needleman_wunsch(
        seq1="ACGTAC",
        seq2="ACGTTC",
        match=2,
        mismatch=-1,
        gap=-2
    )

    assert result["score"] == 9

    assert result["aligned_seq1"] == "ACGTAC"

    assert result["aligned_seq2"] == "ACGTTC"

    assert result["markers"] == "||||.|"


def test_global_matrix_initialization():

    result = needleman_wunsch(
        seq1="AC",
        seq2="AC",
        match=2,
        mismatch=-1,
        gap=-2
    )

    matrix = result["matrix"]

    assert matrix[0] == [0, -2, -4]

    assert matrix[1][0] == -2

    assert matrix[2][0] == -4


def test_traceback_directions():
    result = needleman_wunsch(
        seq1="AC",
        seq2="AC",
        match=2,
        mismatch=-1,
        gap=-2
    )

    assert [
        position.direction
        for position in result["traceback"]
    ] == [
        "D",
        "D"
    ]

def test_global_alignment_with_gap():

    result = needleman_wunsch(
        seq1="AC",
        seq2="AGC",
        match=2,
        mismatch=-1,
        gap=-2
    )

    assert len(result["aligned_seq1"]) == len(
        result["aligned_seq2"]
    )

    assert "-" in result["aligned_seq1"] or "-" in result["aligned_seq2"]

def test_global_returns_direction_matrix():
    result = needleman_wunsch(
        seq1="AC",
        seq2="AC",
        match=2,
        mismatch=-1,
        gap=-2
    )

    assert result["directions"] == [
        [None, "H", "H"],
        ["V", "D", "H"],
        ["V", "V", "D"]
    ]


def test_global_returns_start_position():
    result = needleman_wunsch(
        seq1="AC",
        seq2="AC",
        match=2,
        mismatch=-1,
        gap=-2
    )

    assert result["start_position"] == {
        "row": 2,
        "column": 2
    }

def test_global_traceback_positions():
    result = needleman_wunsch(
        seq1="AC",
        seq2="AC",
        match=2,
        mismatch=-1,
        gap=-2
    )

    traceback = result["traceback"]

    assert traceback[0].row == 2
    assert traceback[0].column == 2
    assert traceback[0].direction == "D"

    assert traceback[1].row == 1
    assert traceback[1].column == 1
    assert traceback[1].direction == "D"