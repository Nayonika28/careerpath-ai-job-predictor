# CareerPath AI - Complete Job Role Prediction System

## Project Overview

CareerPath AI is a comprehensive full-stack web application that predicts suitable job roles based on users' academic qualifications using Machine Learning. The system combines authentication, user profile management, and Random Forest algorithm to provide intelligent career guidance.

## Features

### 🔐 Authentication System
- User registration and login with SHA-256 password hashing
- Role-based access control (User/Admin)
- Session management with Streamlit
- Secure database storage

### 👤 User Profile Management
- Academic details storage (Degree, Specialization, CGPA)
- Profile completion tracking
- Skills, projects, and certifications management
- University and graduation year tracking

### 🤖 Machine Learning Prediction
- Random Forest Classifier for job role prediction
- Trained on 62 samples with 27 unique job roles
- Feature importance analysis
- Confidence scoring for predictions

### 📊 Analytics & Visualizations
- Interactive dashboards with Plotly charts
- Prediction history tracking
- Dataset insights and statistics
- Admin analytics panel

### 🛡️ Admin Panel
- System overview and user management
- Model performance monitoring
- Retraining capabilities
- Comprehensive analytics

## Technology Stack

### Backend
- **Python 3.13**: Core programming language
- **Streamlit**: Web framework for dashboard
- **SQLite**: Database for user data and predictions
- **scikit-learn**: Machine Learning library
- **pandas**: Data manipulation
- **plotly**: Data visualization

### Frontend
- **Streamlit Components**: UI elements
- **Plotly Charts**: Interactive visualizations
- **Custom CSS**: Enhanced styling

### Machine Learning
- **Random Forest Classifier**: Primary algorithm
- **Label Encoding**: Feature preprocessing
- **Train-Test Split**: Model validation
- **Feature Importance**: Model interpretability

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT
);
```

### User Profiles Table
```sql
CREATE TABLE user_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    degree TEXT,
    specialization TEXT,
    cgpa REAL,
    university TEXT,
    graduation_year INTEGER,
    skills TEXT,
    projects TEXT,
    certifications TEXT,
    profile_complete INTEGER DEFAULT 0,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
```

### History Table
```sql
CREATE TABLE history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    degree TEXT,
    specialization TEXT,
    cgpa REAL,
    skills TEXT,
    prediction TEXT,
    timestamp DATETIME,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
```

## Machine Learning Model

### Dataset
- **Total Samples**: 62
- **Job Roles**: 27 unique categories
- **Features**: Degree, Specialization, CGPA
- **Target Variable**: Job Role

### Model Performance
- **Algorithm**: Random Forest Classifier
- **Accuracy**: 30.77% (initial training)
- **Estimators**: 100 trees
- **Validation**: Out-of-Bag scoring

### Feature Importance
- Specialization: 39.49%
- CGPA: 32.55%
- Degree: 27.96%

## Installation & Setup

### Prerequisites
- Python 3.13 or higher
- pip package manager

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/Nayonika28/careerpath-ai-job-predictor.git
cd careerpath-ai-job-predictor
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Train the ML model**
```bash
python -c "from random_forest_model import rf_predictor; rf_predictor.train_random_forest()"
```

4. **Run the application**
```bash
streamlit run careerpath_app.py
```

### Default Credentials
- **Email**: admin@example.com
- **Password**: admin123

## Usage Guide

### For Users

1. **Registration**: Create an account with email and password
2. **Profile Setup**: Complete academic profile with degree, specialization, and CGPA
3. **Get Predictions**: Use the prediction page to get job role recommendations
4. **Track History**: View prediction history and analytics

### For Administrators

1. **System Monitoring**: Track user activity and system performance
2. **User Management**: View and manage user profiles
3. **Model Management**: Monitor and retrain ML model
4. **Analytics**: Access comprehensive system analytics

## Project Structure

```
careerpath-ai-job-predictor/
├── careerpath_app.py          # Main application
├── auth.py                    # Authentication logic
├── database.py                # Database operations
├── user_profile.py            # Profile management
├── random_forest_model.py     # ML model implementation
├── ui.py                      # UI components
├── improved_dataset.csv       # Training dataset
├── requirements.txt           # Python dependencies
├── PROJECT_DOCUMENTATION.md   # This file
└── [ML Model Files]           # Trained models
    ├── rf_job_model.pkl
    ├── rf_degree_encoder.pkl
    ├── rf_spec_encoder.pkl
    └── rf_job_encoder.pkl
