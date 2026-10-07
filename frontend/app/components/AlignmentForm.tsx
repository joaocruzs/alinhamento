"use client";

import {
  normalizeSequence,
  validateSequences,
  validateScoreParameters,
} from "../lib/validation";

import { useState } from "react";

import {
  AlignmentMode,
  AlignmentRequest,
  AlignmentResult,
  executeAlignment,
} from "../lib/api";

interface AlignmentFormProps {
  onResult: (result: AlignmentResult) => void;
}

export default function AlignmentForm({
  onResult,
}: AlignmentFormProps) {

  const [fileName, setFileName] = useState("");
  const [seq1, setSeq1] = useState("");
  const [seq2, setSeq2] = useState("");

  const [match, setMatch] = useState("2");
  const [mismatch, setMismatch] = useState("-1");
  const [gap, setGap] = useState("-2");

  const [mode, setMode] =
    useState<AlignmentMode>("global");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      const normalizedSeq1 = normalizeSequence(seq1);
      const normalizedSeq2 = normalizeSequence(seq2);

      const sequenceError = validateSequences(
        normalizedSeq1,
        normalizedSeq2
      );

      if (sequenceError) {
        setError(sequenceError);
        return;
      }

      const scoreError = validateScoreParameters(
        match,
        mismatch,
        gap
      );

      if (scoreError) {
        setError(scoreError);
        return;
      }

      const request = {
        seq1: normalizedSeq1,
        seq2: normalizedSeq2,
        match: Number(match),
        mismatch: Number(mismatch),
        gap: Number(gap),
        mode,
      };

      const result = await executeAlignment(request);

      setSeq1(normalizedSeq1);
      setSeq2(normalizedSeq2);

      onResult(result);
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("Ocorreu um erro ao executar o alinhamento.");
      }
    } finally {
      setLoading(false);
    }
  }

function handleFileChange(
  event: React.ChangeEvent<HTMLInputElement>
) {
  const file = event.target.files?.[0];

  if (!file) {
    return;
  }

  setError("");
  setFileName("");

  const extension = file.name
    .split(".")
    .pop()
    ?.toLowerCase();

  if (extension !== "txt" && extension !== "fasta") {
    setError(
      "Formato de arquivo incompatível. Utilize .txt ou .fasta."
    );
    event.target.value = "";
    return;
  }

  setFileName(file.name);

  const reader = new FileReader();

  reader.onerror = () => {
    setError("Não foi possível ler o arquivo.");
    setFileName("");
  };

  reader.onload = () => {
    try {
      const content = String(reader.result);

      const lines = content
        .split(/\r?\n/)
        .map((line) => line.trim())
        .filter(Boolean);

      let sequences: string[] = [];

      if (extension === "fasta") {
        let current = "";

        for (const line of lines) {
          if (line.startsWith(">")) {
            if (current) {
              sequences.push(current);
              current = "";
            }
          } else {
            current += line;
          }
        }

        if (current) {
          sequences.push(current);
        }
      } else {
        sequences = lines;
      }

      if (sequences.length !== 2) {
        setError(
          "O arquivo deve conter exatamente duas sequências."
        );
        setFileName("");
        return;
      }

      const normalizedSeq1 = normalizeSequence(sequences[0]);
      const normalizedSeq2 = normalizeSequence(sequences[1]);

      const sequenceError = validateSequences(
        normalizedSeq1,
        normalizedSeq2
      );

      if (sequenceError) {
        setError(sequenceError);
        setFileName("");
        return;
      }

      setSeq1(normalizedSeq1);
      setSeq2(normalizedSeq2);
      setError("");
    } catch {
      setError("Erro ao processar o conteúdo do arquivo.");
      setFileName("");
    }
  };

  reader.readAsText(file);
}

  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-6"
    >
      <div>
        <label className="block font-semibold">
          Carregar arquivo
        </label>

        <input
          type="file"
          accept=".txt,.fasta"
          onChange={handleFileChange}
          className="mt-2 block w-full rounded-lg border p-3"
        />

        {fileName && (
          <p className="mt-2 text-sm text-gray-600">
            Arquivo selecionado: {fileName}
          </p>
        )}
      </div>
      
      <div>
        <label className="block font-semibold">
          Sequência 1
        </label>

        <textarea
          value={seq1}
          onChange={(event) =>
            setSeq1(event.target.value)
          }
          placeholder="Ex.: ACGTAC"
          className="mt-2 w-full rounded-lg border p-3"
          rows={4}
        />
      </div>

      <div>
        <label className="block font-semibold">
          Sequência 2
        </label>

        <textarea
          value={seq2}
          onChange={(event) =>
            setSeq2(event.target.value)
          }
          placeholder="Ex.: ACGTTC"
          className="mt-2 w-full rounded-lg border p-3"
          rows={4}
        />
      </div>

      <div className="grid grid-cols-1 gap-4 md:grid-cols-3">

        <div>
          <label className="block font-semibold">
            Match
          </label>

          <input
            type="number"
            value={match}
            onChange={(event) =>
              setMatch(event.target.value)
            }
            className="mt-2 w-full rounded-lg border p-3"
          />
        </div>

        <div>
          <label className="block font-semibold">
            Mismatch
          </label>

          <input
            type="number"
            value={mismatch}
            onChange={(event) =>
              setMismatch(event.target.value)
            }
            className="mt-2 w-full rounded-lg border p-3"
          />
        </div>

        <div>
          <label className="block font-semibold">
            Gap
          </label>

          <input
            type="number"
            value={gap}
            onChange={(event) =>
              setGap(event.target.value)
            }
            className="mt-2 w-full rounded-lg border p-3"
          />
        </div>

      </div>

      <div>
        <span className="block font-semibold">
          Método
        </span>

        <div className="mt-2 flex gap-6">

          <label className="flex items-center gap-2">
            <input
              type="radio"
              value="global"
              checked={mode === "global"}
              onChange={() =>
                setMode("global")
              }
            />
            Global — Needleman-Wunsch
          </label>

          <label className="flex items-center gap-2">
            <input
              type="radio"
              value="local"
              checked={mode === "local"}
              onChange={() =>
                setMode("local")
              }
            />
            Local — Smith-Waterman
          </label>

        </div>
      </div>

      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4">
          <p className="font-semibold text-red-700">
            Não foi possível executar o alinhamento.
          </p>

          <p className="mt-1 text-sm text-red-600">
            {error}
          </p>
        </div>
      )}

      <button
        type="submit"
        disabled={loading}
        className="rounded-lg bg-black px-6 py-3 font-semibold text-white disabled:cursor-not-allowed disabled:opacity-50"
      >
        {loading ? "Executando..." : "Executar alinhamento"}
      </button>

    </form>
  );
}