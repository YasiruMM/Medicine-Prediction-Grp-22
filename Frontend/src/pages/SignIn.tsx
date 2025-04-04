import React, { useState } from 'react';
import { Lock } from 'lucide-react';
import { signInWithEmailAndPassword } from 'firebase/auth';
import { auth } from '../firebase'; // your firebase config
import { useNavigate } from 'react-router-dom';

const SignIn: React.FC = () => {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [error, setError] = useState<string>('');
  const navigate = useNavigate();

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
      await signInWithEmailAndPassword(auth, email, password);
      setError('');
      alert('Login successful!');
      navigate('/'); // or "/dashboard"
    } catch (err: any) {
      console.error('❌ Firebase Login Error:', err.code, err.message);
      setError(`Login failed: ${err.message}`);
    }
  };

  return (
    <>
      <h2 className="text-5xl text-zinc-400 mt-8 text-center font-medium animate-fade-in-up">
        Sign In
      </h2>

      <main className="flex-grow flex justify-center items-center p-8">
        <div
          className={`
            group relative overflow-hidden backdrop-blur-sm bg-zinc-900/50
            p-8 rounded-2xl border border-zinc-800/50
            transition-all duration-500 hover:scale-105 hover:bg-zinc-800/50
            animate-fade-in-up
          `}
          style={{ animationDelay: '100ms' }}
        >
          <form onSubmit={handleSubmit} className="flex flex-col space-y-6 relative z-10 w-80">
            <div className="flex justify-center">
              <div className="relative">
                <div className="absolute inset-0 bg-purple-500 blur-xl opacity-0 group-hover:opacity-20 transition-opacity duration-500"></div>
                <Lock className="h-12 w-12 text-purple-500 transition-all duration-500 group-hover:scale-110 group-hover:rotate-3" />
              </div>
            </div>

            <div className="flex flex-col">
              <label className="text-zinc-400 mb-1" htmlFor="email">
                Email
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className={`
                  bg-zinc-900 p-2 rounded-md border border-zinc-700
                  focus:outline-none focus:ring-2 focus:ring-purple-600
                  text-zinc-100
                `}
                placeholder="Enter your email"
              />
            </div>

            <div className="flex flex-col">
              <label className="text-zinc-400 mb-1" htmlFor="password">
                Password
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className={`
                  bg-zinc-900 p-2 rounded-md border border-zinc-700
                  focus:outline-none focus:ring-2 focus:ring-purple-600
                  text-zinc-100
                `}
                placeholder="Enter your password"
              />
            </div>

            {error && <p className="text-red-500 text-center">{error}</p>}

            <button
              type="submit"
              className={`
                bg-purple-600 text-white py-2 px-4 rounded-md
                hover:bg-purple-700 transition-colors
              `}
            >
              Sign In
            </button>
          </form>

          <div
            className={`
              absolute inset-0 opacity-0 group-hover:opacity-10
              transition-opacity duration-500
              bg-gradient-to-br from-purple-500 via-transparent to-purple-600
            `}
          />
        </div>
      </main>
    </>
  );
};

export default SignIn;
