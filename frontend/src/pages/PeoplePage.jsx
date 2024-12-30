import { useState, useEffect } from "react";
import axios from "axios";
import Table from "../components/Table";
import PieChart from "../components/PieChart";

// PeoplePage component to display people data
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
 const [stats, setStats] = useState(null);
 const [isLoading, setIsLoading] = useState(true);

 // Get current results
 const indexOfLastResult = currentPage * resultsPerPage;
 const indexOfFirstResult = indexOfLastResult - resultsPerPage;
 const currentResults = results.slice(indexOfFirstResult, indexOfLastResult);
 const totalPages = Math.ceil(results.length / resultsPerPage);

 // Fetch data with retries
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
       const [resultsResponse, statsResponse] = await Promise.all([
         fetchWithRetry("http://127.0.0.1:5000/api/people/filter"),
         fetchWithRetry("http://127.0.0.1:5000/api/people/stats")
       ]);
       
       setResults(resultsResponse);
       setStats(statsResponse);
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

 const handleDeviceChange = (e) => {
   const { value, checked } = e.target;
   setFilters((prev) => ({
     ...prev,
     device: checked
       ? [...prev.device, value]
       : prev.device.filter((d) => d !== value),
   }));
 };
// Fetch filtered results
 const fetchResults = async () => {
   try {
     const response = await axios.get(
       "http://127.0.0.1:5000/api/people/filter",
       {
         params: { ...filters },
         paramsSerializer: {
           indexes: null,
         },
       }
     );
     setResults(response.data);
     setCurrentPage(1);
   } catch (error) {
     console.error("Error fetching results:", error);
   }
 };

 const paginate = (pageNumber) => {
   setCurrentPage(pageNumber);
 };

 // Device chart custom colors
 const deviceColors = [
   "rgba(255, 99, 132, 0.8)",
   "rgba(54, 162, 235, 0.8)",
   "rgba(75, 192, 192, 0.8)",
 ];

 return (
   <div className="p-4">
     <h1 className="text-2xl font-bold mb-4">Client Page</h1>
     
     {/* Filters */}
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
       {Math.min(indexOfLastResult, results.length)} of {results.length} results
     </div>

     {/* Charts section */}
     {!isLoading && stats && (
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