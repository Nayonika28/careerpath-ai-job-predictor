"""
Random Forest Model - Enhanced ML Prediction System
==================================================

This module implements Random Forest classifier for job role prediction
with improved accuracy and robustness for the CareerPath AI system.

Author: CareerPath AI Team
Date: 2026
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

class RandomForestJobPredictor:
    def __init__(self):
        self.model = None
        self.degree_encoder = None
        self.spec_encoder = None
        self.job_encoder = None
        self.accuracy = None
        self.is_trained = False
        self.load_model()
    
    def load_model(self):
        """Load pre-trained Random Forest model"""
        try:
            if os.path.exists('rf_job_model.pkl'):
                with open('rf_job_model.pkl', 'rb') as f:
                    self.model = pickle.load(f)
                with open('rf_degree_encoder.pkl', 'rb') as f:
                    self.degree_encoder = pickle.load(f)
                with open('rf_spec_encoder.pkl', 'rb') as f:
                    self.spec_encoder = pickle.load(f)
                with open('rf_job_encoder.pkl', 'rb') as f:
                    self.job_encoder = pickle.load(f)
                self.is_trained = True
                print("Random Forest model loaded successfully!")
            else:
                print("No pre-trained Random Forest model found. Please train the model first.")
        except Exception as e:
            print(f"Error loading model: {e}")
    
    def train_random_forest(self, dataset_path='improved_dataset.csv'):
        """Train Random Forest classifier with enhanced parameters"""
        print("Training Random Forest Classifier...")
        
        # Load dataset
        df = pd.read_csv(dataset_path)
        print(f"Dataset shape: {df.shape}")
        print(f"Unique job roles: {df['JobRole'].nunique()}")
        
        # Initialize encoders
        self.degree_encoder = LabelEncoder()
        self.spec_encoder = LabelEncoder()
        self.job_encoder = LabelEncoder()
        
        # Encode features
        df['Degree_Encoded'] = self.degree_encoder.fit_transform(df['Degree'])
        df['Specialization_Encoded'] = self.spec_encoder.fit_transform(df['Specialization'])
        df['JobRole_Encoded'] = self.job_encoder.fit_transform(df['JobRole'])
        
        # Prepare features and target
        X = df[['Degree_Encoded', 'Specialization_Encoded', 'CGPA']]
        y = df['JobRole_Encoded']
        
        # Split dataset
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train Random Forest with optimized parameters
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=2,
            min_samples_leaf=1,
            random_state=42,
            criterion='entropy',
            bootstrap=True,
            oob_score=True
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        self.accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Random Forest Accuracy: {self.accuracy:.4f} ({self.accuracy*100:.2f}%)")
        print(f"OOB Score: {self.model.oob_score_:.4f}")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': ['Degree', 'Specialization', 'CGPA'],
            'importance': self.model.feature_importances_
        })
        print("\nFeature Importance:")
        print(feature_importance)
        
        # Save model
        self.save_model()
        self.is_trained = True
        
        return self.accuracy
    
    def save_model(self):
        """Save Random Forest model and encoders"""
        with open('rf_job_model.pkl', 'wb') as f:
            pickle.dump(self.model, f)
        with open('rf_degree_encoder.pkl', 'wb') as f:
            pickle.dump(self.degree_encoder, f)
        with open('rf_spec_encoder.pkl', 'wb') as f:
            pickle.dump(self.spec_encoder, f)
        with open('rf_job_encoder.pkl', 'wb') as f:
            pickle.dump(self.job_encoder, f)
        print("Random Forest model and encoders saved successfully!")
    
    def predict_job_role(self, degree, specialization, cgpa):
        """
        Predict job role using Random Forest model
        
        Args:
            degree (str): Degree name
            specialization (str): Specialization name
            cgpa (float): CGPA score
            
        Returns:
            dict: Prediction results with confidence
        """
        if not self.is_trained:
            return {
                'prediction': 'Model not trained',
                'confidence': 0.0,
                'method': 'N/A'
            }
        
        try:
            # Encode inputs
            degree_encoded = self.degree_encoder.transform([degree])[0]
            spec_encoded = self.spec_encoder.transform([specialization])[0]
            
            # Create feature array
            features = np.array([[degree_encoded, spec_encoded, cgpa]])
            
            # Make prediction
            prediction_encoded = self.model.predict(features)[0]
            prediction_proba = self.model.predict_proba(features)[0]
            confidence = np.max(prediction_proba)
            
            # Decode prediction
            predicted_job = self.job_encoder.inverse_transform([prediction_encoded])[0]
            
            return {
                'prediction': predicted_job,
                'confidence': round(confidence * 100, 2),
                'method': 'Random Forest',
                'accuracy': self.accuracy
            }
            
        except Exception as e:
            return {
                'prediction': f'Prediction error: {str(e)}',
                'confidence': 0.0,
                'method': 'Random Forest'
            }
    
    def get_model_info(self):
        """Get comprehensive model information"""
        if not self.is_trained:
            return {
                'status': 'Not trained',
                'accuracy': 'N/A',
                'model_type': 'Random Forest',
                'feature_importance': {}
            }
        
        feature_importance = {
            'Degree': self.model.feature_importances_[0],
            'Specialization': self.model.feature_importances_[1],
            'CGPA': self.model.feature_importances_[2]
        }
        
        return {
            'status': 'Trained',
            'accuracy': f"{self.accuracy:.2%}",
            'model_type': 'Random Forest',
            'n_estimators': self.model.n_estimators,
            'oob_score': f"{self.model.oob_score_:.2%}",
            'feature_importance': feature_importance
        }
    
    def generate_prediction_report(self, degree, specialization, cgpa):
        """Generate detailed prediction report"""
        result = self.predict_job_role(degree, specialization, cgpa)
        
        accuracy_val = result.get('accuracy', 'N/A')
        accuracy_str = f"{accuracy_val:.2%}" if isinstance(accuracy_val, (int, float)) else str(accuracy_val)
        
        if result['confidence'] > 0:
            report = f"""
            🎯 **Prediction Report**
            
            **Predicted Job Role:** {result['prediction']}
            **Confidence Level:** {result['confidence']}%
            **Model Used:** {result['method']}
            **Model Accuracy:** {accuracy_str}
            
            **Input Profile:**
            - Degree: {degree}
            - Specialization: {specialization}
            - CGPA: {cgpa}
            """
        else:
            report = f"❌ **Prediction Failed:** {result['prediction']}"
        
        return report

# Global predictor instance
rf_predictor = RandomForestJobPredictor()
