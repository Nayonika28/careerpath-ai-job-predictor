"""
ML Model Module - Integrated with Full-Stack Application
========================================================

This module handles the machine learning components for job role prediction.
Integrated with the main application for seamless ML predictions.

Author: ML Developer
Date: 2026
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class MLJobPredictor:
    def __init__(self):
        self.model = None
        self.degree_encoder = None
        self.spec_encoder = None
        self.job_encoder = None
        self.is_trained = False
        self.load_model()
    
    def load_model(self):
        """Load pre-trained model and encoders"""
        try:
            if os.path.exists('job_model.pkl'):
                with open('job_model.pkl', 'rb') as f:
                    self.model = pickle.load(f)
                with open('degree_encoder.pkl', 'rb') as f:
                    self.degree_encoder = pickle.load(f)
                with open('spec_encoder.pkl', 'rb') as f:
                    self.spec_encoder = pickle.load(f)
                with open('job_encoder.pkl', 'rb') as f:
                    self.job_encoder = pickle.load(f)
                self.is_trained = True
                print("ML Model loaded successfully!")
            else:
                print("No pre-trained model found. Please run model_training.py first.")
        except Exception as e:
            print(f"Error loading model: {e}")
    
    def predict_job(self, degree, specialization, cgpa):
        """
        Predict job role using ML model
        
        Args:
            degree (str): Degree name
            specialization (str): Specialization name  
            cgpa (float): CGPA score
            
        Returns:
            str: Predicted job role or fallback prediction
        """
        if not self.is_trained:
            return self.rule_based_prediction(degree, specialization, cgpa)
        
        try:
            # Encode inputs
            degree_encoded = self.degree_encoder.transform([degree])[0]
            spec_encoded = self.spec_encoder.transform([specialization])[0]
            
            # Create feature array
            features = np.array([[degree_encoded, spec_encoded, cgpa]])
            
            # Make prediction
            prediction_encoded = self.model.predict(features)[0]
            
            # Decode prediction
            predicted_job = self.job_encoder.inverse_transform([prediction_encoded])[0]
            
            return predicted_job
            
        except Exception as e:
            print(f"ML prediction failed: {e}")
            return self.rule_based_prediction(degree, specialization, cgpa)
    
    def rule_based_prediction(self, degree, specialization, cgpa):
        """Fallback rule-based prediction system"""
        degree_lower = degree.lower().replace(".", "")
        spec_lower = specialization.lower()
        
        if degree_lower == "btech":
            if "cse" in spec_lower or "computer" in spec_lower or "csbs" in spec_lower:
                if cgpa >= 8.5:
                    return "Software Developer"
                elif cgpa >= 7.5:
                    return "Web Developer"
                else:
                    return "Technical Support Engineer"
            elif "ai" in spec_lower or "artificial intelligence" in spec_lower or "data science" in spec_lower:
                if cgpa >= 8.5:
                    return "Data Scientist"
                else:
                    return "ML Engineer Intern"
            elif "ece" in spec_lower or "electronics" in spec_lower:
                if cgpa >= 8:
                    return "Embedded Systems Engineer"
                else:
                    return "Network Support Engineer"
        elif degree_lower == "bsc":
            if "it" in spec_lower or "computer" in spec_lower:
                if cgpa >= 8:
                    return "System Analyst"
                else:
                    return "IT Support Executive"
            elif "commerce" in spec_lower:
                return "Accounts Executive"
        
        return "Further Skill Development Recommended"
    
    def get_model_info(self):
        """Get model information and statistics"""
        if not self.is_trained:
            return {"status": "Rule-based only", "accuracy": "N/A"}
        
        try:
            # Load dataset for info
            df = pd.read_csv('job_dataset.csv')
            info = {
                "status": "ML Model Active",
                "dataset_size": len(df),
                "unique_jobs": df['JobRole'].nunique(),
                "feature_count": 3,
                "model_type": "Decision Tree Classifier"
            }
            return info
        except:
            return {"status": "ML Model Active", "accuracy": "Available"}

# Global ML predictor instance
ml_predictor = MLJobPredictor()
