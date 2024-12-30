import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
  Title,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
  Title
);

// BarChart component to render a bar chart
export default function BarChart({ title, data, labels, customColors }) {
  // Color generation logic
  const generateColors = (count) => {
    const colors = [];
    for (let i = 0; i < count; i++) {
      // Golden angle approximation
      const hue = (i * 137.508) % 360; 
      colors.push(`hsl(${hue}, 70%, 60%)`);
    }
    return colors;
  };

  // Use provided customColors or generate new ones based on data length
  const colors = customColors || generateColors(data.length);

  const chartData = {
    labels: labels,
    datasets: [
      {
        label: title,
        data: data,
        backgroundColor: colors,
      },
    ],
  };

  const options = {
    plugins: {
      title: {
        display: true,
        text: title,
      },
    },
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  return (
    <div
      className="flex justify-center items-center bg-white p-4 rounded-lg shadow"
      style={{ width: "600px", height: "600px", margin: "0 auto" }}
    >
      <Bar data={chartData} options={options} />
    </div>
  );
}
