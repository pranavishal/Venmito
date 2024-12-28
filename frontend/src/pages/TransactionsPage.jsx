import { useState, useEffect } from "react";
import axios from "axios";
import Table from "../components/Table";

export default function TransactionsPage() {
  const [filters, setFilters] = useState({
    transaction_id: "",
    customer_id: "",
    store: "",
    item_name: "",
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
        "http://127.0.0.1:5000/api/transactions/filter",
        {
          params: filters,
        }
      );
      setResults(response.data);
      setCurrentPage(1); // Reset to page 1 whenever new results are fetched
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const paginate = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Transactions Page</h1>
      <div className="grid grid-cols-2 gap-4">
        <input
          type="number"
          name="transaction_id"
          placeholder="Transaction ID"
          value={filters.transaction_id}
          onChange={handleInputChange}
          className="p-2 border border-gray-300 rounded"
        />
        <input
          type="number"
          name="customer_id"
          placeholder="Customer ID"
          value={filters.customer_id}
          onChange={handleInputChange}
          className="p-2 border border-gray-300 rounded"
        />
        <input
          type="text"
          name="store"
          placeholder="Store"
          value={filters.store}
          onChange={handleInputChange}
          className="p-2 border border-gray-300 rounded"
        />
        <input
          type="text"
          name="item_name"
          placeholder="Item Name"
          value={filters.item_name}
          onChange={handleInputChange}
          className="p-2 border border-gray-300 rounded"
        />
      </div>
      <button
        onClick={fetchResults}
        className="mt-4 px-4 py-2 bg-blue-500 text-white rounded"
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
