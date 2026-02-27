
import React, { useState } from 'react';
import { Icons } from '../constants';
import { EducationDetails } from '../types';

interface PredictionFormProps {
  onSubmit: (details: EducationDetails) => void;
  isLoading: boolean;
}

const PredictionForm: React.FC<PredictionFormProps> = ({ onSubmit, isLoading }) => {
  const [details, setDetails] = useState<EducationDetails>({
    degree: '',
    specialization: '',
    cgpa: 0,
    graduationYear: new Date().getFullYear(),
    skills: [],
    certifications: []
  });
  const [skillInput, setSkillInput] = useState('');
  const [certInput, setCertInput] = useState('');

  const addSkill = () => {
    if (skillInput.trim() && !details.skills.includes(skillInput.trim())) {
      setDetails({ ...details, skills: [...details.skills, skillInput.trim()] });
      setSkillInput('');
    }
  };

  const addCert = () => {
    if (certInput.trim() && !details.certifications.includes(certInput.trim())) {
      setDetails({ ...details, certifications: [...details.certifications, certInput.trim()] });
      setCertInput('');
    }
  };

  const removeSkill = (skill: string) => {
    setDetails({ ...details, skills: details.skills.filter(s => s !== skill) });
  };

  const removeCert = (cert: string) => {
    setDetails({ ...details, certifications: details.certifications.filter(c => c !== cert) });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (details.skills.length === 0) {
        alert("Enter your expertise to proceed.");
        return;
    }
    onSubmit(details);
  };

  // High Contrast Elite Input Classes
  const inputClasses = "w-full bg-slate-900 border border-white/20 px-6 py-4 rounded-2xl text-white font-bold text-lg focus:ring-2 focus:ring-teal-400 focus:border-transparent outline-none transition-all placeholder:text-slate-500 shadow-inner";
  const labelClasses = "block text-[10px] font-black text-teal-400 uppercase tracking-[0.3em] mb-3 ml-1";

  return (
    <div className="bg-white/5 backdrop-blur-3xl border border-white/10 rounded-[3rem] overflow-hidden shadow-2xl relative">
      <div className="absolute top-0 right-0 w-32 h-32 bg-teal-500/10 blur-3xl rounded-full"></div>
      
      <div className="bg-gradient-to-r from-teal-600/20 to-blue-600/20 p-10 flex items-center space-x-6 border-b border-white/10">
        <div className="p-4 bg-teal-500/20 rounded-[1.2rem] shadow-lg text-white">
          <Icons.Education />
        </div>
        <div>
          <h2 className="text-3xl font-black text-white tracking-tight">Career Architecture</h2>
          <p className="text-slate-400 font-bold text-xs uppercase tracking-widest mt-1">AI-Powered Profile Analysis</p>
        </div>
      </div>
      
      <form onSubmit={handleSubmit} className="p-10 space-y-10">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
          <div className="space-y-3">
            <label className={labelClasses}>Academic Degree</label>
            <select
              required
              value={details.degree}
              onChange={(e) => setDetails({ ...details, degree: e.target.value })}
              className={`${inputClasses} appearance-none cursor-pointer`}
            >
              <option value="" className="bg-slate-950">Select Qualification</option>
              <option value="B.Tech" className="bg-slate-950">B.Tech / Engineering</option>
              <option value="B.Sc" className="bg-slate-950">B.Sc / Science</option>
              <option value="B.CA" className="bg-slate-950">BCA / Computers</option>
              <option value="M.Tech" className="bg-slate-950">M.Tech / Post-Grad</option>
              <option value="MBA" className="bg-slate-950">MBA / Business</option>
            </select>
          </div>

          <div className="space-y-3">
            <label className={labelClasses}>Core Specialization</label>
            <input
              type="text"
              required
              value={details.specialization}
              onChange={(e) => setDetails({ ...details, specialization: e.target.value })}
              className={inputClasses}
              placeholder="e.g. Machine Learning"
            />
          </div>

          <div className="space-y-3">
            <label className={labelClasses}>GPA / Percentage</label>
            <input
              type="number"
              step="0.01"
              max="10"
              min="0"
              required
              value={details.cgpa || ''}
              onChange={(e) => setDetails({ ...details, cgpa: parseFloat(e.target.value) })}
              className={inputClasses}
              placeholder="0.00"
            />
          </div>

          <div className="space-y-3">
            <label className={labelClasses}>Passing Year</label>
            <input
              type="number"
              required
              value={details.graduationYear}
              onChange={(e) => setDetails({ ...details, graduationYear: parseInt(e.target.value) })}
              className={inputClasses}
            />
          </div>
        </div>

        <div className="space-y-5">
          <label className={labelClasses}>Skill Inventory</label>
          <div className="flex flex-col sm:flex-row space-y-3 sm:space-y-0 sm:space-x-4">
            <input
              type="text"
              value={skillInput}
              onChange={(e) => setSkillInput(e.target.value)}
              className={inputClasses}
              placeholder="Skill Keyword (e.g. React)"
              onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addSkill())}
            />
            <button
              type="button"
              onClick={addSkill}
              className="px-10 bg-white/10 hover:bg-white/20 text-white font-black rounded-2xl border border-white/10 transition-all uppercase text-[10px] tracking-widest shadow-xl"
            >
              Add Skill
            </button>
          </div>
          <div className="flex flex-wrap gap-3 min-h-[60px] p-6 bg-black/40 rounded-[1.5rem] border border-white/5">
            {details.skills.length === 0 && <span className="text-slate-600 text-[10px] font-black uppercase tracking-[0.2em] self-center">No skills indexed</span>}
            {details.skills.map((skill) => (
              <span key={skill} className="inline-flex items-center px-5 py-2.5 rounded-xl bg-teal-500/10 text-teal-400 text-[11px] font-black border border-teal-500/30 shadow-lg group">
                {skill}
                <button type="button" onClick={() => removeSkill(skill)} className="ml-3 hover:text-red-400 transition-colors">×</button>
              </span>
            ))}
          </div>
        </div>

        <button
          type="submit"
          disabled={isLoading}
          className={`w-full py-6 rounded-[2rem] text-white font-black text-xl shadow-2xl transition-all relative overflow-hidden group border border-white/10 ${
            isLoading 
              ? 'bg-slate-800 cursor-not-allowed opacity-50' 
              : 'bg-gradient-to-r from-teal-500 to-blue-600 hover:shadow-[0_0_40px_rgba(20,184,166,0.5)] active:scale-[0.98]'
          }`}
        >
          {isLoading ? (
            <div className="flex items-center justify-center space-x-4">
              <div className="w-6 h-6 border-4 border-white/30 border-t-white rounded-full animate-spin"></div>
              <span className="uppercase tracking-[0.3em] text-xs">Architecting Future...</span>
            </div>
          ) : (
            <span className="uppercase tracking-[0.3em] text-lg">Generate Elite Prediction</span>
          )}
          <div className="absolute inset-0 bg-white/5 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
        </button>
      </form>
    </div>
  );
};

export default PredictionForm;
