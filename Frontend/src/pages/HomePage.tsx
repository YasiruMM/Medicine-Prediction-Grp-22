import {
  Activity,
  AlertCircleIcon,
  FlaskRound as Flask,
  LineChart,
  PlusCircle,
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';

function HomePage() {
  const navigate = useNavigate();

  const menuItems = [
    {
      icon: LineChart,
      title: 'Future Demands',
      desc: 'Predict pharmaceutical needs',
      color: 'blue',
      path: '/future-demands',
    },
    {
      icon: AlertCircleIcon,
      title: 'Storage Risk Detection',
      desc: 'Monitor storage conditions',
      color: 'purple',
      path: '/storage-risk',
    },
    {
      icon: PlusCircle,
      title: 'Overstock Predictions',
      desc: 'Optimize inventory levels',
      color: 'green',
      path: '/overstock',
    },
    {
      icon: Flask,
      title: 'About Drugs',
      desc: 'Comprehensive database',
      color: 'pink',
      path: '/about-drugs',
    },
  ];

  return (
    <>
      <motion.h2
        className="text-4xl text-zinc-400 mt-10 text-center font-semibold"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        Homepage
      </motion.h2>

      <main className="flex-grow flex justify-center items-center p-8">
        <motion.div
          className="grid grid-cols-1 sm:grid-cols-2 gap-8 max-w-4xl w-full"
          initial="hidden"
          animate="visible"
          variants={{
            hidden: {},
            visible: {
              transition: {
                staggerChildren: 0.1,
              },
            },
          }}
        >
          {menuItems.map((item) => {
            const colorClass = `text-${item.color}-500`;
            const glowClass = `bg-${item.color}-500`;

            return (
              <motion.button
                key={item.title}
                onClick={() => navigate(item.path)}
                className={`group relative overflow-hidden backdrop-blur-md bg-zinc-900/50 p-8 rounded-2xl border border-zinc-800/50
                  transition-all duration-500 hover:scale-105 shadow-md`}
                variants={{
                  hidden: { opacity: 0, y: 30 },
                  visible: { opacity: 1, y: 0 },
                }}
              >
                {/* Glowing aura */}
                <div
                  className={`absolute inset-0 z-0 opacity-0 group-hover:opacity-20 transition-opacity duration-500 blur-3xl 
                              ${glowClass} rounded-xl`}
                />

                {/* Card content */}
                <div className="relative z-10 flex flex-col items-center space-y-4">
                  <item.icon
                    className={`h-12 w-12 ${colorClass} transition-transform duration-500 group-hover:scale-110`}
                  />
                  <div className="text-center space-y-2">
                    <span className="block text-lg font-semibold text-zinc-100">
                      {item.title}
                    </span>
                    <span className="block text-sm text-zinc-400 opacity-0 group-hover:opacity-100 transition-opacity duration-500">
                      {item.desc}
                    </span>
                  </div>
                </div>
              </motion.button>
            );
          })}
        </motion.div>
      </main>
    </>
  );
}

export default HomePage;
