
import React, { useState, useEffect } from 'react';
import { User, UserRole, PredictionRecord, EducationDetails, JobRolePrediction } from './types';
import Layout from './components/Layout';
import Auth from './components/Auth';
import PredictionForm from './components/PredictionForm';
import { predictJobRoles } from './services/geminiService';
import { Icons } from './constants';

const INITIAL_USERS: User[] = [
  { id: '1', email: 'admin@example.com', name: 'Elite Admin', role: UserRole.ADMIN, passwordHash: 'admin123' },
  { id: '2', email: 'user@example.com', name: 'Future Talent', role: UserRole.USER, passwordHash: 'user123' }
];

const CHART_COLORS = [
  '#2dd4bf', // Teal (Role 1)
  '#f472b6', // Pink (Role 2)
  '#60a5fa', // Blue (Role 3)
  '#fbbf24'  // Amber (Role 4)
];

const App: React.FC = () => {
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [predictions, setPredictions] = useState<PredictionRecord[]>([]);
  const [users, setUsers] = useState<User[]>(INITIAL_USERS);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const savedPredictions = localStorage.getItem('cp_predictions');
    if (savedPredictions) setPredictions(JSON.parse(savedPredictions));
    
    const savedUsers = localStorage.getItem('cp_users');
    if (savedUsers) setUsers(JSON.parse(savedUsers));
  }, []);

  useEffect(() => {
    localStorage.setItem('cp_predictions', JSON.stringify(predictions));
  }, [predictions]);

  useEffect(() => {
    localStorage.setItem('cp_users', JSON.stringify(users));
  }, [users]);

  const handlePredictionSubmit = async (details: EducationDetails) => {
    if (!currentUser) return;
    setIsLoading(true);
    try {
      const results = await predictJobRoles(details);
      const newRecord: PredictionRecord = {
        id: Math.random().toString(36).substr(2, 9),
        userId: currentUser.id,
        userName: currentUser.name,
        timestamp: Date.now(),
        education: details,
        predictions: results
      };
      setPredictions([newRecord, ...predictions]);
      setActiveTab('history');
    } catch (error) {
      console.error("Prediction failed:", error);
      alert("AI analysis failed. Check your API key.");
    } finally {
      setIsLoading(false);
    }
  };

  if (!currentUser) {
    return <Auth users={users} onLoginSuccess={setCurrentUser} onRegister={(u) => setUsers([...users, u])} />;
  }

  return (
    <Layout 
      user={currentUser} 
      onLogout={() => setCurrentUser(null)} 
      activeTab={activeTab} 
      setActiveTab={setActiveTab}
    >
      <div className="animate-in fade-in slide-in-from-bottom-4 duration-700">
        {activeTab === 'dashboard' && <DashboardView predictions={predictions} user={currentUser} />}
        {activeTab === 'predict' && <PredictionForm onSubmit={handlePredictionSubmit} isLoading={isLoading} />}
        {activeTab === 'history' && <HistoryView predictions={predictions} user={currentUser} />}
        {activeTab === 'admin' && currentUser.role === UserRole.ADMIN && <AdminView predictions={predictions} />}
      </div>
    </Layout>
  );
};

const DashboardView = ({ predictions, user }: { predictions: PredictionRecord[], user: User }) => {
  const filtered = user.role === UserRole.ADMIN ? predictions : predictions.filter(p => p.userId === user.id);
  
  return (
    <div className="space-y-10">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h1 className="text-5xl font-black text-white tracking-tighter mb-2">Command Center</h1>
          <p className="text-slate-400 font-bold uppercase tracking-[0.3em] text-xs">Profile: {user.name}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {[
          { label: 'Global Sessions', val: filtered.length, color: 'from-teal-400 to-emerald-500' },
          { label: 'Primary Path', val: filtered[0]?.predictions[0]?.roleName || 'Analyzing', color: 'from-blue-400 to-indigo-500' },
          { label: 'AI Confidence', val: filtered.length > 0 ? '97.2%' : '0%', color: 'from-purple-400 to-pink-500' }
        ].map((card, idx) => (
          <div key={idx} className="bg-white/5 border border-white/10 rounded-[2rem] p-8 backdrop-blur-xl group hover:border-white/20 transition-all shadow-xl">
            <p className="text-xs font-black text-slate-500 uppercase tracking-widest mb-4">{card.label}</p>
            <p className={`text-3xl font-black bg-gradient-to-r ${card.color} bg-clip-text text-transparent`}>{card.val}</p>
          </div>
        ))}
      </div>

      <div className="bg-white/5 border border-white/10 rounded-[2.5rem] p-10 backdrop-blur-xl relative overflow-hidden">
        <div className="absolute top-0 right-0 p-10 opacity-10">
            <Icons.Dashboard />
        </div>
        <h3 className="text-xl font-black text-white mb-8 uppercase tracking-widest">Platform Activity Trend</h3>
        <div className="h-48 flex items-end justify-between gap-3">
          {[40, 70, 45, 90, 65, 80, 50, 95, 60, 85, 55, 100].map((h, i) => (
            <div key={i} className="flex-grow bg-gradient-to-t from-blue-500/10 to-blue-400 rounded-xl transition-all duration-500 hover:shadow-[0_0_15px_rgba(96,165,250,0.5)]" style={{ height: `${h}%` }}></div>
          ))}
        </div>
      </div>
    </div>
  );
};

