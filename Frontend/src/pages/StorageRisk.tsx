import { useState, useEffect } from "react";
import { ArrowLeft } from "lucide-react";
import { useNavigate } from "react-router-dom";
import {
  ComposedChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer
} from "recharts";
import { DiseaseCategories } from "../components/DiseaseCategories"; // Assuming you already have this component

const API_BASE_URL = "http://127.0.0.1:5002";  // The base URL for your Flask app

export default function StorageRisk() {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);  // Added type for selectedCategory
  const [drugNames, setDrugNames] = useState<string[]>([]);  // Stores the list of drug names
  const [selectedDrug, setSelectedDrug] = useState<string | null>(null);
  const [lossQuantity, setLossQuantity] = useState<number | null>(null);
  const [predictions, setPredictions] = useState<any>(null);
  const [bufferStock, setBufferStock] = useState<number | null>(null); // Added to store buffer stock
  const [errorMessage, setErrorMessage] = useState<string | null>(null); // Added error message state
  const navigate = useNavigate();

  // Fetch drug names when a category is selected
  useEffect(() => {
    if (selectedCategory) {
      console.log("Fetching drug names for category:", selectedCategory);  // Log before making the fetch request
      fetch(`${API_BASE_URL}/get-drug-names?category=${selectedCategory.toLowerCase()}`, {
        method: "GET",
        headers: { "Accept": "application/json" }
      })
        .then(res => res.json())
        .then(data => {
          if (data && data.drug_names) {
            setDrugNames(data.drug_names);
            console.log("Fetched Drug Names:", data.drug_names); // Log the drug names array
          } else {
            console.error("Invalid response format:", data);
          }
        })
        .catch(error => {
          console.error("Error fetching drug names:", error);
        });
    }
  }, [selectedCategory]);

  // Updated category select handler with type definition
  const handleCategorySelect = (category: string) => {
    setSelectedCategory(category);
    setErrorMessage(null);  // Reset error message when a new category is selected
  };

  const handlePredict = () => {
    if (!selectedDrug || !lossQuantity) {
      alert("Please select a drug and enter the loss quantity.");
      return;
    }

    // Reset error message before making the request
    setErrorMessage(null);

    // Make the API request to fetch predictions
    fetch(`${API_BASE_URL}/predict-oos`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ drug_name: selectedDrug, loss_quantity: lossQuantity })
    })
      .then(res => res.json())
      .then(data => {
        if (data.error) {
          setErrorMessage(data.error);  // Show error message if drug is not found or another error occurs
          setPredictions(null);  // Clear any existing predictions
          setBufferStock(null);   // Clear buffer stock
        } else {
          setPredictions(data);
          setBufferStock(data.buffer_stock); // Store buffer stock value from API response
        }
      })
      .catch(error => {
        console.error("Error fetching predictions:", error);
        setErrorMessage("There was an issue with the prediction. Please try again.");
      });
  };

  // Safely prepare data for the chart
  const chartData = predictions?.original_predictions
    ? predictions.original_predictions.map((value: number, index: number) => ({
        month: `Month ${index + 1}`,
        original: value,
        adjusted: predictions.adjusted_predictions?.[index] || 0,
        risk_quantity: predictions.shortage_risk_levels?.[index] || 0
      }))
    : [];

  return (
    <div className="flex-1 p-8">
      <button
        onClick={() => navigate("/")}
        className="mb-6 flex items-center space-x-2 text-zinc-400 hover:text-white transition-colors duration-200"
      >
        <ArrowLeft className="h-5 w-5" />
        <span>Back to Home</span>
      </button>

      <h2 className="text-2xl font-bold text-center mb-8 animate-fade-in-up">
        Out-of-Stock Risk Detection
      </h2>

      {/* Step 1: Select Disease Category */}
      {!selectedCategory ? (
        <div className="flex justify-center animate-fade-in-up">
          <DiseaseCategories onSelect={handleCategorySelect} />
        </div>
      ) : !selectedDrug ? (
        <div className="flex flex-col items-center animate-fade-in-up">
          <button
            onClick={() => setSelectedCategory(null)}
            className="text-sm text-blue-400 mb-4 hover:text-blue-300"
          >
            ← Back to category selection
          </button>
          <label className="block text-white text-lg mb-2">Select a Drug:</label>
          <select
            className="p-2 rounded bg-zinc-800 text-white"
            onChange={(e) => setSelectedDrug(e.target.value)}
          >
            <option value="">-- Select a Drug --</option>
            {drugNames.map((drug) => (
              <option key={drug} value={drug}>
                {drug}
              </option>
            ))}
          </select>
        </div>
      ) : (
        <div className="max-w-4xl mx-auto bg-zinc-900/50 p-6 rounded-xl animate-fade-in-up">
          <h3 className="text-xl font-semibold mb-4 capitalize">Analyze {selectedDrug} Risk</h3>
          <button
            onClick={() => setSelectedDrug(null)}
            className="text-sm text-blue-400 hover:text-blue-300 transition-colors"
          >
            ← Back to drug selection
          </button>

          {/* Step 2: Enter Loss Quantity */}
          <div className="mt-4">
            <label className="block text-white text-lg mb-2">Enter Loss Quantity:</label>
            <input
              type="number"
              className="p-2 rounded bg-zinc-800 text-white w-full"
              placeholder="Enter loss quantity"
              value={lossQuantity || ""}
              onChange={(e) => setLossQuantity(Number(e.target.value))}
            />
            <button
              onClick={handlePredict}
              className="mt-4 bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
            >
              Predict Shortage Risk
            </button>
          </div>
        </div>
      )}

      {/* Step 3: Display Predictions */}
      {errorMessage ? (
        <div className="mt-8 bg-red-500/50 p-6 rounded-xl">
          <h3 className="text-xl font-semibold text-center text-white">{errorMessage}</h3>
        </div>
      ) : (
        predictions && (
          <div className="mt-8 bg-zinc-900/50 p-6 rounded-xl">
            <h3 className="text-xl font-semibold mb-4">Shortage Risk Analysis {selectedDrug}</h3>

            {/* Display Buffer Stock before the chart */}
            {bufferStock !== null && (
              <p className="text-white text-lg mb-4">
                <strong>Buffer Stock:</strong> {bufferStock}
              </p>
            )}

            {/* Display Risk Levels */}
            <ul className="list-disc ml-6 text-white">
              {predictions.shortage_risk_levels?.map((value: number, index: number) => (
                <li key={index}>
                  Month {index + 1}: {value > 0 ? `${value} units at risk` : "No Risk"}
                </li>
              ))}
            </ul>

            <div className="mt-6">
              <h3 className="text-lg font-semibold text-center text-white mb-4">
                Shortage Risk Over 6 Months
              </h3>
              <ResponsiveContainer width="100%" height={300}>
                <ComposedChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 10 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" label={{ value: "Months", position: "insideBottom", offset: -5 }} />
                  <YAxis label={{ value: "Quantity", angle: -90, position: "insideLeft" }} />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="original" stroke="#8884d8" strokeWidth={2} name="Original Prediction" />
                  <Line type="monotone" dataKey="adjusted" stroke="#82ca9d" strokeWidth={2} name="Adjusted Prediction" />
                  <Line type="monotone" dataKey="risk_quantity" stroke="#ff7300" strokeWidth={2} name="Shortage Risk" />
                </ComposedChart>
              </ResponsiveContainer>
            </div>
          </div>
        )
      )}
    </div>
  );
}
