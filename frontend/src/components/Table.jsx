export default function Table({ data }) {
  if (!data || data.length === 0) {
    return <div className="mt-4 text-gray-600">No results found.</div>;
  }

  // Get columns from the first data item
  const columns = Object.keys(data[0]);

  // Helper function to format cell content
  const formatCellContent = (content) => {
    if (typeof content === "boolean") {
      return content.toString();
    }
    if (content === null || content === undefined) {
      return "";
    }
    return content;
  };

  return (
    <div className="mt-4 overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            {columns.map((column) => (
              <th
                key={column}
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                {column}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {data.map((row, rowIndex) => (
            <tr key={row.id || rowIndex}>
              {columns.map((column) => (
                <td key={column} className="px-6 py-4 whitespace-nowrap">
                  {formatCellContent(row[column])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
