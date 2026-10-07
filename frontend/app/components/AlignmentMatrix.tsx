interface AlignmentMatrixProps {
  matrix: number[][];
  directions: (string | null)[][];
  seq1: string;
  seq2: string;
  traceback: {
    row: number;
    column: number;
    direction: string;
  }[];
}

export default function AlignmentMatrix({
  matrix,
  directions,
  seq1,
  seq2,
  traceback,
}: AlignmentMatrixProps) {

  const tracebackCells = new Set(
    traceback.map(
      (position) =>
        `${position.row}-${position.column}`
    )
  );

  const startCell =
  traceback.length > 0
    ? traceback[0]
    : null;

  const endCell =
    traceback.length > 0
      ? traceback[traceback.length - 1]
      : null;

  return (
    <div className="rounded-xl bg-white p-6 shadow">

      <h3 className="text-xl font-bold">
        Matriz de programação dinâmica
      </h3>

      <p className="mt-2 text-sm text-gray-600">
        As células destacadas fazem parte do
        traceback escolhido pelo algoritmo.
      </p>

      <div className="mt-6 overflow-x-auto">

        <table className="border-collapse">

          <thead>
            <tr>

              <th className="h-12 w-12 border bg-gray-100">
                ∅
              </th>

              {seq2.split("").map((base, index) => (
                <th
                  key={index}
                  className="h-12 w-12 border bg-gray-100 font-bold"
                >
                  {base}
                </th>
              ))}

            </tr>
          </thead>

          <tbody>

            {matrix.map((row, rowIndex) => (

              <tr key={rowIndex}>

                <th className="h-12 w-12 border bg-gray-100 font-bold">
                  {rowIndex === 0
                    ? "∅"
                    : seq1[rowIndex - 1]}
                </th>

                {row.map((value, columnIndex) => {

                  const isTraceback =
                    tracebackCells.has(
                      `${rowIndex}-${columnIndex}`
                    );

                  const isStart =
                    startCell?.row === rowIndex &&
                    startCell?.column === columnIndex;

                  const isEnd =
                    endCell?.row === rowIndex &&
                    endCell?.column === columnIndex;

                  const direction =
                    directions[rowIndex]?.[columnIndex];

                  return (
                    <td
                      key={columnIndex}
                      className={`relative h-12 w-12 border text-center font-mono ${
                        isStart
                          ? "bg-blue-200 font-bold"
                          : isEnd
                            ? "bg-purple-200 font-bold"
                            : isTraceback
                              ? "bg-yellow-100 font-bold"
                              : "bg-white"
                      }`}
                    >

                      <span>
                        {value}
                      </span>

                      {direction && (
                        <span className="absolute bottom-0 right-1 text-[9px] text-gray-500">
                          {direction}
                        </span>
                      )}

                    </td>
                  );
                })}

              </tr>

            ))}

          </tbody>

        </table>

      </div>

      <div className="mt-4 flex flex-wrap gap-4 text-sm">

        <span>
          <span className="mr-1 inline-block h-3 w-3 bg-blue-200" />
          Início
        </span>

        <span>
          <span className="mr-1 inline-block h-3 w-3 bg-yellow-100" />
          Traceback
        </span>

        <span>
          <span className="mr-1 inline-block h-3 w-3 bg-purple-200" />
          Fim
        </span>

      </div>
      
      <div className="mt-4 flex gap-4 text-sm">

        <span>
          <strong>D</strong> = diagonal
        </span>

        <span>
          <strong>V</strong> = vertical
        </span>

        <span>
          <strong>H</strong> = horizontal
        </span>

      </div>

    </div>
  );
}