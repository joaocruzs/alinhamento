import AlignmentMatrix from "./AlignmentMatrix";
import Traceback from "./Traceback";

import {
  AlignmentResult as AlignmentResultType,
} from "../lib/api";

interface AlignmentResultProps {
  result: AlignmentResultType;
}

export default function AlignmentResult({
  result,
}: AlignmentResultProps) {

  const methodName =
    result.method === "global"
      ? "Needleman-Wunsch"
      : "Smith-Waterman";

function getAlignmentClass(
  base1: string,
  base2: string
) {
  if (base1 === "-" || base2 === "-") {
    return "bg-gray-200";
  }

  if (base1 === base2) {
    return "bg-green-100 text-green-800";
  }

  return "bg-red-100 text-red-800";
}

  return (
    <div className="space-y-6">

      {/* RESUMO */}

      <div className="rounded-xl bg-white p-6 shadow">

        <h2 className="text-2xl font-bold">
          Resultado do alinhamento
        </h2>

        <div className="mt-5 grid gap-4 md:grid-cols-2">

          <div>
            <span className="text-sm text-gray-500">
              Método
            </span>

            <p className="font-semibold">
              {methodName}
            </p>
          </div>

          <div>
            <span className="text-sm text-gray-500">
              Score final
            </span>

            <p className="text-2xl font-bold">
              {result.score}
            </p>
          </div>

        </div>

      </div>


      {/* PARÂMETROS */}

      <div className="rounded-xl bg-white p-6 shadow">

        <h3 className="text-xl font-bold">
          Parâmetros
        </h3>

        <div className="mt-4 grid gap-4 md:grid-cols-3">

          <div className="rounded-lg bg-gray-50 p-4">
            <span className="text-sm text-gray-500">
              Match
            </span>

            <p className="text-xl font-bold">
              {result.parameters.match}
            </p>
          </div>

          <div className="rounded-lg bg-gray-50 p-4">
            <span className="text-sm text-gray-500">
              Mismatch
            </span>

            <p className="text-xl font-bold">
              {result.parameters.mismatch}
            </p>
          </div>

          <div className="rounded-lg bg-gray-50 p-4">
            <span className="text-sm text-gray-500">
              Gap
            </span>

            <p className="text-xl font-bold">
              {result.parameters.gap}
            </p>
          </div>

        </div>

      </div>


      {/* SEQUÊNCIAS ORIGINAIS */}

      <div className="rounded-xl bg-white p-6 shadow">

        <h3 className="text-xl font-bold">
          Sequências originais
        </h3>

        <div className="mt-4 space-y-3 font-mono">

          <div>
            <span className="mr-3 font-sans font-bold">
              Seq1:
            </span>

            {result.seq1}
          </div>

          <div>
            <span className="mr-3 font-sans font-bold">
              Seq2:
            </span>

            {result.seq2}
          </div>

        </div>

      </div>


      {/* ALINHAMENTO */}

      <div className="rounded-xl bg-white p-6 shadow">

        <h3 className="text-xl font-bold">
          Alinhamento reconstruído
        </h3>

        <div className="mt-5 overflow-x-auto rounded-lg bg-gray-50 p-5">

          <div className="flex font-mono text-lg">

            {result.aligned_seq1
              .split("")
              .map((base, index) => {

                const base2 =
                  result.aligned_seq2[index];

                return (
                  <div
                    key={index}
                    className={`min-w-8 border p-2 text-center ${getAlignmentClass(
                      base,
                      base2
                    )}`}
                  >
                    {base}
                  </div>
                );
              })}

          </div>

          <div className="flex font-mono text-lg">

            {result.markers
              .split("")
              .map((marker, index) => (
                <div
                  key={index}
                  className="min-w-8 p-2 text-center font-bold"
                >
                  {marker === " " ? "·" : marker}
                </div>
              ))}

          </div>

          <div className="flex font-mono text-lg">

            {result.aligned_seq2
              .split("")
              .map((base, index) => {

                const base1 =
                  result.aligned_seq1[index];

                return (
                  <div
                    key={index}
                    className={`min-w-8 border p-2 text-center ${getAlignmentClass(
                      base1,
                      base
                    )}`}
                  >
                    {base}
                  </div>
                );
              })}

          </div>

        </div>

        </div>

        <div className="mt-4 flex flex-wrap gap-5 text-sm text-gray-600">

          <span>
            <strong>|</strong> Match
          </span>

          <span>
            <strong>.</strong> Mismatch
          </span>

          <span>
            espaço = Gap
          </span>

        </div>


      {/* MATRIZ */}

      <AlignmentMatrix
        matrix={result.matrix}
        directions={result.directions}
        seq1={result.seq1}
        seq2={result.seq2}
        traceback={result.traceback}
      />

      <Traceback
        traceback={result.traceback}
      />

      {/* POSIÇÃO INICIAL DO TRACEBACK */}

      {result.start_position && (
        <div className="rounded-xl bg-white p-6 shadow">

          <h3 className="text-xl font-bold">
            Ponto inicial do traceback
          </h3>

          <div className="mt-4 grid gap-4 md:grid-cols-3">

            <div className="rounded-lg bg-gray-50 p-4">
              <p className="text-sm text-gray-500">
                Linha
              </p>

              <p className="text-2xl font-bold">
                {result.start_position.row}
              </p>
            </div>

            <div className="rounded-lg bg-gray-50 p-4">
              <p className="text-sm text-gray-500">
                Coluna
              </p>

              <p className="text-2xl font-bold">
                {result.start_position.column}
              </p>
            </div>

            <div className="rounded-lg bg-gray-50 p-4">
              <p className="text-sm text-gray-500">
                Direção
              </p>

              <p className="text-2xl font-bold">
                {result.start_position.direction}
              </p>
            </div>

          </div>

        </div>
      )}

    </div>
  );
}