
import React from 'react';
import { Icons } from '../constants';
import { User, UserRole } from '../types';

interface LayoutProps {
  children: React.ReactNode;
  user: User | null;
  onLogout: () => void;
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

const Layout: React.FC<LayoutProps> = ({ children, user, onLogout, activeTab, setActiveTab }) => {
  if (!user) return <div className="min-h-screen bg-[#020617]">{children}</div>;

  const NavItem = ({ id, icon: Icon, label }: { id: string, icon: any, label: string }) => (
    <button
      onClick={() => setActiveTab(id)}
      className={`w-full flex items-center space-x-4 px-6 py-4 rounded-2xl transition-all group ${
        activeTab === id 
          ? 'bg-teal-500 text-white shadow-[0_0_20px_rgba(20,184,166,0.3)]' 
          : 'hover:bg-white/5 text-slate-500 hover:text-slate-200'
      }`}
    >
      <div className={`${activeTab === id ? 'text-white' : 'text-slate-500 group-hover:text-teal-400'}`}>
        <Icon />
      </div>
      <span className="font-black text-sm uppercase tracking-widest">{label}</span>
    </button>
  );

  return (
    <div className="min-h-screen flex flex-col md:flex-row bg-[#020617] font-['Inter'] selection:bg-teal-500/30">
      {/* Sidebar - Desktop */}
      <aside className="w-80 bg-slate-950/50 backdrop-blur-3xl border-r border-white/5 flex-shrink-0 flex flex-col hidden md:flex">
        <div className="p-10 border-b border-white/5 flex items-center space-x-4">
          <div className="p-3 bg-gradient-to-br from-teal-400 to-blue-500 rounded-2xl shadow-lg shadow-teal-500/20 text-white">
            <Icons.Education />
          </div>
          <div>
            <h1 className="text-xl font-black text-white tracking-tighter leading-tight">CAREER<br/>PATH AI</h1>
          </div>
        </div>
        
        <nav className="flex-grow p-6 space-y-3">
          <NavItem id="dashboard" icon={Icons.Dashboard} label="Dashboard" />
          <NavItem id="predict" icon={Icons.Job} label="AI Predictor" />
          <NavItem id="history" icon={Icons.History} label="Intelligence" />
          {user.role === UserRole.ADMIN && (
            <NavItem id="admin" icon={Icons.Admin} label="Admin Hub" />
          )}
        </nav>

        <div className="p-8 border-t border-white/5 space-y-6">
          <div className="flex items-center space-x-4 p-4 bg-white/5 rounded-3xl border border-white/5">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-slate-700 to-slate-800 flex items-center justify-center font-black text-teal-400 uppercase shadow-inner">
              {user.name.charAt(0)}
            </div>
            <div className="overflow-hidden">
              <p className="text-sm font-black text-white truncate uppercase tracking-tight">{user.name}</p>
              <p className="text-[10px] text-slate-500 font-bold truncate uppercase tracking-widest">{user.role}</p>
            </div>
          </div>
          <button
            onClick={onLogout}
            className="w-full flex items-center justify-center space-x-3 px-6 py-4 bg-red-500/10 hover:bg-red-500/20 text-red-400 rounded-2xl border border-red-500/20 transition-all font-black text-xs uppercase tracking-widest"
          >
            <Icons.Logout />
            <span>Terminate Session</span>
          </button>
        </div>
      </aside>

      {/* Header - Mobile */}
      <header className="bg-slate-950/80 backdrop-blur-2xl border-b border-white/5 px-6 py-5 flex justify-between items-center md:hidden sticky top-0 z-50">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-teal-500 rounded-xl text-white shadow-lg shadow-teal-500/30">
            <Icons.Education />
          </div>
          <h1 className="text-lg font-black text-white tracking-tighter">CP-AI</h1>
        </div>
        <div className="flex items-center space-x-4">
            <button 
              onClick={() => setActiveTab('dashboard')}
              className={`p-2 rounded-lg ${activeTab === 'dashboard' ? 'text-teal-400' : 'text-slate-500'}`}
            >
              <Icons.Dashboard />
            </button>
            <button 
              onClick={() => setActiveTab('predict')}
              className={`p-2 rounded-lg ${activeTab === 'predict' ? 'text-teal-400' : 'text-slate-500'}`}
            >
              <Icons.Job />
            </button>
            <button onClick={onLogout} className="p-2 text-slate-500 hover:text-red-400 transition-colors">
                <Icons.Logout />
            </button>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-grow flex flex-col min-h-screen overflow-hidden relative">
        {/* Background Decor */}
        <div className="absolute top-[20%] right-[-5%] w-[30%] h-[30%] bg-blue-500/10 blur-[100px] rounded-full"></div>
        
        <div className="flex-grow overflow-y-auto p-6 md:p-12 relative z-10">
            <div className="max-w-6xl mx-auto">
                {children}
            </div>
        </div>
      </main>
    </div>
  );
};

export default Layout;
