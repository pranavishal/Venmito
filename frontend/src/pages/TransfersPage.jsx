import { useState, useEffect } from "react";
import axios from "axios";
import Table from "../components/Table";

export default function TransfersPage() {
  const [filters, setFilters] = useState({
    sender_id: "",
    recipient_id: "",
    date_after: "",
    date_before: "",
  });
  const [results, setResults] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [resultsPerPage] = useState(10);

  // Get current results
  const indexOfLastResult = currentPage * resultsPerPage;
  const indexOfFirstResult = indexOfLastResult - resultsPerPage;
  const currentResults = results.slice(indexOfFirstResult, indexOfLastResult);
  const totalPages = Math.ceil(results.length / resultsPerPage);

  useEffect(() => {
    // When component mounts, fetch all results
    fetchResults();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFilters({ ...filters, [name]: value });
  };

  const fetchResults = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:5000/api/transfers/filter",
        {
          params: filters,
        }
      );
      setResults(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const paginate = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Transfers Page</h1>
      <div className="grid grid-cols-2 gap-4">
        <input
          type="number"
          name="sender_id"
          placeholder="Sender ID"
          value={filters.sender_id}
          onChange={handleInputChange}
          className="p-2 border border-gray-300 rounded"
        />
        <input
          type="number"
          name="recipient_id"
          placeholder="Recipient ID"
          value={filters.recipient_id}
          onChange={handleInputChange}
          className="p-2 border border-gray-300 rounded"
        />
        <div className="flex flex-col">
          <label className="text-sm text-gray-600 mb-1">
            Date After (From)
          </label>
          <input
            type="date"
            name="date_after"
            value={filters.date_after}
            onChange={handleInputChange}
            className="p-2 border border-gray-300 rounded"
          />
        </div>
        <div className="flex flex-col">
          <label className="text-sm text-gray-600 mb-1">Date Before (To)</label>
          <input
            type="date"
            name="date_before"
            value={filters.date_before}
            onChange={handleInputChange}
            className="p-2 border border-gray-300 rounded"
          />
        </div>
      </div>
      <button
        onClick={fetchResults}
        className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        Filter
      </button>

      <Table data={currentResults} />

      {/* Pagination */}
      <div className="mt-4 flex justify-center space-x-2">
        <button
          onClick={() => paginate(currentPage - 1)}
          disabled={currentPage === 1}
          className="px-3 py-1 bg-gray-200 rounded disabled:opacity-50"
        >
          Previous
        </button>

        <span className="px-4 py-1">
          Page {currentPage} of {totalPages}
        </span>

        <button
          onClick={() => paginate(currentPage + 1)}
          disabled={currentPage === totalPages}
          className="px-3 py-1 bg-gray-200 rounded disabled:opacity-50"
        >
          Next
        </button>
      </div>

      <div className="mt-2 text-center text-sm text-gray-600">
        Showing {indexOfFirstResult + 1} to{" "}
        {Math.min(indexOfLastResult, results.length)} of {results.length}{" "}
        results
      </div>
    </div>
  );
}
