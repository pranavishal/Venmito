import { Link } from "react-router-dom";

export default function LandingPage() {
  const sections = [
    {
      title: "Client Analytics",
      path: "/people",
      description: "Comprehensive client database with filtering capabilities across names, locations, and device preferences. Features interactive visualizations showing client distribution by country and device ownership patterns.",
      features: [
        "Advanced filtering by name, location, and device type",
        "Geographic distribution analysis",
        "Device ownership insights",
        "Interactive data tables with pagination"
      ],
      icon: "👥"
    },
    {
      title: "Promotion Performance",
      path: "/promotions",
      description: "Track and analyze promotion campaigns with detailed response metrics. Visualize acceptance rates across different regions and compare promotion effectiveness.",
      features: [
        "Filter promotions by type and recipient",
        "Regional acceptance rate analysis",
        "Promotional item performance rankings",
        "Response rate tracking"
      ],
      icon: "📊"
    },
    {
      title: "Transaction Monitoring",
      path: "/transactions",
      description: "Detailed transaction tracking system with store and customer insights. Analyze spending patterns and store performance through interactive visualizations.",
      features: [
        "Transaction filtering and search",
        "Individual customer spending analysis",
        "Store revenue tracking",
        "Geographic spending distribution"
      ],
      icon: "💳"
    },
    {
      title: "Transfer Analytics",
      path: "/transfers",
      description: "Monitor money movement patterns with comprehensive transfer tracking. Analyze sending and receiving trends across regions and time periods.",
      features: [
        "Transfer filtering by user and date",
        "Regional money flow analysis",
        "Temporal trend visualization",
        "Sender/receiver patterns"
      ],
      icon: "💱"
    },
    {
      title: "AI Driven Business Insights",
      path: "/insights",
      description: "AI-powered analysis providing actionable insights derived from all data sources. Get strategic recommendations for business growth and optimization.",
      features: [
        "AI-generated business insights",
        "Cross-Table data analysis",
        "Strategic recommendations",
        "Growth opportunity identification"
      ],
      icon: "💡"
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-gray-800 text-white py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h1 className="text-4xl font-bold text-center mb-4">
            Welcome to Venmito Analytics
          </h1>
          <p className="text-xl text-gray-300 text-center max-w-3xl mx-auto">
            A comprehensive platform for analyzing client behavior, monitoring transactions,
            tracking promotions, and gaining valuable business insights. Use the navigation bar above or the cards below to navigate to different sections.
          </p>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {sections.map((section) => (
            <Link
              key={section.path}
              to={section.path}
              className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden"
            >
              <div className="p-6">
                <div className="text-3xl mb-4">{section.icon}</div>
                <h2 className="text-2xl font-bold mb-4 text-gray-800">
                  {section.title}
                </h2>
                <p className="text-gray-600 mb-6">{section.description}</p>
                <div className="space-y-2">
                  {section.features.map((feature, index) => (
                    <div
                      key={index}
                      className="flex items-center text-sm text-gray-500"
                    >
                      <span className="mr-2">•</span>
                      {feature}
                    </div>
                  ))}
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}