"""
Improved ML Model Training - Better Dataset for Higher Accuracy
========================================================

This module trains the ML model with an improved dataset that has
multiple samples per job role for better learning and accuracy.

Author: ML Developer
Date: 2026
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

# ==================== DATA LOADING & PREPROCESSING ====================

def load_and_preprocess_data():
    """
    Load improved dataset and perform preprocessing
    Returns: X (features), y (target), encoders
    """
    print("Loading improved dataset...")
    df = pd.read_csv('improved_dataset.csv')
    
    print(f"Dataset shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"Unique job roles: {df['JobRole'].nunique()}")
    print("\nJob Role Distribution:")
    print(df['JobRole'].value_counts())
    
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
    
    return X, y, degree_encoder, spec_encoder, job_encoder, df

# ==================== MODEL TRAINING ====================

def train_model(X, y):
    """
    Train Decision Tree Classifier model
    Returns: trained model, X_test, y_test
    """
    print("\nTraining Decision Tree Classifier...")
    
    # Split dataset (80% train, 20% test)
    # Remove stratify due to some classes having only 1-2 members
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"Training set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")
    
    # Initialize and train model
    model = DecisionTreeClassifier(
        random_state=42,
        max_depth=15,
        min_samples_split=2,
        min_samples_leaf=1,
        criterion='entropy'
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
    
    # Generate classification report
    print("\nClassification Report:")
    # Get unique labels present in y_test and y_pred
    unique_labels = sorted(list(set(y_test) | set(y_pred)))
    unique_class_names = [job_encoder.classes_[i] for i in unique_labels]
    
    report = classification_report(y_test, y_pred, labels=unique_labels, target_names=unique_class_names)
    print(report)
    
    # Generate confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    
    print("\nConfusion Matrix:")
    plt.figure(figsize=(15, 12))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=job_encoder.classes_,
                yticklabels=job_encoder.classes_)
    plt.title('Confusion Matrix - Improved Job Role Prediction')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig('improved_confusion_matrix.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return accuracy

# ==================== MODEL PERSISTENCE ====================

def save_model_and_encoders(model, degree_encoder, spec_encoder, job_encoder):
    """
    Save trained model and encoders to disk
    """
    print("\nSaving improved model and encoders...")
    
    # Save model
    with open('improved_job_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    # Save encoders
    with open('improved_degree_encoder.pkl', 'wb') as f:
        pickle.dump(degree_encoder, f)
    
    with open('improved_spec_encoder.pkl', 'wb') as f:
        pickle.dump(spec_encoder, f)
    
    with open('improved_job_encoder.pkl', 'wb') as f:
        pickle.dump(job_encoder, f)
    
    print("Improved model and encoders saved successfully!")
    print("Files created:")
    print("- improved_job_model.pkl")
    print("- improved_degree_encoder.pkl")
    print("- improved_spec_encoder.pkl")
    print("- improved_job_encoder.pkl")

# ==================== PREDICTION FUNCTION ====================

def predict_job_improved(degree, specialization, cgpa):
    """
    Predict job role using improved ML model
    
    Args:
        degree (str): Degree name
        specialization (str): Specialization name
        cgpa (float): CGPA score
    
    Returns:
        str: Predicted job role
    """
    try:
        # Load improved model and encoders
        with open('improved_job_model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        with open('improved_degree_encoder.pkl', 'rb') as f:
            degree_encoder = pickle.load(f)
        
        with open('improved_spec_encoder.pkl', 'rb') as f:
            spec_encoder = pickle.load(f)
        
        with open('improved_job_encoder.pkl', 'rb') as f:
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
    Main function to execute the complete improved training pipeline
    """
    print("=" * 70)
    print("IMPROVED AI JOB ROLE PREDICTION SYSTEM - MODEL TRAINING")
    print("=" * 70)
    
    # Step 1: Load and preprocess data
    X, y, degree_encoder, spec_encoder, job_encoder, df = load_and_preprocess_data()
    
    # Step 2: Train model
    model, X_test, y_test, X_train, y_train = train_model(X, y)
    
    # Step 3: Evaluate model
    accuracy = evaluate_model(model, X_test, y_test, job_encoder)
    
    # Step 4: Save model and encoders
    save_model_and_encoders(model, degree_encoder, spec_encoder, job_encoder)
    
    # Step 5: Test prediction function
    print("\nTesting improved prediction function...")
    test_prediction = predict_job_improved("B.Tech", "Computer Science", 8.5)
    print(f"Test Prediction: {test_prediction}")
    
    print("\n" + "=" * 70)
    print("IMPROVED TRAINING COMPLETED SUCCESSFULLY!")
    print(f"Improved Model Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print("=" * 70)
    
    return accuracy

# ==================== EXECUTION ====================

if __name__ == "__main__":
    main()