```

## API Reference

### Authentication Functions

#### `login_user(email, password)`
Authenticates user with email and password.

#### `create_user(name, email, password, role='user')`
Creates new user account with SHA-256 password hashing.

### Profile Functions

#### `save_user_profile(user_id, degree, specialization, cgpa, ...)`
Saves or updates user academic profile.

#### `get_user_profile(user_id)`
Retrieves user profile information.

### ML Functions

#### `predict_job_role(degree, specialization, cgpa)`
Predicts job role using Random Forest model.

#### `train_random_forest(dataset_path)`
Trains Random Forest classifier with specified dataset.

## Testing

### Unit Tests
- Authentication system validation
- Database operations testing
- ML model prediction accuracy

### Integration Tests
- End-to-end user workflow
- Admin panel functionality
- Model training and prediction pipeline

### System Tests
- Load testing with multiple users
- Database performance testing
- Error handling and recovery

## Deployment

### Local Development
```bash
streamlit run careerpath_app.py
```

### Production Deployment
- **Streamlit Cloud**: Deploy to Streamlit's cloud platform
- **Docker**: Containerize application for portability
- **Cloud Services**: AWS, Azure, or Google Cloud deployment

## Performance Optimization

### Database Optimization
- Indexed queries for faster data retrieval
- Connection pooling for concurrent users
- Regular database maintenance

### Model Optimization
- Hyperparameter tuning for better accuracy
- Feature engineering for improved predictions
- Model compression for faster inference

### UI Optimization
- Lazy loading for large datasets
- Caching for frequently accessed data
- Responsive design for mobile devices

## Security Considerations

### Authentication Security
- SHA-256 password hashing
- Session timeout management
- SQL injection prevention

### Data Protection
- Input validation and sanitization
- Secure database connections
- Privacy policy compliance

### System Security
- Error handling without information leakage
- Rate limiting for API endpoints
- Regular security updates

## Future Enhancements

### Planned Features
- **Advanced ML Models**: Deep learning and ensemble methods
- **Real-time Recommendations**: Live career guidance
- **Mobile Application**: React Native mobile app
- **Integration APIs**: Connect with job portals
- **Skill Assessment**: Automated skill evaluation

### Technical Improvements
- **Microservices Architecture**: Scalable system design
- **Cloud Database**: PostgreSQL or MongoDB
- **Caching Layer**: Redis for performance
- **Monitoring**: Application performance monitoring

## Contributing

### Development Guidelines
1. Follow PEP 8 Python style guide
2. Write comprehensive tests for new features
3. Update documentation for API changes
4. Use semantic versioning for releases

### Git Workflow
1. Create feature branch from main
2. Make changes with descriptive commits
3. Test thoroughly before pull request
4. Code review and merge

## Support

### Troubleshooting
- **Model Training Issues**: Check dataset format and dependencies
- **Database Errors**: Verify SQLite permissions and disk space
- **Authentication Problems**: Clear browser cache and cookies

### Contact
- **GitHub Issues**: Report bugs and feature requests
- **Email**: support@careerpath-ai.com
- **Documentation**: Check this file and inline code comments

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Acknowledgments

- **scikit-learn**: Machine Learning library
- **Streamlit**: Web application framework
- **Plotly**: Data visualization library
- **Open Source Community**: Contributors and supporters

---

**CareerPath AI** - Empowering career decisions with artificial intelligence.