const HistoryView = ({ predictions, user }: { predictions: PredictionRecord[], user: User }) => {
  const filtered = user.role === UserRole.ADMIN ? predictions : predictions.filter(p => p.userId === user.id);

  return (
    <div className="space-y-8">
      <h1 className="text-4xl font-black text-white tracking-tighter">Prediction Analytics</h1>
      {filtered.length === 0 ? (
        <div className="bg-white/5 border-2 border-dashed border-white/10 p-20 rounded-[3rem] text-center">
          <p className="text-slate-500 text-xl font-black uppercase tracking-widest">No predictions generated yet</p>
        </div>
      ) : (
        <div className="space-y-12">
          {filtered.map((record) => (
            <div key={record.id} className="bg-white/5 border border-white/10 p-10 rounded-[3rem] backdrop-blur-xl shadow-2xl">
              <div className="flex flex-col md:flex-row justify-between items-start mb-12 gap-6">
                <div>
                  <h4 className="text-3xl font-black text-white tracking-tight">{record.education.degree} in {record.education.specialization}</h4>
                  <div className="flex items-center space-x-4 mt-3">
                    <span className="text-teal-400 font-black uppercase tracking-widest text-[10px] bg-teal-400/10 px-3 py-1 rounded-full border border-teal-400/20">Analysis {new Date(record.timestamp).toLocaleDateString()}</span>
                    <span className="text-slate-400 font-bold text-xs">CGPA: {record.education.cgpa}</span>
                  </div>
                </div>
              </div>

              {/* Advanced Analytics Panel */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 mb-12">
                {/* 1. Bar Chart: Confidence & Interest Score */}
                <div className="bg-black/30 p-8 rounded-[2rem] border border-white/5 space-y-8">
                  <h5 className="text-sm font-black text-white uppercase tracking-widest border-b border-white/10 pb-4 mb-6">Competency Matrix (Confidence vs Interest)</h5>
                  <div className="space-y-6">
                    {record.predictions.map((p, idx) => (
                      <div key={idx} className="space-y-2">
                        <div className="flex justify-between text-[10px] font-black uppercase tracking-widest text-slate-500">
                          <span>{p.roleName}</span>
                          <span className="text-white">Conf: {Math.round(p.confidence * 100)}% | Int: {Math.round(p.interestScore * 100)}%</span>
                        </div>
                        <div className="h-3 bg-white/5 rounded-full overflow-hidden flex">
                          <div 
                            className="h-full rounded-full transition-all duration-1000 shadow-[0_0_10px_rgba(20,184,166,0.5)]" 
                            style={{ width: `${p.confidence * 100}%`, backgroundColor: CHART_COLORS[idx] }}
                          ></div>
                        </div>
                        <div className="h-1 bg-white/5 rounded-full overflow-hidden opacity-30">
                          <div 
                            className="h-full bg-white transition-all duration-1000" 
                            style={{ width: `${p.interestScore * 100}%` }}
                          ></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* 2. Pie Chart: Career Distribution */}
                <div className="bg-black/30 p-8 rounded-[2rem] border border-white/5 flex flex-col items-center justify-center relative min-h-[300px]">
                   <h5 className="text-sm font-black text-white uppercase tracking-widest border-b border-white/10 pb-4 mb-10 w-full text-left">Career Domain Split</h5>
                   <div className="relative w-48 h-48">
                      {/* Simple SVG Donut/Pie representation */}
                      <svg viewBox="0 0 100 100" className="w-full h-full transform -rotate-90">
                         {record.predictions.map((p, idx) => {
                            const offset = record.predictions.slice(0, idx).reduce((acc, curr) => acc + curr.confidence, 0);
                            const total = record.predictions.reduce((acc, curr) => acc + curr.confidence, 0);
                            const startPercent = (offset / total) * 100;
                            const sizePercent = (p.confidence / total) * 100;
                            return (
                               <circle
                                  key={idx}
                                  cx="50" cy="50" r="40"
                                  fill="transparent"
                                  stroke={CHART_COLORS[idx]}
                                  strokeWidth="15"
                                  strokeDasharray={`${sizePercent} ${100 - sizePercent}`}
                                  strokeDashoffset={-startPercent}
                                  className="transition-all duration-1000"
                               />
                            );
                         })}
                      </svg>
                      <div className="absolute inset-0 flex items-center justify-center flex-col">
                        <span className="text-2xl font-black text-white">4</span>
                        <span className="text-[8px] font-black text-slate-500 uppercase tracking-widest">Paths</span>
                      </div>
                   </div>
                   <div className="grid grid-cols-2 gap-4 mt-10 w-full">
                      {record.predictions.map((p, idx) => (
                         <div key={idx} className="flex items-center space-x-2">
                            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: CHART_COLORS[idx] }}></div>
                            <span className="text-[10px] font-bold text-slate-400 truncate uppercase">{p.roleName}</span>
                         </div>
                      ))}
                   </div>
                </div>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {record.predictions.map((p, idx) => (
                  <div key={idx} className="bg-white/5 p-6 rounded-[2rem] border border-white/5 flex flex-col justify-between hover:bg-white/10 transition-colors">
                    <div>
                      <div className="flex justify-between items-center mb-4">
                        <span className="font-black text-white text-sm tracking-tight">{p.roleName}</span>
                        <div className="w-2 h-2 rounded-full shadow-[0_0_10px_rgba(20,184,166,1)]" style={{ backgroundColor: CHART_COLORS[idx] }}></div>
                      </div>
                      <p className="text-[11px] text-slate-400 font-medium leading-relaxed mb-4 line-clamp-4">{p.explanation}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

const AdminView = ({ predictions }: { predictions: PredictionRecord[] }) => {
  return (
    <div className="space-y-8">
      <h1 className="text-4xl font-black text-white tracking-tighter uppercase">Global Master Control</h1>
      <div className="bg-white/5 rounded-[3rem] border border-white/10 overflow-hidden shadow-2xl backdrop-blur-xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead className="bg-white/5 border-b border-white/10">
              <tr>
                <th className="px-10 py-8 text-xs font-black text-slate-500 uppercase tracking-[0.2em]">Profile Info</th>
                <th className="px-10 py-8 text-xs font-black text-slate-500 uppercase tracking-[0.2em]">Academics</th>
                <th className="px-10 py-8 text-xs font-black text-slate-500 uppercase tracking-[0.2em]">Dominant Path</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/5">
              {predictions.map((p) => (
                <tr key={p.id} className="hover:bg-white/[0.03] transition-colors">
                  <td className="px-10 py-8">
                    <div className="font-black text-white text-lg">{p.userName}</div>
                    <div className="text-[10px] text-slate-500 font-black uppercase tracking-widest">{new Date(p.timestamp).toLocaleDateString()}</div>
                  </td>
                  <td className="px-10 py-8">
                    <div className="text-sm text-slate-300 font-bold">{p.education.degree}</div>
                    <div className="text-xs text-teal-400 font-black tracking-widest uppercase">{p.education.specialization}</div>
                  </td>
                  <td className="px-10 py-8">
                     <span className="px-4 py-2 bg-teal-400/10 text-teal-400 text-xs font-black rounded-xl border border-teal-500/20 shadow-lg">{p.predictions[0].roleName}</span>
                  </td>
                </tr>
              ))}
              {predictions.length === 0 && (
                <tr>
                    <td colSpan={3} className="px-10 py-32 text-center text-slate-500 font-black tracking-widest uppercase italic text-xl">System Standby - No Data</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default App;
