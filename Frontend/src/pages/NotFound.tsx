import { AlertTriangle } from 'lucide-react';
import { Link } from 'react-router-dom';

const NotFound = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br  p-4">
      <AlertTriangle className="w-24 h-24 text-red-500 animate-bounce" />
      <h1 className="mt-4 text-6xl font-extrabold text-white transition-opacity duration-1000">
        404
      </h1>
      <p className="mt-2 text-2xl text-gray-300 animate-pulse">
        Oops! Page Not Found
      </p>
      <Link
        to="/"
        className="mt-6 inline-flex items-center px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-md shadow transition transform hover:scale-105"
      >
        Go to Home
      </Link>
    </div>
  );
};

export default NotFound;
