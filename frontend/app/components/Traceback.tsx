interface TracebackPosition {
  row: number;
  column: number;
  direction: string;
}

interface TracebackProps {
  traceback: TracebackPosition[];
}

export default function Traceback({
  traceback,
}: TracebackProps) {

  function getDirectionLabel(
    direction: string
  ) {
    switch (direction) {
      case "D":
        return "Diagonal — base contra base";

      case "V":
        return "Vertical — gap em Seq2";

      case "H":
        return "Horizontal — gap em Seq1";

      default:
        return "Desconhecida";
    }
  }

  return (
    <div className="rounded-xl bg-white p-6 shadow">

      <h3 className="text-xl font-bold">
        Traceback
      </h3>

      <div className="mt-5 overflow-x-auto">

        <table className="w-full border-collapse">

          <thead>
            <tr>
              <th className="border bg-gray-100 p-3">
                Passo
              </th>

              <th className="border bg-gray-100 p-3">
                Linha
              </th>

              <th className="border bg-gray-100 p-3">
                Coluna
              </th>

              <th className="border bg-gray-100 p-3">
                Direção
              </th>
            </tr>
          </thead>

          <tbody>

            {traceback.map((position, index) => (

              <tr key={index}>

                <td className="border p-3 text-center">
                  {index + 1}
                </td>

                <td className="border p-3 text-center">
                  {position.row}
                </td>

                <td className="border p-3 text-center">
                  {position.column}
                </td>

                <th className="border bg-gray-100 p-3">
                  Operação
                </th>

                <td className="border p-3 text-center font-bold">
                  {position.direction}
                </td>

              </tr>

            ))}

          </tbody>

        </table>

      </div>

    </div>
  );
}