from typing import Literal
from app.services.traceback_service import build_traceback_positions

Direction = Literal["D", "V", "H"]


def calculate_score(
    base1: str,
    base2: str,
    match: int,
    mismatch: int
) -> int:
    """
    Calcula a pontuação entre duas bases.
    """
    if base1 == base2:
        return match

    return mismatch


def initialize_matrix(
    rows: int,
    columns: int,
    gap: int
) -> list[list[int]]:
    """
    Inicializa a matriz do Needleman-Wunsch.

    A primeira célula é 0.
    A primeira linha e a primeira coluna recebem
    penalidades acumuladas de gap.
    """
    matrix = [
        [0 for _ in range(columns)]
        for _ in range(rows)
    ]

    for i in range(1, rows):
        matrix[i][0] = matrix[i - 1][0] + gap

    for j in range(1, columns):
        matrix[0][j] = matrix[0][j - 1] + gap

    return matrix


def initialize_traceback(
    rows: int,
    columns: int
) -> list[list[str | None]]:
    """
    Cria a matriz que armazenará a direção escolhida
    para cada célula.
    """
    traceback = [
        [None for _ in range(columns)]
        for _ in range(rows)
    ]

    for i in range(1, rows):
        traceback[i][0] = "V"

    for j in range(1, columns):
        traceback[0][j] = "H"

    return traceback


def fill_matrix(
    seq1: str,
    seq2: str,
    match: int,
    mismatch: int,
    gap: int,
    matrix: list[list[int]],
    traceback: list[list[str | None]]
) -> None:
    """
    Preenche a matriz de programação dinâmica.

    Prioridade em caso de empate:
    1. Diagonal
    2. Vertical
    3. Horizontal
    """

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
                diagonal,
                vertical,
                horizontal
            )

            matrix[i][j] = best_score

            # A ordem das verificações implementa
            # a prioridade D > V > H.
            if diagonal == best_score:
                traceback[i][j] = "D"

            elif vertical == best_score:
                traceback[i][j] = "V"

            else:
                traceback[i][j] = "H"


def perform_traceback(
    seq1: str,
    seq2: str,
    traceback: list[list[str | None]]
) -> tuple[str, str, list[str]]:
    """
    Reconstrói o alinhamento a partir do canto inferior
    direito até a origem.
    """

    i = len(seq1)
    j = len(seq2)

    aligned_seq1 = []
    aligned_seq2 = []
    path = []

    while i > 0 or j > 0:

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
                "Traceback inválido: "
                "não foi encontrada uma direção."
            )

    aligned_seq1.reverse()
    aligned_seq2.reverse()
    path.reverse()

    return (
        "".join(aligned_seq1),
        "".join(aligned_seq2),
        path
    )


def build_markers(
    aligned_seq1: str,
    aligned_seq2: str
) -> str:
    """
    Cria a representação visual do alinhamento.

    | = match
    . = mismatch
      = gap
    """

    markers = []

    for base1, base2 in zip(
        aligned_seq1,
        aligned_seq2
    ):
        if base1 == "-" or base2 == "-":
            markers.append(" ")

        elif base1 == base2:
            markers.append("|")

        else:
            markers.append(".")

    return "".join(markers)


def needleman_wunsch(
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
        columns,
        gap
    )

    traceback = initialize_traceback(
        rows,
        columns
    )

    fill_matrix(
        seq1,
        seq2,
        match,
        mismatch,
        gap,
        matrix,
        traceback
    )

    aligned_seq1, aligned_seq2, path = perform_traceback(
        seq1,
        seq2,
        traceback
    )

    markers = build_markers(
        aligned_seq1,
        aligned_seq2
    )

    score = matrix[-1][-1]

    traceback_positions = build_traceback_positions(
        path=path,
        start_row=len(seq1),
        start_column=len(seq2)
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
            "row": len(seq1),
            "column": len(seq2),
            "direction": "START"
        }
    }