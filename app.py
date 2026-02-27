
import streamlit as st
import pandas as pd
import plotly.express as px
from auth import login_user, create_user
from database import init_db, add_prediction, get_user_history, get_all_history
from ml_model import ml_predictor
from ui import inject_custom_css, card_component

# Initialize Configuration
st.set_page_config(page_title="CareerPath AI", layout="wide", page_icon="🎓")
init_db()
inject_custom_css()

# Session State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = None

def main():
    if not st.session_state.logged_in:
        auth_page()
    else:
        sidebar_nav()

def auth_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; color: #0d9488;'>🎓 CareerPath AI</h1>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type='password', key="login_pass")
            if st.button("Sign In"):
                user = login_user(email, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user_info = {'id': user[0], 'name': user[1], 'email': user[2], 'role': user[4]}
                    st.rerun()
                else:
                    st.error("Invalid credentials")
                    
        with tab2:
            new_name = st.text_input("Full Name")
            new_email = st.text_input("Email")
            new_pass = st.text_input("Password", type='password')
            if st.button("Create Account"):
                if create_user(new_name, new_email, new_pass):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("User already exists")

def sidebar_nav():
    user = st.session_state.user_info
    st.sidebar.markdown(f"### Welcome, {user['name']} 👋")
    st.sidebar.markdown(f"*Role: {user['role'].capitalize()}*")
    st.sidebar.divider()
    
    menu = ["Dashboard", "Predict Job Role", "My History"]
    if user['role'] == 'admin':
        menu.append("Admin Panel")
    
    choice = st.sidebar.radio("Navigation", menu)
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_info = None
        st.rerun()

    if choice == "Dashboard":
        show_dashboard(user)
    elif choice == "Predict Job Role":
        show_prediction_page(user)
    elif choice == "My History":
        show_history(user)
    elif choice == "Admin Panel":
        show_admin_panel()

def show_dashboard(user):
    st.title("🚀 Career Insights")
    history = get_user_history(user['id'])
    
    if not history.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Your Recent Predictions")
            st.dataframe(history[['degree', 'specialization', 'prediction', 'timestamp']].head())
        
        with col2:
            st.subheader("Field Distribution")
            fig = px.pie(history, names='specialization', color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Start your journey by making your first prediction!")

def show_prediction_page(user):
    st.title("🔍 Job Role Predictor")
    
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        with col1:
            degree = st.selectbox("Current Degree", ["B.Tech", "B.Sc", "B.Com", "BBA", "MBA", "M.Tech"])
            spec = st.selectbox("Specialization", ["CSE", "Computer Science", "CSBS", "AI", "Artificial Intelligence", "Data Science", "ECE", "Electronics", "IT", "Computer", "Commerce", "Math", "Physics", "Finance", "HR", "Marketing"])
        with col2:
            cgpa = st.slider("CGPA", 0.0, 10.0, 8.0)
            skills = st.multiselect("Skills / Certifications", ["Python", "Java", "React", "SQL", "Cloud", "Management", "Communication", "Data Analysis"])
            
        submitted = st.form_submit_button("Predict Suitable Roles")
        
        if submitted:
            with st.spinner("🤖 AI is analyzing your profile..."):
                # Use ML prediction
                prediction = ml_predictor.predict_job(degree, spec, cgpa)
                add_prediction(user['id'], degree, spec, cgpa, ", ".join(skills), prediction)
                
                st.success(f"Based on your profile, we recommend: **{prediction}**")
                
                # Show model info
                model_info = ml_predictor.get_model_info()
                st.info(f"Prediction Method: {model_info['status']}")
                
                # Show additional insights
                st.subheader("📊 Your Profile Analysis")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Degree", degree)
                with col2:
                    st.metric("Specialization", spec)
                with col3:
                    st.metric("CGPA", f"{cgpa:.1f}")
                
                if skills:
                    st.subheader("🎯 Skills & Certifications")
                    skills_text = ", ".join(skills)
                    st.write(f"**Selected Skills:** {skills_text}")

def show_history(user):
    st.title("📜 Prediction History")
    history = get_user_history(user['id'])
    if not history.empty:
        st.dataframe(history, use_container_width=True)
    else:
        st.warning("No history found.")

def show_admin_panel():
    st.title("🛡️ Admin Dashboard")
    
    tab1, tab2, tab3 = st.tabs(["Global History", "ML Model Status", "System Management"])
    
    with tab1:
        st.subheader("All User Activity")
        all_data = get_all_history()
        st.dataframe(all_data)
        
    with tab2:
        st.subheader("🤖 ML Model Information")
        model_info = ml_predictor.get_model_info()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Model Status", model_info['status'])
            if 'dataset_size' in model_info:
                st.metric("Dataset Size", model_info['dataset_size'])
        with col2:
            if 'unique_jobs' in model_info:
                st.metric("Job Categories", model_info['unique_jobs'])
            if 'model_type' in model_info:
                st.metric("Model Type", model_info['model_type'])
        
        st.info("💡 The system uses ML predictions when available, with rule-based fallback for robustness.")
        
    with tab3:
        st.subheader("🔧 System Management")
        st.write("System is running with integrated ML + Rule-based predictions")
        
        # Show system stats
        try:
            df = pd.read_csv('job_dataset.csv')
            st.metric("Training Dataset Size", len(df))
            st.metric("Available Job Roles", df['JobRole'].nunique())
        except:
            st.warning("Training dataset not found")
        
        st.success("✅ Full-stack system is operational!")

if __name__ == '__main__':
    main()
