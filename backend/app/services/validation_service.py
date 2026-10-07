from typing import Tuple


VALID_DNA_BASES = {"A", "C", "G", "T"}


class ValidationError(Exception):
    """
    Erro específico para problemas de validação
    das entradas do alinhamento.
    """
    pass


def normalize_sequence(sequence: str) -> str:
    """
    Remove espaços/quebras de linha e converte
    a sequência para letras maiúsculas.
    """

    if sequence is None:
        raise ValidationError("A sequência não pode ser nula.")

    normalized = "".join(sequence.split()).upper()

    return normalized


def validate_sequence(sequence: str, sequence_name: str) -> str:
    """
    Normaliza e valida uma sequência de DNA.

    Retorna a sequência normalizada caso seja válida.
    """

    normalized = normalize_sequence(sequence)

    if not normalized:
        raise ValidationError(
            f"{sequence_name} não pode ser vazia."
        )

    invalid_bases = set(normalized) - VALID_DNA_BASES

    if invalid_bases:
        invalid = ", ".join(sorted(invalid_bases))

        raise ValidationError(
            f"Base(s) inválida(s) em {sequence_name}: {invalid}. "
            f"Apenas A, C, G e T são permitidas."
        )

    return normalized


def validate_sequences(
    seq1: str,
    seq2: str
) -> Tuple[str, str]:
    """
    Valida as duas sequências e retorna
    ambas normalizadas.
    """

    normalized_seq1 = validate_sequence(seq1, "Seq1")
    normalized_seq2 = validate_sequence(seq2, "Seq2")

    return normalized_seq1, normalized_seq2


def validate_score_parameters(
    match: int,
    mismatch: int,
    gap: int
) -> tuple[int, int, int]:
    """
    Valida os parâmetros de pontuação.
    """

    if match is None:
        raise ValidationError(
            "O parâmetro Match é obrigatório."
        )

    if mismatch is None:
        raise ValidationError(
            "O parâmetro Mismatch é obrigatório."
        )

    if gap is None:
        raise ValidationError(
            "O parâmetro Gap é obrigatório."
        )

    if not isinstance(match, int):
        raise ValidationError(
            "O parâmetro Match deve ser numérico."
        )

    if not isinstance(mismatch, int):
        raise ValidationError(
            "O parâmetro Mismatch deve ser numérico."
        )

    if not isinstance(gap, int):
        raise ValidationError(
            "O parâmetro Gap deve ser numérico."
        )

    return match, mismatch, gap