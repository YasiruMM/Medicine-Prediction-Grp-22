import { useLocation, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Line,
} from 'recharts';
import { ArrowLeft } from 'lucide-react';

interface ChartEntry {
  name: string;
  value: number;
}

interface LocationState {
  drug: string;
  category: string;
}

export default function DrugDetails() {
  const location = useLocation();
  const navigate = useNavigate();
  const { drug, category } = location.state as LocationState;

  const [forecastData, setForecastData] = useState<ChartEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`http://localhost:5004/excessive-stocks/${category.toLowerCase()}`)
      .then((res) => res.json())
      .then((data) => {
        const forecast = data.excessive_stock_forecast.find(
          (item: { [key: string]: string }) =>
            item["Drug Name"].toLowerCase().trim() === drug.toLowerCase().trim()
        );

        if (forecast) {
          const chartData: ChartEntry[] = Object.entries(forecast)
            .filter(([key]) => key.startsWith("Month"))
            .map(([month, value]) => ({
              name: month,
              value: parseFloat((value as string).replace('%', '')),
            }));

          setForecastData(chartData);
        } else {
          setForecastData([]);
        }

        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching drug forecast:", err);
        setForecastData([]);
        setLoading(false);
      });
  }, [drug]);

  const handleGoBack = () => {
    navigate('/overstock', { state: { category } });
  };

  return (
    <div className="flex flex-col items-center justify-center p-8 text-white w-full">
      <button
        onClick={handleGoBack}
        className="mb-6 flex items-center space-x-2 text-zinc-400 hover:text-white transition-colors duration-200 self-start"
      >
        <ArrowLeft className="h-5 w-5" />
        <span>Back to Drug List</span>
      </button>
      <h2 className="text-2xl font-bold mb-4 text-center">{drug} Overstock Forecast</h2>

      {loading ? (
        <p>Loading...</p>
      ) : forecastData.length > 0 ? (
        <ResponsiveContainer width="90%" height={400}>
          <BarChart data={forecastData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis tickFormatter={(value) => `${value}%`} />
            <Tooltip formatter={(value: number) => `${value}%`} />
            <Bar dataKey="value" fill="#8884d8" />

            {/* Add Gradient Definition */}
            <defs>
              <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="red" stopOpacity={0.8} />
                <stop offset="100%" stopColor="blue" stopOpacity={0.8} />
              </linearGradient>
            </defs>

            {/* Gradient Line */}
            <Line
              type="monotone"
              data={forecastData}
              dataKey="value"
              stroke="url(#lineGradient)" // Apply the gradient
              strokeWidth={3}
              dot={false} // Disable dots
              activeDot={{ r: 8 }}
              strokeDasharray="5 5"
            />
          </BarChart>
        </ResponsiveContainer>
      ) : (
        <p>No excessive stock forecast available for this drug.</p>
      )}
    </div>
  );
}
