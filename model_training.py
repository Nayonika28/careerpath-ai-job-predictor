"""
AI Job Role Prediction System - Model Training Module
=====================================================

This module handles:
- Data loading and preprocessing
- Model training using Decision Tree Classifier
- Model evaluation and persistence
- Job role prediction functionality

Author: ML Developer
Date: 2026
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

# ==================== DATA LOADING & PREPROCESSING ====================

def load_and_preprocess_data():
    """
    Load dataset and perform preprocessing
    Returns: X (features), y (target), encoders
    """
    print("Loading dataset...")
    df = pd.read_csv('job_dataset.csv')
    
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print("\nDataset preview:")
    print(df.head())
    
    # Initialize label encoders
    degree_encoder = LabelEncoder()
    spec_encoder = LabelEncoder()
    job_encoder = LabelEncoder()
    
    # Encode categorical variables
    df['Degree_Encoded'] = degree_encoder.fit_transform(df['Degree'])
    df['Specialization_Encoded'] = spec_encoder.fit_transform(df['Specialization'])
    df['JobRole_Encoded'] = job_encoder.fit_transform(df['JobRole'])
    
    # Prepare features and target
    X = df[['Degree_Encoded', 'Specialization_Encoded', 'CGPA']]
    y = df['JobRole_Encoded']
    
    print(f"\nFeatures shape: {X.shape}")
    print(f"Target shape: {y.shape}")
    print(f"Unique job roles: {len(job_encoder.classes_)}")
    
    return X, y, degree_encoder, spec_encoder, job_encoder, df

# ==================== MODEL TRAINING ====================

def train_model(X, y):
    """
    Train Decision Tree Classifier model
    Returns: trained model, X_test, y_test
    """
    print("\nTraining Decision Tree Classifier...")
    
    # Split dataset (80% train, 20% test)
    # Remove stratify due to single instances of each class
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"Training set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")
    
    # Initialize and train model
    model = DecisionTreeClassifier(
        random_state=42,
        max_depth=10,
        min_samples_split=2,
        min_samples_leaf=1
    )
    
    model.fit(X_train, y_train)
    print("Model training completed!")
    
    return model, X_test, y_test, X_train, y_train

# ==================== MODEL EVALUATION ====================

def evaluate_model(model, X_test, y_test, job_encoder):
    """
    Evaluate model performance
    """
    print("\nEvaluating model performance...")
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    # Generate confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    
    print("\nConfusion Matrix:")
    plt.figure(figsize=(12, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=job_encoder.classes_,
                yticklabels=job_encoder.classes_)
    plt.title('Confusion Matrix - Job Role Prediction')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig('confusion_matrix.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return accuracy

# ==================== MODEL PERSISTENCE ====================

def save_model_and_encoders(model, degree_encoder, spec_encoder, job_encoder):
    """
    Save trained model and encoders to disk
    """
    print("\nSaving model and encoders...")
    
    # Save model
    with open('job_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    # Save encoders
    with open('degree_encoder.pkl', 'wb') as f:
        pickle.dump(degree_encoder, f)
    
    with open('spec_encoder.pkl', 'wb') as f:
        pickle.dump(spec_encoder, f)
    
    with open('job_encoder.pkl', 'wb') as f:
        pickle.dump(job_encoder, f)
    
    print("Model and encoders saved successfully!")
    print("Files created:")
    print("- job_model.pkl")
    print("- degree_encoder.pkl")
    print("- spec_encoder.pkl")
    print("- job_encoder.pkl")

# ==================== PREDICTION FUNCTION ====================

def predict_job(degree, specialization, cgpa):
    """
    Predict job role based on degree, specialization, and CGPA
    
    Args:
        degree (str): Degree name
        specialization (str): Specialization name
        cgpa (float): CGPA score
    
    Returns:
        str: Predicted job role
    """
    try:
        # Load model and encoders
        with open('job_model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        with open('degree_encoder.pkl', 'rb') as f:
            degree_encoder = pickle.load(f)
        
        with open('spec_encoder.pkl', 'rb') as f:
            spec_encoder = pickle.load(f)
        
        with open('job_encoder.pkl', 'rb') as f:
            job_encoder = pickle.load(f)
        
        # Encode inputs
        degree_encoded = degree_encoder.transform([degree])[0]
        spec_encoded = spec_encoder.transform([specialization])[0]
        
        # Create feature array
        features = np.array([[degree_encoded, spec_encoded, cgpa]])
        
        # Make prediction
        prediction_encoded = model.predict(features)[0]
        
        # Decode prediction
        predicted_job = job_encoder.inverse_transform([prediction_encoded])[0]
        
        return predicted_job
    
    except Exception as e:
        return f"Prediction Error: {str(e)}"

# ==================== MAIN TRAINING PIPELINE ====================

def main():
    """
    Main function to execute the complete training pipeline
    """
    print("=" * 60)
    print("AI JOB ROLE PREDICTION SYSTEM - MODEL TRAINING")
    print("=" * 60)
    
    # Step 1: Load and preprocess data
    X, y, degree_encoder, spec_encoder, job_encoder, df = load_and_preprocess_data()
    
    # Step 2: Train model
    model, X_test, y_test, X_train, y_train = train_model(X, y)
    
    # Step 3: Evaluate model
    accuracy = evaluate_model(model, X_test, y_test, job_encoder)
    
    # Step 4: Save model and encoders
    save_model_and_encoders(model, degree_encoder, spec_encoder, job_encoder)
    
    # Step 5: Test prediction function
    print("\nTesting prediction function...")
    test_prediction = predict_job("B.Tech", "Computer Science", 8.5)
    print(f"Test Prediction: {test_prediction}")
    
    print("\n" + "=" * 60)
    print("TRAINING COMPLETED SUCCESSFULLY!")
    print(f"Model Accuracy: {accuracy:.4f}")
    print("=" * 60)
    
    return accuracy

# ==================== EXECUTION ====================

if __name__ == "__main__":
    main()
