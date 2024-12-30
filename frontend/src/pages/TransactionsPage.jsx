import { useState, useEffect } from "react";
import axios from "axios";
import Table from "../components/Table";
import StatTable from "../components/StatTable";
import PieChart from "../components/PieChart";

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
  const [customerStats, setCustomerStats] = useState([]);
  const [storeStats, setStoreStats] = useState([]);
  const [spendingByCountry, setSpendingByCountry] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Get current results
  const indexOfLastResult = currentPage * resultsPerPage;
  const indexOfFirstResult = indexOfLastResult - resultsPerPage;
  const currentResults = results.slice(indexOfFirstResult, indexOfLastResult);
  const totalPages = Math.ceil(results.length / resultsPerPage);

  const fetchWithRetry = async (url, maxRetries = 5, delay = 1000) => {
    for (let i = 0; i < maxRetries; i++) {
      try {
        const response = await axios.get(url);
        return response.data;
      } catch (error) {
        if (i === maxRetries - 1) throw error;
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  };

  useEffect(() => {
    const initializeData = async () => {
      setIsLoading(true);
      try {
        const [resultsResponse, customerResponse, storeResponse, countryResponse] = await Promise.all([
          fetchWithRetry("http://127.0.0.1:5000/api/transactions/filter"),
          fetchWithRetry("http://127.0.0.1:5000/api/transactions/stats/customers"),
          fetchWithRetry("http://127.0.0.1:5000/api/transactions/stats/stores"),
          fetchWithRetry("http://127.0.0.1:5000/api/transactions/stats/spending_by_country")
        ]);
        
        setResults(resultsResponse);
        setCustomerStats(customerResponse);
        setStoreStats(storeResponse);
        setSpendingByCountry(countryResponse);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setIsLoading(false);
      }
    };

    initializeData();
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
      setCurrentPage(1);
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

      {/* Charts and Stats section */}
      {!isLoading && customerStats.length > 0 && storeStats.length > 0 && (
        <>
          <div className="flex flex-col md:flex-row justify-between items-start gap-8">
            <div className="flex-1 flex justify-center">
              <div>
                <h2 className="text-xl font-bold mb-4 text-center">
                  Customer Spending (Greatest to Least)
                </h2>
                <StatTable data={customerStats} />
              </div>
            </div>
            <div className="flex-1 flex justify-center">
              <div>
                <h2 className="text-xl font-bold mb-4 text-center">
                  Store Revenue (Greatest to Least)
                </h2>
                <StatTable data={storeStats} />
              </div>
            </div>
          </div>
          <div className="flex justify-center mt-8">
            <div>
              <h2 className="text-xl font-bold mb-4 text-center"></h2>
              <PieChart
                title="Transactions Spent by Country"
                data={spendingByCountry.map((stat) => stat.total_spent)}
                labels={spendingByCountry.map((stat) => stat.country)}
              />
            </div>
          </div>
        </>
      )}
    </div>
  );
}