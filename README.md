
# CareerPath AI - Job Role Predictor

A professional Streamlit-based application that uses Machine Learning to predict suitable job roles based on education details.

## Features
- **Secure Authentication**: User registration and login with SHA-256 hashing.
- **Role-Based Access**: Separate interfaces for Users and Admins.
- **AI Prediction**: Random Forest model predicting top career matches.
- **Dashboard**: Interactive visualizations using Plotly.
- **Admin Control**: Monitor all predictions and retrain the model with new data.

## Setup Instructions
1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   streamlit run app.py
   ```

## Default Admin Credentials
- **Email**: `admin@example.com`
- **Password**: `admin123`
