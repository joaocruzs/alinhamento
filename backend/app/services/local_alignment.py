from app.services.global_alignment import (
    calculate_score,
    build_markers,
)
from app.services.traceback_service import build_traceback_positions



def initialize_matrix(
    rows: int,
    columns: int
) -> list[list[int]]:
    """
    Inicializa a matriz do Smith-Waterman.

    Diferentemente do alinhamento global,
    a primeira linha e a primeira coluna
    são preenchidas com zero.
    """
    return [
        [0 for _ in range(columns)]
        for _ in range(rows)
    ]


def initialize_traceback(
    rows: int,
    columns: int
) -> list[list[str | None]]:
    """
    Cria a matriz de direções.

    No Smith-Waterman, a primeira linha e a primeira
    coluna permanecem sem direção, pois o traceback
    termina ao atingir zero.
    """
    return [
        [None for _ in range(columns)]
        for _ in range(rows)
    ]


def fill_matrix(
    seq1: str,
    seq2: str,
    match: int,
    mismatch: int,
    gap: int,
    matrix: list[list[int]],
    traceback: list[list[str | None]]
) -> tuple[int, int]:
    """
    Preenche a matriz do Smith-Waterman.

    Retorna a posição da maior célula.

    Prioridade em caso de empate:
    1. Diagonal
    2. Vertical
    3. Horizontal
    """

    max_score = 0
    max_i = 0
    max_j = 0

    for i in range(1, len(seq1) + 1):
        for j in range(1, len(seq2) + 1):

            diagonal = (
                matrix[i - 1][j - 1]
                + calculate_score(
                    seq1[i - 1],
                    seq2[j - 1],
                    match,
                    mismatch
                )
            )

            vertical = (
                matrix[i - 1][j]
                + gap
            )

            horizontal = (
                matrix[i][j - 1]
                + gap
            )

            best_score = max(
                0,
                diagonal,
                vertical,
                horizontal
            )

            matrix[i][j] = best_score

            if best_score == 0:
                traceback[i][j] = None

            elif diagonal == best_score:
                traceback[i][j] = "D"

            elif vertical == best_score:
                traceback[i][j] = "V"

            else:
                traceback[i][j] = "H"

            if best_score > max_score:
                max_score = best_score
                max_i = i
                max_j = j

    return max_i, max_j


def perform_traceback(
    seq1: str,
    seq2: str,
    matrix: list[list[int]],
    traceback: list[list[str | None]],
    start_i: int,
    start_j: int
) -> tuple[str, str, list[str]]:
    """
    Reconstrói o alinhamento local.

    O traceback começa na maior célula e termina
    quando encontra uma célula com valor zero.
    """

    i = start_i
    j = start_j

    aligned_seq1 = []
    aligned_seq2 = []
    path = []

    while i > 0 and j > 0:

        if matrix[i][j] == 0:
            break

        direction = traceback[i][j]

        if direction == "D":

            aligned_seq1.append(seq1[i - 1])
            aligned_seq2.append(seq2[j - 1])
            path.append("D")

            i -= 1
            j -= 1

        elif direction == "V":

            aligned_seq1.append(seq1[i - 1])
            aligned_seq2.append("-")
            path.append("V")

            i -= 1

        elif direction == "H":

            aligned_seq1.append("-")
            aligned_seq2.append(seq2[j - 1])
            path.append("H")

            j -= 1

        else:
            raise ValueError(
                "Traceback inválido no Smith-Waterman."
            )

    aligned_seq1.reverse()
    aligned_seq2.reverse()
    path.reverse()

    return (
        "".join(aligned_seq1),
        "".join(aligned_seq2),
        path
    )


def smith_waterman(
    seq1: str,
    seq2: str,
    match: int,
    mismatch: int,
    gap: int
) -> dict:

    rows = len(seq1) + 1
    columns = len(seq2) + 1

    matrix = initialize_matrix(
        rows,
        columns
    )

    traceback = initialize_traceback(
        rows,
        columns
    )

    max_i, max_j = fill_matrix(
        seq1=seq1,
        seq2=seq2,
        match=match,
        mismatch=mismatch,
        gap=gap,
        matrix=matrix,
        traceback=traceback
    )

    aligned_seq1, aligned_seq2, path = perform_traceback(
        seq1=seq1,
        seq2=seq2,
        matrix=matrix,
        traceback=traceback,
        start_i=max_i,
        start_j=max_j
    )

    markers = build_markers(
        aligned_seq1,
        aligned_seq2
    )

    score = matrix[max_i][max_j]

    traceback_positions = build_traceback_positions(
        path=path,
        start_row=max_i,
        start_column=max_j
    )

    return {
        "score": score,
        "aligned_seq1": aligned_seq1,
        "aligned_seq2": aligned_seq2,
        "markers": markers,
        "matrix": matrix,
        "traceback": traceback_positions,
        "directions": traceback,
        "start_position": {
            "row": max_i,
            "column": max_j,
            "direction": "START"
        }
    }