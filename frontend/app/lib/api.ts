export type AlignmentMode = "global" | "local";

export interface AlignmentRequest {
  seq1: string;
  seq2: string;
  match: number;
  mismatch: number;
  gap: number;
  mode: AlignmentMode;
}

export interface AlignmentParameters {
  match: number;
  mismatch: number;
  gap: number;
}

export interface TracebackPosition {
  row: number;
  column: number;
  direction: string;
}

export interface AlignmentResult {
  method: AlignmentMode;
  seq1: string;
  seq2: string;

  parameters: AlignmentParameters;

  score: number;

  aligned_seq1: string;
  markers: string;
  aligned_seq2: string;

  matrix: number[][];

  directions: (string | null)[][];

  traceback: TracebackPosition[];

  start_position: TracebackPosition | null;
}


const API_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "http://127.0.0.1:8000";

export async function executeAlignment(
  request: AlignmentRequest
): Promise<AlignmentResult> {

  const response = await fetch(
    `${API_URL}/api/alignment/`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    }
  );

  const data = await response.json();

  if (!response.ok) {
    throw new Error(
      data.detail || "Erro ao executar alinhamento."
    );
  }

  return data;
}