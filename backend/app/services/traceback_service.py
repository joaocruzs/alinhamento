from app.schemas.alignment_schema import TracebackPosition


def build_traceback_positions(
    path: list[str],
    start_row: int,
    start_column: int
) -> list[TracebackPosition]:
    """
    Converte o caminho do traceback em posições
    explícitas da matriz.

    O caminho recebido está na ordem em que o
    alinhamento é construído, ou seja, do início
    para o fim do alinhamento.
    """

    positions = []

    row = start_row
    column = start_column

    for direction in path:
        positions.append(
            TracebackPosition(
                row=row,
                column=column,
                direction=direction
            )
        )

        if direction == "D":
            row -= 1
            column -= 1

        elif direction == "V":
            row -= 1

        elif direction == "H":
            column -= 1

        else:
            raise ValueError(
                f"Direção de traceback inválida: {direction}"
            )

    return positions