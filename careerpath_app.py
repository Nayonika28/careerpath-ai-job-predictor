"""
CareerPath AI - Complete Full-Stack Application
===============================================

Milestone 4: Complete integration of authentication, user profiles,
Random Forest ML predictions, and enhanced UI with visualizations.

Features:
- User authentication & registration
- Academic profile management
- Random Forest job role predictions
- Interactive dashboards with charts
- Admin panel with system analytics
- Complete error handling and stability

Author: CareerPath AI Team
Date: 2026
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import sqlite3

# Import custom modules
from auth import login_user, create_user
from database import init_db, add_prediction, get_user_history, get_all_history
from user_profile import create_user_profile_table, save_user_profile, get_user_profile, get_profile_completion_percentage
from random_forest_model import rf_predictor
from ui import inject_custom_css, card_component

# Initialize configuration
st.set_page_config(
    page_title="CareerPath AI - Job Role Predictor", 
    layout="wide", 
    page_icon="🎓",
    initial_sidebar_state="expanded"
)

# Initialize database and tables
init_db()
create_user_profile_table()
inject_custom_css()

# Session state management
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = None
if 'profile_updated' not in st.session_state:
    st.session_state.profile_updated = False

def main():
    """Main application router"""
    if not st.session_state.logged_in:
        show_auth_page()
    else:
        show_main_app()

def show_auth_page():
    """Authentication page with login and registration"""
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h1 style='color: #0d9488; font-size: 3rem;'>🎓 CareerPath AI</h1>
        <p style='font-size: 1.2rem; color: #666;'>Your Intelligent Career Path Predictor</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with tab1:
            st.subheader("Welcome Back!")
            login_email = st.text_input("Email Address", key="login_email")
            login_password = st.text_input("Password", type="password", key="login_pass")
            
            if st.button("Sign In", use_container_width=True, type="primary"):
                user = login_user(login_email, login_password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_info = {
                        'id': user[0], 
                        'name': user[1], 
                        'email': user[2], 
                        'role': user[4]
                    }
                    st.success(f"Welcome back, {user[1]}! 🎉")
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password")
        
        with tab2:
            st.subheader("Create Your Account")
            reg_name = st.text_input("Full Name", key="reg_name")
            reg_email = st.text_input("Email Address", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
            
            if st.button("Create Account", use_container_width=True):
                if reg_password != reg_confirm:
                    st.error("❌ Passwords do not match")
                elif len(reg_password) < 6:
                    st.error("❌ Password must be at least 6 characters")
                elif create_user(reg_name, reg_email, reg_password):
                    st.success("✅ Account created successfully! Please login.")
                    st.balloons()
                else:
                    st.error("❌ Email already exists")

def show_main_app():
    """Main application interface"""
    user = st.session_state.user_info
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"""
        ### 👋 Welcome, {user['name']}!
        **Role:** {user['role'].capitalize()}
        """)
        st.divider()
        
        # Menu options based on user role
        if user['role'] == 'admin':
            menu_options = ["🏠 Dashboard", "👤 Profile", "🔮 Predictions", "📊 Analytics", "🛡️ Admin Panel"]
        else:
            menu_options = ["🏠 Dashboard", "👤 Profile", "🔮 Predictions", "📊 Analytics"]
        
        choice = st.radio("Navigation", menu_options)
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_info = None
            st.rerun()
    
    # Route to selected page
    if choice == "🏠 Dashboard":
        show_dashboard()
    elif choice == "👤 Profile":
        show_profile_page()
    elif choice == "🔮 Predictions":
        show_prediction_page()
    elif choice == "📊 Analytics":
        show_analytics_page()
    elif choice == "🛡️ Admin Panel" and user['role'] == 'admin':
        show_admin_panel()

def show_dashboard():
    """Enhanced dashboard with insights and charts"""
    st.title("🏠 Career Dashboard")
    user = st.session_state.user_info
    
    # Get user data
    profile = get_user_profile(user['id'])
    history = get_user_history(user['id'])
    profile_completion = get_profile_completion_percentage(user['id'])
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Profile Completion", f"{profile_completion}%", 
                 help="Complete your profile for better predictions")
    
    with col2:
        st.metric("Total Predictions", len(history) if not history.empty else 0)
    
    with col3:
        if profile and profile.get('cgpa'):
            st.metric("Your CGPA", f"{profile['cgpa']:.1f}")
        else:
            st.metric("Your CGPA", "Not set")
    
    with col4:
        model_info = rf_predictor.get_model_info()
        st.metric("Model Accuracy", model_info.get('accuracy', 'N/A'))
    
    st.divider()
    
    # Charts section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Prediction History")
        if not history.empty:
            # Create prediction timeline
            fig = px.line(
                history, 
                x='timestamp', 
                y='prediction',
                title="Your Prediction Timeline",
                markers=True
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No predictions yet. Make your first prediction to see insights!")
    
    with col2:
        st.subheader("🎯 Job Role Distribution")
        if not history.empty:
            job_counts = history['prediction'].value_counts()
            fig = px.pie(
                values=job_counts.values, 
                names=job_counts.index,
                title="Predicted Job Roles"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Start making predictions to see your job role distribution!")
    
    # Recent activity
    st.subheader("📋 Recent Activity")
    if not history.empty:
        recent_history = history.head(5)
        st.dataframe(
            recent_history[['degree', 'specialization', 'prediction', 'timestamp']],
            use_container_width=True
        )
    else:
        st.info("No recent activity. Complete your profile and make predictions!")

def show_profile_page():
    """User profile management page"""
    st.title("👤 Academic Profile")
    user = st.session_state.user_info
    
    profile = get_user_profile(user['id'])
    profile_completion = get_profile_completion_percentage(user['id'])
    
    # Profile completion indicator
    st.progress(profile_completion / 100)
    st.caption(f"Profile Completion: {profile_completion}%")
    
    # Profile form
    with st.form("profile_form"):
        st.subheader("📚 Academic Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            degree = st.selectbox(
                "Degree",
                ["B.Tech", "B.Sc", "B.Com", "BBA", "MBA", "M.Tech", "Other"],
                index=0 if not profile else ["B.Tech", "B.Sc", "B.Com", "BBA", "MBA", "M.Tech", "Other"].index(profile.get('degree', 'B.Tech'))
            )
            
            specialization = st.selectbox(
                "Specialization",
                ["Computer Science", "Information Technology", "Electronics", "Mechanical", "Civil", 
                 "Electrical", "Chemical", "AI/ML", "Data Science", "Business", "Finance", "HR", "Marketing", "Other"],
                index=0 if not profile else 0
            )
            
            cgpa = st.slider("CGPA", 0.0, 10.0, 
                            value=profile.get('cgpa', 8.0) if profile else 8.0,
                            step=0.1)
        
        with col2:
            university = st.text_input("University", value=profile.get('university', '') if profile else '')
            graduation_year = st.number_input(
                "Graduation Year", 
                min_value=1990, 
                max_value=2030, 
                value=profile.get('graduation_year', 2024) if profile else 2024
            )
            
            skills = st.text_area(
                "Skills (comma-separated)", 
                value=profile.get('skills', '') if profile else '',
                help="e.g., Python, Java, Machine Learning, Data Analysis"
            )
        
        st.subheader("🚀 Additional Information")
        
        col3, col4 = st.columns(2)
        with col3:
            projects = st.text_area(
                "Projects",
                value=profile.get('projects', '') if profile else '',
                help="Describe your academic or personal projects"
            )
        
        with col4:
            certifications = st.text_area(
                "Certifications",
                value=profile.get('certifications', '') if profile else '',
                help="List any relevant certifications"
            )
        
        # Submit button
        submitted = st.form_submit_button("💾 Save Profile", use_container_width=True, type="primary")
        
        if submitted:
            save_user_profile(
                user['id'], degree, specialization, cgpa, university,
                graduation_year, skills, projects, certifications
            )
            st.success("✅ Profile updated successfully!")
            st.session_state.profile_updated = True
            st.rerun()

def show_prediction_page():
    """ML prediction page with Random Forest model"""
    st.title("🔮 Job Role Prediction")
    user = st.session_state.user_info
    
    # Get user profile
    profile = get_user_profile(user['id'])
    
    # Check if profile is complete
    if not profile or not profile.get('degree'):
        st.warning("⚠️ Please complete your academic profile first to get accurate predictions!")
        st.info("👉 Go to Profile page to update your academic information")
        return
    
    # Model information
    model_info = rf_predictor.get_model_info()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Get Your Career Prediction")
        
        with st.form("prediction_form"):
            # Use profile data as defaults
            degree = st.selectbox(
                "Degree",
                ["B.Tech", "B.Sc", "B.Com", "BBA", "MBA", "M.Tech"],
                index=0 if not profile else ["B.Tech", "B.Sc", "B.Com", "BBA", "MBA", "M.Tech"].index(profile.get('degree', 'B.Tech'))
            )
            
            specialization = st.selectbox(
                "Specialization",
                ["Computer Science", "Information Technology", "Electronics", "Mechanical", "Civil",
                 "Electrical", "Chemical", "AI/ML", "Data Science", "Business", "Finance", "HR", "Marketing"],
                index=0
            )
            
            cgpa = st.slider("CGPA", 0.0, 10.0, 
                            value=float(profile.get('cgpa', 8.0)),
                            step=0.1)
            
            submitted = st.form_submit_button("🚀 Predict Job Role", use_container_width=True, type="primary")
            
            if submitted:
                with st.spinner("🤖 AI is analyzing your profile..."):
                    # Get prediction
                    result = rf_predictor.predict_job_role(degree, specialization, cgpa)
                    
                    # Save prediction to history
                    add_prediction(user['id'], degree, specialization, cgpa, "", result['prediction'])
                    
                    # Display results
                    st.success(f"🎉 **Predicted Job Role: {result['prediction']}**")
                    
                    # Confidence meter
                    confidence = result['confidence']
                    st.progress(confidence / 100)
                    st.caption(f"Prediction Confidence: {confidence}%")
                    
                    # Detailed report
                    with st.expander("📊 Detailed Prediction Report"):
                        st.markdown(rf_predictor.generate_prediction_report(degree, specialization, cgpa))
                    
                    # Feature importance
                    if 'feature_importance' in model_info:
                        st.subheader("🔍 Feature Importance")
                        importance_data = model_info['feature_importance']
                        fig = go.Figure(data=[
                            go.Bar(x=list(importance_data.keys()), 
                                  y=list(importance_data.values()),
                                  marker_color='lightblue')
                        ])
                        fig.update_layout(title="Model Feature Importance")
                        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Model Information")
        
        # Model stats
        st.metric("Model Type", model_info['model_type'])
        st.metric("Accuracy", model_info['accuracy'])
        
        if 'oob_score' in model_info:
            st.metric("OOB Score", model_info['oob_score'])
        
        st.info("🤖 This prediction uses Random Forest algorithm trained on real academic data")
        
        # Tips
        st.subheader("💡 Tips for Better Predictions")
        st.markdown("""
        - ✅ Keep your CGPA updated
        - ✅ Provide accurate specialization
        - ✅ Complete your profile fully
        - ✅ Include relevant skills
        """)

def show_analytics_page():
    """Analytics page with dataset insights and visualizations"""
    st.title("📊 Career Analytics")
    
    # Load dataset for insights
    try:
        df = pd.read_csv('improved_dataset.csv')
        
        st.subheader("🎓 Dataset Overview")
        
        # Dataset statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Samples", len(df))
        
        with col2:
            st.metric("Job Roles", df['JobRole'].nunique())
        
        with col3:
            st.metric("Degrees", df['Degree'].nunique())
        
        with col4:
            st.metric("Avg CGPA", f"{df['CGPA'].mean():.2f}")
        
        st.divider()
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Job Role Distribution")
            job_counts = df['JobRole'].value_counts().head(10)
            fig = px.bar(
                x=job_counts.values, 
                y=job_counts.index,
                orientation='h',
                title="Top 10 Job Roles",
                color=job_counts.values,
                color_continuous_scale='viridis'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🎓 Degree Distribution")
            degree_counts = df['Degree'].value_counts()
            fig = px.pie(
                values=degree_counts.values, 
                names=degree_counts.index,
                title="Degree Types",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # CGPA Analysis
        st.subheader("📊 CGPA Analysis by Job Role")
        
        # Top job roles by CGPA
        top_jobs = df.groupby('JobRole')['CGPA'].mean().sort_values(ascending=False).head(10)
        
        fig = px.bar(
            x=top_jobs.values,
            y=top_jobs.index,
            orientation='h',
            title="Average CGPA by Job Role",
            color=top_jobs.values,
            color_continuous_scale='plasma'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        # Dataset table
        st.subheader("📋 Dataset Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Additional analytics
        st.subheader("🔍 Additional Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📚 Specialization Distribution")
            spec_counts = df['Specialization'].value_counts().head(8)
            fig = px.bar(
                x=spec_counts.values,
                y=spec_counts.index,
                orientation='h',
                title="Top 8 Specializations"
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📊 CGPA Distribution")
            fig = px.histogram(
                df, 
                x='CGPA', 
                nbins=20,
                title="CGPA Distribution Histogram",
                color_discrete_sequence=['lightblue']
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
    except FileNotFoundError:
        st.error("❌ Dataset file not found. Please ensure 'improved_dataset.csv' is available.")
        st.info("📁 The dataset should be in the same directory as the application.")
    except Exception as e:
        st.error(f"❌ Error loading analytics: {str(e)}")
        st.info("Please check the dataset file and try again.")

def show_admin_panel():
    """Admin dashboard with system management"""
    st.title("🛡️ Admin Dashboard")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 System Overview", "👥 User Management", "🤖 Model Management", "📈 Analytics"])
    
    with tab1:
        st.subheader("🖥️ System Overview")
        
        # System metrics
        col1, col2, col3, col4 = st.columns(4)
        
        try:
            # Get user statistics
            conn = sqlite3.connect('career_path.db')
            users_df = pd.read_sql_query("SELECT role, COUNT(*) as count FROM users GROUP BY role", conn)
            conn.close()
            
            total_users = users_df['count'].sum()
            admin_users = users_df[users_df['role'] == 'admin']['count'].sum() if 'admin' in users_df['role'].values else 0
            regular_users = total_users - admin_users
            
            with col1:
                st.metric("Total Users", total_users)
            with col2:
                st.metric("Regular Users", regular_users)
            with col3:
                st.metric("Admin Users", admin_users)
            with col4:
                model_info = rf_predictor.get_model_info()
                st.metric("Model Status", model_info['status'])
        except:
            st.error("Unable to fetch system statistics")
        
        # Recent activity
        st.subheader("📋 Recent System Activity")
        all_history = get_all_history()
        if not all_history.empty:
            st.dataframe(all_history.head(10), use_container_width=True)
        else:
            st.info("No system activity recorded yet")
    
    with tab2:
        st.subheader("👥 User Management")
        
        try:
            from user_profile import get_all_profiles_summary
            profiles_df = get_all_profiles_summary()
            
            if not profiles_df.empty:
                st.dataframe(profiles_df, use_container_width=True)
                
                # User statistics
                st.subheader("📊 User Statistics")
                
                # Profile completion distribution
                profile_complete = profiles_df['profile_complete'].value_counts()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig = px.pie(
                        values=profile_complete.values,
                        names=profile_complete.index,
                        title="Profile Completion Distribution"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Degree distribution
                    degree_dist = profiles_df['degree'].value_counts()
                    fig = px.bar(
                        x=degree_dist.values,
                        y=degree_dist.index,
                        orientation='h',
                        title="Degree Distribution"
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No user profiles found")
        except Exception as e:
            st.error(f"Error loading user data: {e}")
    
    with tab3:
        st.subheader("🤖 Model Management")
        
        # Model information
        model_info = rf_predictor.get_model_info()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Model Type", model_info['model_type'])
            st.metric("Status", model_info['status'])
            st.metric("Accuracy", model_info['accuracy'])
        
        with col2:
            if 'n_estimators' in model_info:
                st.metric("Estimators", model_info['n_estimators'])
            if 'oob_score' in model_info:
                st.metric("OOB Score", model_info['oob_score'])
        
        # Feature importance
        if 'feature_importance' in model_info and model_info['feature_importance']:
            st.subheader("🎯 Feature Importance")
            
            importance_data = model_info['feature_importance']
            fig = go.Figure(data=[
                go.Bar(x=list(importance_data.keys()), 
                      y=list(importance_data.values()),
                      marker_color='lightgreen')
            ])
            fig.update_layout(title="Model Feature Importance")
            st.plotly_chart(fig, use_container_width=True)
        
        # Model training section
        st.subheader("🔄 Model Retraining")
        
        if st.button("🚀 Retrain Model", help="Retrain the Random Forest model with current dataset"):
            with st.spinner("Training model..."):
                try:
                    accuracy = rf_predictor.train_random_forest()
                    st.success(f"✅ Model retrained successfully! New accuracy: {accuracy:.2%}")
                except Exception as e:
                    st.error(f"❌ Error training model: {e}")
    
    with tab4:
        st.subheader("📈 System Analytics")
        
        # Prediction trends
        all_history = get_all_history()
        
        if not all_history.empty:
            # Prediction timeline
            st.subheader("📅 Prediction Timeline")
            
            # Convert timestamp to datetime
            all_history['timestamp'] = pd.to_datetime(all_history['timestamp'])
            
            # Daily predictions
            daily_predictions = all_history.groupby(all_history['timestamp'].dt.date).size()
            
            fig = px.line(
                x=daily_predictions.index,
                y=daily_predictions.values,
                title="Daily Prediction Volume",
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Popular predictions
            st.subheader("🎯 Popular Predictions")
            
            prediction_counts = all_history['prediction'].value_counts().head(10)
            
            fig = px.bar(
                x=prediction_counts.values,
                y=prediction_counts.index,
                orientation='h',
                title="Top 10 Predicted Job Roles"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No analytics data available yet")

# Error handling wrapper
def safe_run_app():
    """Run the application with error handling"""
    try:
        main()
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.info("Please refresh the page or contact support if the issue persists.")

if __name__ == "__main__":
    safe_run_app()
