from app.schemas.alignment_schema import AlignmentMode
from app.services.global_alignment import needleman_wunsch
from app.services.local_alignment import smith_waterman


def execute_alignment(
    seq1: str,
    seq2: str,
    match: int,
    mismatch: int,
    gap: int,
    mode: AlignmentMode
) -> dict:

    if mode == AlignmentMode.GLOBAL:

        return needleman_wunsch(
            seq1=seq1,
            seq2=seq2,
            match=match,
            mismatch=mismatch,
            gap=gap
        )

    if mode == AlignmentMode.LOCAL:

        return smith_waterman(
            seq1=seq1,
            seq2=seq2,
            match=match,
            mismatch=mismatch,
            gap=gap
        )

    raise ValueError(
        "Modo de alinhamento inválido."
    )