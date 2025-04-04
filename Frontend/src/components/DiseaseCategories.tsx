import { Heart, Droplet, Activity } from 'lucide-react';

interface DiseaseCategoryProps {
  onSelect: (category: string) => void;
}

export function DiseaseCategories({ onSelect }: DiseaseCategoryProps) {
  const categories = [
    { name: 'Cardiovascular', icon: Heart, color: 'red' },
    { name: 'Diabetes', icon: Droplet, color: 'blue' },
    { name: 'Cholesterol', icon: Activity, color: 'yellow' }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-4xl">
      {categories.map((category) => (
        <button
          key={category.name}
          onClick={() => {
            console.log(`Category selected: ${category.name.toLowerCase()}`); // Log selected category
            onSelect(category.name.toLowerCase());
          }}
          className="group relative overflow-hidden backdrop-blur-sm bg-zinc-900/50 p-6 rounded-xl border border-zinc-800/50 
                     transition-all duration-300 hover:scale-105 hover:bg-zinc-800/50"
        >
          <div className="relative z-10 flex flex-col items-center space-y-4">
            <div className="relative">
              <div className={`absolute inset-0 bg-${category.color}-500 blur-xl opacity-0 group-hover:opacity-20 transition-opacity duration-300`}></div>
              <category.icon className={`h-10 w-10 text-${category.color}-500 transition-transform duration-300 group-hover:scale-110`} />
            </div>
            <span className="text-lg font-medium text-zinc-100">{category.name}</span>
          </div>
        </button>
      ))}
    </div>
  );
}
