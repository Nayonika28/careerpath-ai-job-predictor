
import React, { useState } from 'react';
import { Icons } from '../constants';
import { User, UserRole } from '../types';

interface AuthProps {
  onLoginSuccess: (user: User) => void;
  users: User[];
  onRegister: (newUser: User) => void;
}

const Auth: React.FC<AuthProps> = ({ onLoginSuccess, users, onRegister }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (isLogin) {
      const user = users.find(u => u.email === email && u.passwordHash === password);
      if (user) {
        onLoginSuccess(user);
      } else {
        setError('Invalid credentials.');
      }
    } else {
      if (users.some(u => u.email === email)) {
        setError('Email already registered.');
        return;
      }
      const newUser: User = {
        id: Math.random().toString(36).substr(2, 9),
        email,
        name,
        role: email.includes('admin') ? UserRole.ADMIN : UserRole.USER,
        passwordHash: password
      };
      onRegister(newUser);
      onLoginSuccess(newUser);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#020617] relative overflow-hidden p-6">
      {/* Neon Blobs Background */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-teal-500/20 blur-[120px] rounded-full"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-600/20 blur-[120px] rounded-full"></div>

      <div className="w-full max-w-md bg-white/5 backdrop-blur-2xl border border-white/10 rounded-[2.5rem] p-8 md:p-12 shadow-2xl relative z-10 transition-all duration-500 hover:border-white/20">
        <div className="flex flex-col items-center mb-10">
          <div className="w-20 h-20 bg-gradient-to-br from-teal-400 to-blue-500 rounded-2xl shadow-[0_0_25px_rgba(20,184,166,0.4)] flex items-center justify-center text-white mb-6">
            <Icons.Education />
          </div>
          <h2 className="text-4xl font-black text-white tracking-tighter mb-2">
            {isLogin ? 'Welcome' : 'Join Us'}
          </h2>
          <p className="text-slate-400 text-center font-medium">
            Elite Career Prediction with AI Grounding
          </p>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-500/10 border border-red-500/20 text-red-400 text-sm font-bold rounded-2xl text-center">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {!isLogin && (
            <div className="space-y-2">
              <label className="text-xs font-bold text-teal-400 uppercase tracking-widest ml-1">Full Name</label>
              <input
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full bg-slate-900/50 border border-white/10 px-5 py-4 rounded-2xl text-white font-medium focus:ring-2 focus:ring-teal-500 focus:border-transparent outline-none transition-all placeholder:text-slate-600"
                placeholder="Ex: Elon Musk"
              />
            </div>
          )}
          <div className="space-y-2">
            <label className="text-xs font-bold text-teal-400 uppercase tracking-widest ml-1">Email Address</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-slate-900/50 border border-white/10 px-5 py-4 rounded-2xl text-white font-medium focus:ring-2 focus:ring-teal-500 focus:border-transparent outline-none transition-all placeholder:text-slate-600"
              placeholder="name@future.ai"
            />
          </div>
          <div className="space-y-2">
            <label className="text-xs font-bold text-teal-400 uppercase tracking-widest ml-1">Access Key</label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full bg-slate-900/50 border border-white/10 px-5 py-4 rounded-2xl text-white font-medium focus:ring-2 focus:ring-teal-500 focus:border-transparent outline-none transition-all placeholder:text-slate-600"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-gradient-to-r from-teal-500 to-blue-600 hover:from-teal-400 hover:to-blue-500 text-white font-black py-4 rounded-2xl shadow-[0_0_20px_rgba(20,184,166,0.3)] transition-all active:scale-[0.97] text-lg uppercase tracking-wider"
          >
            {isLogin ? 'Sign In' : 'Sign Up'}
          </button>
        </form>

        <div className="mt-10 text-center">
          <p className="text-slate-500 font-bold">
            {isLogin ? "New here?" : "Returning member?"}
            <button
              onClick={() => setIsLogin(!isLogin)}
              className="ml-2 text-teal-400 hover:text-teal-300 transition-colors underline-offset-4 hover:underline"
            >
              {isLogin ? 'Create Account' : 'Back to Login'}
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Auth;
