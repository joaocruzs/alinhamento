const VALID_DNA_BASES = /^[ACGT]+$/;

export function normalizeSequence(sequence: string): string {
  return sequence.replace(/\s/g, "").toUpperCase();
}

export function validateSequence(
  sequence: string,
  sequenceName: string
): string | null {
  const normalized = normalizeSequence(sequence);

  if (!normalized) {
    return `${sequenceName} não pode ser vazia.`;
  }

  if (!VALID_DNA_BASES.test(normalized)) {
    const invalidBases = [...new Set(
      normalized.split("").filter(
        (base) => !["A", "C", "G", "T"].includes(base)
      )
    )];

    return (
      `Base(s) inválida(s) em ${sequenceName}: ` +
      `${invalidBases.join(", ")}. ` +
      "Apenas A, C, G e T são permitidas."
    );
  }

  return null;
}

export function validateSequences(
  seq1: string,
  seq2: string
): string | null {
  const seq1Error = validateSequence(seq1, "Seq1");

  if (seq1Error) {
    return seq1Error;
  }

  const seq2Error = validateSequence(seq2, "Seq2");

  if (seq2Error) {
    return seq2Error;
  }

  return null;
}

export function validateScoreParameters(
  match: string,
  mismatch: string,
  gap: string
): string | null {
  if (match.trim() === "") {
    return "O parâmetro Match é obrigatório.";
  }

  if (mismatch.trim() === "") {
    return "O parâmetro Mismatch é obrigatório.";
  }

  if (gap.trim() === "") {
    return "O parâmetro Gap é obrigatório.";
  }

  if (!Number.isInteger(Number(match))) {
    return "O parâmetro Match deve ser numérico.";
  }

  if (!Number.isInteger(Number(mismatch))) {
    return "O parâmetro Mismatch deve ser numérico.";
  }

  if (!Number.isInteger(Number(gap))) {
    return "O parâmetro Gap deve ser numérico.";
  }

  return null;
}