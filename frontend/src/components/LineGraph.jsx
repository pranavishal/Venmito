import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

// Register Chart.js components
ChartJS.register(
  LineElement,
  PointElement,
  LinearScale,
  Title,
  Tooltip,
  Legend
);

// LineGraph component to render a line graph
export default function LineGraph({ title, data, labels }) {
  const chartData = {
    labels: labels, // X-axis labels (months)
    datasets: [
      {
        label: title,
        data: data, // Y-axis data (total money sent)
        borderColor: "rgba(75, 192, 192, 1)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
        tension: 0.4,
        fill: true,
      },
    ],
  };

  const options = {
    plugins: {
      title: {
        display: true,
        text: title,
        font: { size: 18 },
      },
    },
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: {
        title: {
          display: true,
          text: "Month",
        },
      },
      y: {
        title: {
          display: true,
          text: "Total Money Sent ($)",
        },
        beginAtZero: true,
      },
    },
  };

  return (
    <div
      className="flex justify-center items-center bg-white p-4 rounded-lg shadow"
      style={{ width: "100%", height: "400px" }}
    >
      <Line data={chartData} options={options} />
    </div>
  );
}
