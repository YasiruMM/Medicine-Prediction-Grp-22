import { ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function AboutDrugs() {
  const navigate = useNavigate();

  return (
    <div className="flex-1 p-8">
      <button
        onClick={() => navigate('/')}
        className="mb-6 flex items-center space-x-2 text-zinc-400 hover:text-white transition-colors duration-200"
      >
        <ArrowLeft className="h-5 w-5" />
        <span>Back to Home</span>
      </button>

      <h2 className="text-2xl font-bold text-center mb-8 animate-fade-in-up">Drug Information Database</h2>
    </div>
  );
}