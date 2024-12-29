import { useState, useEffect } from "react";

export default function InsightsPage() {
  // Initialize state from localStorage if available
  const [insights, setInsights] = useState(() => {
    const savedData = localStorage.getItem("venmito_insights");
    return savedData
      ? JSON.parse(savedData)
      : {
          customers: [],
          promotions: [],
          transactions: [],
          transfers: [],
        };
  });

  const [loading, setLoading] = useState({
    customers: true,
    promotions: true,
    transactions: true,
    transfers: true,
  });

  const [errors, setErrors] = useState({});

  useEffect(() => {
    const fetchInsights = async () => {
      // Check if we already fetched insights in this browser session
      const currentSession = localStorage.getItem("venmito_session");
      const browserSession = sessionStorage.getItem("insights_fetched");

      // If we have insights and they're from the current session, don't fetch again
      if (currentSession && browserSession && insights.customers.length > 0) {
        setLoading({
          customers: false,
          promotions: false,
          transactions: false,
          transfers: false,
        });
        return;
      }

      console.log("Fetching fresh insights...");
      const categories = [
        "customers",
        "promotions",
        "transactions",
        "transfers",
      ];

      for (const category of categories) {
        try {
          const response = await fetch(
            `http://127.0.0.1:5000/api/initialize/${category}`,
            {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
            }
          );

          if (!response.ok) {
            throw new Error(`Server returned ${response.status}`);
          }

          const data = await response.json();

          if (!data.insights) {
            throw new Error(`No insights data received`);
          }

          setInsights((prev) => {
            const newInsights = {
              ...prev,
              [category]: data.insights
                .split("\n")
                .filter((insight) => insight.trim()),
            };
            localStorage.setItem(
              "venmito_insights",
              JSON.stringify(newInsights)
            );
            return newInsights;
          });
        } catch (error) {
          console.error(`Error fetching ${category} insights:`, error);
          setErrors((prev) => ({
            ...prev,
            [category]: error.message || `Failed to fetch insights`,
          }));
        } finally {
          setLoading((prev) => ({
            ...prev,
            [category]: false,
          }));
        }
      }

      // Mark that we've fetched insights in this browser session
      sessionStorage.setItem("insights_fetched", "true");
      localStorage.setItem("venmito_session", Date.now().toString());
    };

    fetchInsights();
  }, []);

  const categories = [
    { id: "customers", title: "Customer Insights" },
    { id: "promotions", title: "Promotion Insights" },
    { id: "transactions", title: "Transaction Insights" },
    { id: "transfers", title: "Transfer Insights" },
  ];

  return (
    <div className="p-6 space-y-8">
      <h1 className="text-3xl font-bold">Business Insights Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {categories.map(({ id, title }) => (
          <div key={id} className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">{title}</h2>

            {loading[id] ? (
              <div className="flex items-center justify-center h-32">
                <div className="animate-pulse text-gray-500">
                  Loading insights...
                </div>
              </div>
            ) : errors[id] ? (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative">
                <strong className="font-medium">Error: </strong>
                <span className="block sm:inline">{errors[id]}</span>
              </div>
            ) : insights[id]?.length > 0 ? (
              <ul className="space-y-3">
                {insights[id].map((insight, index) => (
                  <li
                    key={index}
                    className="text-gray-700 pl-4 border-l-2 border-blue-500"
                  >
                    {insight.replace(/^-\s*/, "")}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500 text-center">
                No insights available.
              </p>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
