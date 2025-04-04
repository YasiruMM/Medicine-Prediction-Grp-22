import { useState, useEffect } from 'react';
import { DiseaseCategories } from '../components/DiseaseCategories';
import { ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function FutureDemands() {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  console.log(selectedCategory)
  const [drugs, setDrugs] = useState<string[]>([]);
  const navigate = useNavigate();

  useEffect(() => {
    if (selectedCategory) {
      fetch(`http://127.0.0.1:5004/excessive-stocks/${selectedCategory}`)
        .then(response => response.json())
        .then(data => {
          if (data.excessive_stock_forecast) {
            const drugNames = data.excessive_stock_forecast.map((drug: any) => drug["Drug Name"]);
            setDrugs(drugNames);
          }
        })
        .catch(error => console.error('Error fetching drugs:', error));
    }
  }, [selectedCategory]);

  const handleRowClick = (drug: string) => {
    navigate('/drug-details', { state: { drug, category: selectedCategory } });
  };
  
  return (
    <div className="flex-1 p-8">
      <button
        onClick={() => navigate('/')}
        className="mb-6 flex items-center space-x-2 text-zinc-400 hover:text-white transition-colors duration-200"
      >
        <ArrowLeft className="h-5 w-5" />
        <span>Back to Home</span>
      </button>

      <h2 className="text-2xl font-bold text-center mb-8 animate-fade-in-up">
        Overstock Predictions
      </h2>

      {!selectedCategory ? (
        <div className="flex justify-center animate-fade-in-up">
          <DiseaseCategories onSelect={setSelectedCategory} />
        </div>
      ) : (
        <div className="max-w-4xl mx-auto bg-zinc-900/50 p-6 rounded-xl animate-fade-in-up">
          <h3 className="text-xl font-semibold mb-4 capitalize">
            {selectedCategory} Predictions
          </h3>
          <button
            onClick={() => setSelectedCategory(null)}
            className="text-sm text-blue-400 hover:text-blue-300 transition-colors"
          >
            ← Back to categories
          </button>

          {/* Table to display drugs */}
          <div className="mt-6 overflow-x-auto">
            <table className="min-w-full bg-zinc-800 border border-zinc-700 rounded">
              <thead className="bg-zinc-700">
                <tr>
                  <th className="px-4 py-2 text-left text-sm font-medium text-gray-200">
                    Drug Name
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-600">
                {drugs.map((drug, index) => (
                  <tr
                    key={index}
                    onClick={() => handleRowClick(drug)}
                    className="cursor-pointer hover:bg-zinc-700 transition-colors"
                  >
                    <td className="px-4 py-2 text-sm text-gray-300">
                      {drug}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
