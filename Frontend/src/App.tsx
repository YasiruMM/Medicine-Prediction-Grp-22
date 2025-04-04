import { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Activity } from 'lucide-react';
import { onAuthStateChanged } from 'firebase/auth';
import { auth } from './firebase'; // ✅ import your Firebase auth

// Pages
import HomePage from './pages/HomePage';
import FutureDemands from './pages/FutureDemands';
import StorageRisk from './pages/StorageRisk';
import Overstock from './pages/Overstock';
import AboutDrugs from './pages/AboutDrugs';
import SignIn from './pages/SignIn';
import NotFound from './pages/NotFound';
import DrugDetails from './pages/DrugDetails';
import DrugDemandChart from './pages/DrugDemandChart';

function App() {
  const [isSignedIn, setIsSignedIn] = useState<boolean | null>(null); // null = loading state

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setIsSignedIn(!!user); // true if user exists
    });

    return () => unsubscribe(); // cleanup listener
  }, []);

  if (isSignedIn === null) {
    // Loading state while checking auth
    return (
      <div className="flex items-center justify-center min-h-screen bg-black text-white">
        <p>Checking authentication...</p>
      </div>
    );
  }

  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-black text-white font-sans">
        <header className="backdrop-blur-sm bg-zinc-900/90 sticky top-0 z-50 p-6 border-b border-zinc-800/50">
          <div className="max-w-7xl mx-auto flex items-center justify-between">
            <div className="flex items-center space-x-4 animate-fade-in">
              <div className="relative">
                <div className="absolute inset-0 bg-green-500 blur-xl opacity-20 animate-pulse"></div>
                <Activity className="h-10 w-10 text-blue-500 relative" />
              </div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-500 via-purple-500 to-blue-500 bg-clip-text text-transparent bg-300% animate-gradient">
                MediTrack
              </h1>
            </div>
          </div>
        </header>

        <Routes>
          {isSignedIn ? (
            <>
              <Route path="/" element={<HomePage />} />
              <Route path="/future-demands" element={<FutureDemands />} />
              <Route path="/storage-risk" element={<StorageRisk />} />
              <Route path="/overstock" element={<Overstock />} />
              <Route path="/about-drugs" element={<AboutDrugs />} />
              <Route path="/drug-details" element={<DrugDetails />} />
              <Route path="/drug-demand-chart" element={<DrugDemandChart />} />
              <Route path="*" element={<NotFound />} />
            </>
          ) : (
            <>
              <Route path="*" element={<SignIn />} />
            </>
          )}
        </Routes>
      </div>
    </Router>
  );
}

export default App;