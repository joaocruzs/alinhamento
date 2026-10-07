from pathlib import Path

from app.services.validation_service import (
    ValidationError,
    validate_sequences,
)


ALLOWED_EXTENSIONS = {".txt", ".fasta"}


def _decode_file(content: bytes) -> str:
    """
    Converte o conteúdo do arquivo para texto UTF-8.
    """
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        raise ValidationError(
            "Erro ao ler o arquivo. Utilize UTF-8."
        )


def _parse_txt(content: str) -> list[str]:
    """
    Interpreta um arquivo .txt contendo exatamente
    duas sequências, uma por linha.
    """
    sequences = [
        line.strip()
        for line in content.splitlines()
        if line.strip()
    ]

    return sequences


def _parse_fasta(content: str) -> list[str]:
    """
    Interpreta um arquivo FASTA.

    Exemplo:

    >Seq1
    ACGTAC
    >Seq2
    ACGTTC
    """
    sequences = []
    current_sequence = []

    for line in content.splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith(">"):
            if current_sequence:
                sequences.append("".join(current_sequence))
                current_sequence = []
        else:
            current_sequence.append(line)

    if current_sequence:
        sequences.append("".join(current_sequence))

    return sequences


def read_sequences_from_file(
    filename: str,
    content: bytes
) -> tuple[str, str]:

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            "Formato de arquivo incompatível. "
            "Utilize .txt ou .fasta."
        )

    decoded_content = _decode_file(content)

    if extension == ".fasta":
        sequences = _parse_fasta(decoded_content)
    else:
        sequences = _parse_txt(decoded_content)

    if len(sequences) != 2:
        raise ValidationError(
            "O arquivo deve conter exatamente duas sequências."
        )

    seq1, seq2 = validate_sequences(
        sequences[0],
        sequences[1]
    )

    return seq1, seq2