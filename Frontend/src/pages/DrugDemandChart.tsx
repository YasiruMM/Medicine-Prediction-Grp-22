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

export default function DrugDemandChart() {
  const location = useLocation();
  const navigate = useNavigate();
  const { drug, category } = location.state as LocationState;

  const [forecastData, setForecastData] = useState<ChartEntry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`http://127.0.0.1:5003/future-demand-predict/${encodeURIComponent(drug)}`)
      .then((res) => res.json())
      .then((data) => {
        const chartData: ChartEntry[] = data.forecast.map((item: any) => ({
          name: item.name,
          value: item.value,
        }));

        setForecastData(chartData);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching drug forecast:", err);
        setForecastData([]);
        setLoading(false);
      });
  }, [drug]);

  const handleGoBack = () => {
    navigate('/future-demands', { state: { category } }); // optional: can restore category state
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

      <h2 className="text-2xl font-bold mb-4 text-center">
        {drug} Demand Forecast
      </h2>

      {loading ? (
        <p>Loading...</p>
      ) : forecastData.length > 0 ? (
        <ResponsiveContainer width="90%" height={400}>
          <BarChart data={forecastData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis tickFormatter={(value) => `${value}`} />
            <Tooltip formatter={(value: number) => `${value}`} />
            <Bar dataKey="value" fill="#4ade80" />
          </BarChart>
        </ResponsiveContainer>
      ) : (
        <p>No forecast data available for this drug.</p>
      )}
    </div>
  );
}
