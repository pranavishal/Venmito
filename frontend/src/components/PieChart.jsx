import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend, Title } from "chart.js";

// Register ChartJS components
ChartJS.register(ArcElement, Tooltip, Legend, Title);

export default function PieChart({ title, data, labels, customColors }) {
  const generateColors = (count) => {
    const colors = [];
    for (let i = 0; i < count; i++) {
      const hue = (i * 137.508) % 360; // Use golden angle approximation
      colors.push(`hsl(${hue}, 70%, 60%)`);
    }
    return colors;
  };

  const chartData = {
    labels: labels,
    datasets: [
      {
        data: data,
        backgroundColor: customColors || generateColors(data.length),
        borderWidth: 1,
      },
    ],
  };

  const options = {
    plugins: {
      title: {
        display: true,
        text: title,
        font: {
          size: 16,
        },
      },
    },
    maintainAspectRatio: false, // Ensure the chart adapts to the container size
  };

  return (
    <div
      className="flex justify-center items-center bg-white pt-16 pb-16 p-4 rounded-lg shadow"
      style={{
        width: "600px",
        height: "600px",
        marginTop: "80px",
        marginBottom: "80px",
        marginLeft: "auto",
        marginRight: "auto",
      }}
    >
      <Pie data={chartData} options={options} />
    </div>
  );
}
