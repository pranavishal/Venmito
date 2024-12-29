import { useState } from "react";

export default function StatTable({ data }) {
  const [currentPage, setCurrentPage] = useState(1);
  const resultsPerPage = 5;

  if (!data || data.length === 0) {
    return <div className="mt-4 text-gray-600">No results found.</div>;
  }

  // Calculate pagination details
  const indexOfLastResult = currentPage * resultsPerPage;
  const indexOfFirstResult = indexOfLastResult - resultsPerPage;
  const currentResults = data.slice(indexOfFirstResult, indexOfLastResult);
  const totalPages = Math.ceil(data.length / resultsPerPage);

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
    <div
      className="flex flex-col justify-between items-center bg-white p-4 rounded-lg shadow"
      style={{ width: "400px", height: "300px" }}
    >
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            {Object.keys(currentResults[0]).map((column) => (
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
          {currentResults.map((row, rowIndex) => (
            <tr key={row.id || rowIndex}>
              {Object.keys(row).map((column) => (
                <td key={column} className="px-6 py-4 whitespace-nowrap">
                  {formatCellContent(row[column])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>

      {/* Pagination Controls */}
      <div className="mt-4 flex justify-center items-center gap-4">
        <button
          onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
          disabled={currentPage === 1}
          className="px-3 py-1 bg-gray-200 rounded disabled:opacity-50"
        >
          Previous
        </button>
        <span>
          Page {currentPage} of {totalPages}
        </span>
        <button
          onClick={() =>
            setCurrentPage((prev) => Math.min(prev + 1, totalPages))
          }
          disabled={currentPage === totalPages}
          className="px-3 py-1 bg-gray-200 rounded disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </div>
  );
}
