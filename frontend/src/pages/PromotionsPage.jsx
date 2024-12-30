import { useState, useEffect } from "react";
import axios from "axios";
import Table from "../components/Table";
import BarChart from "../components/BarChart";
import StatTable from "../components/StatTable";

export default function PromotionsPage() {
  const [filters, setFilters] = useState({
    promotion: "",
    email: "",
    responded: [],
  });
  const [results, setResults] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [resultsPerPage] = useState(10);
  const [countryStats, setCountryStats] = useState([]);
  const [promotionStats, setPromotionStats] = useState([]);
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
 // Fetch data on component mount
  useEffect(() => {
    const initializeData = async () => {
      setIsLoading(true);
      try {
        const [resultsResponse, statsResponse, promotionsResponse] = await Promise.all([
          fetchWithRetry("http://127.0.0.1:5000/api/promotions/filter"),
          fetchWithRetry("http://127.0.0.1:5000/api/promotions/stats"),
          fetchWithRetry("http://127.0.0.1:5000/api/promotions/stats/promotions")
        ]);
        
        setResults(resultsResponse);
        setCountryStats(statsResponse.country_stats);
        setPromotionStats(promotionsResponse);
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

  const handleResponseChange = (e) => {
    const { value, checked } = e.target;
    setFilters((prev) => ({
      ...prev,
      responded: checked
        ? [...prev.responded, value]
        : prev.responded.filter((r) => r !== value),
    }));
  };

  const fetchResults = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:5000/api/promotions/filter",
        {
          params: filters,
          paramsSerializer: {
            indexes: null,
          },
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
      <h1 className="text-2xl font-bold mb-4">Promotions Page</h1>
      <div className="grid grid-cols-2 gap-4">
        <input
          type="text"
          name="promotion"
          placeholder="Promotion"
          value={filters.promotion}
          onChange={handleInputChange}
          className="p-2 border border-gray-300 rounded"
        />
        <input
          type="text"
          name="email"
          placeholder="Email"
          value={filters.email}
          onChange={handleInputChange}
          className="p-2 border border-gray-300 rounded"
        />
        <div className="flex items-center space-x-4">
          <label>
            <input
              type="checkbox"
              value="yes"
              checked={filters.responded.includes("yes")}
              onChange={handleResponseChange}
              className="mr-2"
            />
            Responded Yes
          </label>
          <label>
            <input
              type="checkbox"
              value="no"
              checked={filters.responded.includes("no")}
              onChange={handleResponseChange}
              className="mr-2"
            />
            Responded No
          </label>
        </div>
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

      {/* Charts section */}
      {!isLoading && countryStats.length > 0 && promotionStats.length > 0 && (
        <div className="flex flex-col md:flex-row justify-center items-center gap-8">
          <div className="flex-1 flex justify-center">
            <BarChart
              title="Promotion Acceptance Rate by Country"
              data={countryStats.map((stat) => stat.response_rate)}
              labels={countryStats.map((stat) => stat.country)}
            />
          </div>
          <div className="flex-1 flex justify-center">
            <div>
              <h2 className="text-xl font-bold mb-4 text-center">
                Promotion Item Acceptance Rate (Descending)
              </h2>
              <StatTable data={promotionStats} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}