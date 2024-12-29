import { useState, useEffect } from "react";
import axios from "axios";
import Table from "../components/Table";
import PieChart from "../components/PieChart";

export default function PeoplePage() {
  const [filters, setFilters] = useState({
    first_name: "",
    last_name: "",
    city: "",
    country: "",
    device: [],
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

  const handleDeviceChange = (e) => {
    const { value, checked } = e.target;
    console.log("Device change:", { value, checked });

    setFilters((prev) => {
      const newFilters = {
        ...prev,
        device: checked
          ? [...prev.device, value]
          : prev.device.filter((d) => d !== value),
      };
      console.log("Updated filters:", newFilters);
      return newFilters;
    });
  };

  const fetchResults = async () => {
    try {
      // Create params object
      const params = {
        ...filters,
        device: filters.device,
      };

      // Log exact params being sent
      console.log("Exact params being sent:", params);

      // Log the constructed URL
      const queryString = new URLSearchParams(params).toString();
      console.log(
        "Full URL being called:",
        `http://127.0.0.1:5000/api/people/filter?${queryString}`
      );

      const response = await axios.get(
        "http://127.0.0.1:5000/api/people/filter",
        {
          params,
          // Add paramsSerializer to handle arrays properly
          paramsSerializer: {
            indexes: null, // This will send device[]=value instead of device[0]=value
          },
        }
      );

      // Log the response data
      console.log("Response from server:", response.data);
      setResults(response.data);
      setCurrentPage(1); // Reset to page 1 whenever new results are fetched
    } catch (error) {
      console.error("Full error object:", error);
      console.error("Error response if any:", error.response);
    }
  };

  const paginate = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchResults();
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:5000/api/people/stats"
      );
      setStats(response.data);
    } catch (error) {
      console.error("Error fetching stats:", error);
    }
  };

  // Device chart custom colors
  const deviceColors = [
    "rgba(255, 99, 132, 0.8)", // Red for Android
    "rgba(54, 162, 235, 0.8)", // Blue for iPhone
    "rgba(75, 192, 192, 0.8)", // Green for Desktop
  ];

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Client Page</h1>
      <div className="grid grid-cols-2 gap-4">
        <input
          type="text"
          name="first_name"
          placeholder="First Name"
          value={filters.first_name}
          onChange={handleInputChange}
          className="p-2 border border-gray-300 rounded"
        />
        <input
          type="text"
          name="last_name"
          placeholder="Last Name"
          value={filters.last_name}
          onChange={handleInputChange}
          className="p-2 border border-gray-300 rounded"
        />
        <input
          type="text"
          name="city"
          placeholder="City"
          value={filters.city}
          onChange={handleInputChange}
          className="p-2 border border-gray-300 rounded"
        />
        <input
          type="text"
          name="country"
          placeholder="Country"
          value={filters.country}
          onChange={handleInputChange}
          className="p-2 border border-gray-300 rounded"
        />
        <div className="flex items-center space-x-4">
          <label>
            <input
              type="checkbox"
              value="Android"
              checked={filters.device.includes("Android")}
              onChange={handleDeviceChange}
              className="mr-2"
            />
            Android
          </label>
          <label>
            <input
              type="checkbox"
              value="iPhone"
              checked={filters.device.includes("iPhone")}
              onChange={handleDeviceChange}
              className="mr-2"
            />
            iPhone
          </label>
          <label>
            <input
              type="checkbox"
              value="Desktop"
              checked={filters.device.includes("Desktop")}
              onChange={handleDeviceChange}
              className="mr-2"
            />
            Desktop
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
      {stats && (
        <div className="flex justify-center items-center gap-8">
          <PieChart
            title="Client Distribution by Country"
            data={stats.country_stats.map((stat) => stat.percentage)}
            labels={stats.country_stats.map((stat) => stat.country)}
          />
          <PieChart
            title="Client Device Ownership Breakdown"
            data={stats.device_stats.map((stat) => stat.percentage)}
            labels={stats.device_stats.map((stat) => stat.device)}
            customColors={deviceColors}
          />
        </div>
      )}
    </div>
  );
}
