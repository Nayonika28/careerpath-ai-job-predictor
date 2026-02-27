
export enum UserRole {
  ADMIN = 'ADMIN',
  USER = 'USER'
}

export interface User {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  passwordHash: string;
}

export interface EducationDetails {
  degree: string;
  specialization: string;
  cgpa: number;
  graduationYear: number;
  skills: string[];
  certifications: string[];
}

export interface JobRolePrediction {
  roleName: string;
  confidence: number;
  interestScore: number; // Derived from CGPA and Skillsets
  explanation: string;
}

export interface PredictionRecord {
  id: string;
  userId: string;
  userName: string;
  timestamp: number;
  education: EducationDetails;
  predictions: JobRolePrediction[];
}

export interface AppState {
  currentUser: User | null;
  predictions: PredictionRecord[];
  allUsers: User[];
}
