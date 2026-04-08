import streamlit as st
import pandas as pd
import numpy as np
import pickle
from pathlib import Path
import matplotlib.pyplot as plt # Added for charts
import seaborn as sns # Added for charts

# Page configuration
st.set_page_config(page_title="Student Performance Predictor", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        border-radius: 8px;
    }
    /* Custom Risk Level Cards */
    .high-risk-card {
        background-color: #ffebee; /* Light Red */
        border-left: 8px solid #ff4444; /* Red border */
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .medium-risk-card {
        background-color: #fff3e0; /* Light Orange */
        border-left: 8px solid #ffa500; /* Orange border */
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .low-risk-card {
        background-color: #e8f5e9; /* Light Green */
        border-left: 8px solid #44aa44; /* Green border */
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
        /* ... (Student's Values) ... */
    .stMetric > div[data-testid="stMetricValue"] {
        background-color: transparent !important; /* Make background transparent */
        color: #f0f2f6 !important; /* Ensure text is light/white */
        font-weight: bold; /* Keep it bold for emphasis */
    }
    .stMetric > div[data-testid="stMetricLabel"] {
        color: #bbbbbb !important; /* Light gray for labels */
        font-weight: light !important; /* Thinner font for labels */
    }
    .stProgress > div > div > div > div {
        background-color: #4CAF50; /* Green progress bar */
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# MODEL LOADING
# ============================================================================

@st.cache_resource
def load_model_and_scaler():
    """Load the trained model and scaler."""
    try:
        # Load logistic regression model (39 features)
        model_path = Path('models/logistic_regression.pkl')
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        
        # Load scaler
        scaler_path = Path('models/scaler.pkl')
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)
        
        return model, scaler
    
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        return None, None


def create_feature_dataframe(form_inputs):
    """Convert form inputs to DataFrame with correct 39 features."""
    features = {}
    
    # 13 numeric features
    features['age'] = form_inputs.get('age', 17)
    features['Medu'] = form_inputs.get('Medu', 2)
    features['Fedu'] = form_inputs.get('Fedu', 2)
    features['traveltime'] = form_inputs.get('traveltime', 2)
    features['studytime'] = form_inputs.get('studytime', 2)
    features['failures'] = form_inputs.get('failures', 0)
    features['famrel'] = form_inputs.get('famrel', 4)
    features['freetime'] = form_inputs.get('freetime', 3)
    features['goout'] = form_inputs.get('goout', 3)
    features['Dalc'] = form_inputs.get('Dalc', 1)
    features['Walc'] = form_inputs.get('Walc', 1)
    features['health'] = form_inputs.get('health', 3)
    features['absences'] = form_inputs.get('absences', 0)
    
    # Binary features (one-hot encoded, 1 if condition met)
    features['school_MS'] = 1 if form_inputs.get('school') == 'MS' else 0
    features['sex_M'] = 1 if form_inputs.get('sex') == 'M' else 0
    features['address_U'] = 1 if form_inputs.get('address') == 'U' else 0
    features['famsize_LE3'] = 1 if form_inputs.get('famsize') == 'LE3' else 0
    features['Pstatus_T'] = 1 if form_inputs.get('Pstatus') == 'T' else 0
    
    # Mjob (drop first: at_home, keep: health, other, services, teacher)
    mjob = form_inputs.get('Mjob', 'other')
    features['Mjob_health'] = 1 if mjob == 'health' else 0
    features['Mjob_other'] = 1 if mjob == 'other' else 0
    features['Mjob_services'] = 1 if mjob == 'services' else 0
    features['Mjob_teacher'] = 1 if mjob == 'teacher' else 0
    
    # Fjob (drop first: at_home, keep: health, other, services, teacher)
    fjob = form_inputs.get('Fjob', 'other')
    features['Fjob_health'] = 1 if fjob == 'health' else 0
    features['Fjob_other'] = 1 if fjob == 'other' else 0
    features['Fjob_services'] = 1 if fjob == 'services' else 0
    features['Fjob_teacher'] = 1 if fjob == 'teacher' else 0
    
    # Reason (drop first: course, keep: home, other, reputation)
    reason = form_inputs.get('reason', 'other')
    features['reason_home'] = 1 if reason == 'home' else 0
    features['reason_other'] = 1 if reason == 'other' else 0
    features['reason_reputation'] = 1 if reason == 'reputation' else 0
    
    # Guardian (drop first: father, keep: mother, other)
    guardian = form_inputs.get('guardian', 'mother')
    features['guardian_mother'] = 1 if guardian == 'mother' else 0
    features['guardian_other'] = 1 if guardian == 'other' else 0
    
    # Yes/No features (yes = 1)
    features['schoolsup_yes'] = 1 if form_inputs.get('schoolsup') == 'yes' else 0
    features['famsup_yes'] = 1 if form_inputs.get('famsup') == 'yes' else 0
    features['paid_yes'] = 1 if form_inputs.get('paid') == 'yes' else 0
    features['activities_yes'] = 1 if form_inputs.get('activities') == 'yes' else 0
    features['nursery_yes'] = 1 if form_inputs.get('nursery') == 'yes' else 0
    features['higher_yes'] = 1 if form_inputs.get('higher') == 'yes' else 0
    features['internet_yes'] = 1 if form_inputs.get('internet') == 'yes' else 0
    features['romantic_yes'] = 1 if form_inputs.get('romantic') == 'yes' else 0
    
    # Subject (position 39)
    features['subject_portuguese'] = 1 if form_inputs.get('subject') == 'portuguese' else 0
    
    # Engineered features (positions 40-42)
    features['parent_edu_avg'] = (features['Medu'] + features['Fedu']) / 2
    features['total_alcohol'] = features['Dalc'] + features['Walc']
    
    # has_support: any support (school OR family OR paid)
    has_schoolsup = 1 if form_inputs.get('schoolsup') == 'yes' else 0
    has_famsup = 1 if form_inputs.get('famsup') == 'yes' else 0
    has_paid = 1 if form_inputs.get('paid') == 'yes' else 0
    features['has_support'] = 1 if (has_schoolsup or has_famsup or has_paid) else 0
    
    # Create DataFrame with exact column order
    df = pd.DataFrame([features])
    
    # Ensure correct order (43 features - matches model exactly)
    column_order = [
        'age', 'Medu', 'Fedu', 'traveltime', 'studytime', 'failures', 'famrel', 
        'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences',
        'school_MS', 'sex_M', 'address_U', 'famsize_LE3', 'Pstatus_T',
        'Mjob_health', 'Mjob_other', 'Mjob_services', 'Mjob_teacher',
        'Fjob_health', 'Fjob_other', 'Fjob_services', 'Fjob_teacher',
        'reason_home', 'reason_other', 'reason_reputation',
        'guardian_mother', 'guardian_other',
        'schoolsup_yes', 'famsup_yes', 'paid_yes', 'activities_yes',
        'nursery_yes', 'higher_yes', 'internet_yes', 'romantic_yes',
        'subject_portuguese', 'parent_edu_avg', 'total_alcohol', 'has_support'
    ]
    
    return df[column_order]


def make_prediction(form_inputs, model, scaler):
    """Make prediction using the model."""
    try:
        # Create feature DataFrame
        X = create_feature_dataframe(form_inputs)
        
        # Scale features
        X_scaled = scaler.transform(X)
        
        # Make prediction
        prediction = model.predict(X_scaled)[0]
        probabilities = model.predict_proba(X_scaled)[0]
        
        # Map to risk categories
        classes = model.classes_
        prob_dict = {cls: float(prob) for cls, prob in zip(classes, probabilities)}
        confidence = float(max(probabilities))
        
        return prediction, confidence, prob_dict, None
    
    except Exception as e:
        return None, None, None, str(e)

def get_recommendations(risk_level):
    """
    Get personalized recommendations based on risk level.
    
    Parameters:
        risk_level: Predicted risk level (High, Medium, Low)
        
    Returns:
        Dictionary with recommendations
    """
    recommendations = {
        "High": {
            "actions": [
                "🎯 Schedule intervention meeting with school counselor",
                "📚 Recommend intensive tutoring services",
                "📋 Monitor attendance closely (weekly check-ins)",
                "👥 Connect with peer mentoring programs",
                "📞 Establish regular parent/guardian communication"
            ],
            "priority": "URGENT",
            "timeline": "Within 1 week",
            "color_class": "high-risk-card" # This class will be used for styling in the display
        },
        "Medium": {
            "actions": [
                "📅 Check in bi-weekly with student and teachers",
                "👫 Participate in study groups",
                "📊 Review progress at mid-semester",
                "💡 Receive targeted academic support in weak areas",
                "🎓 Discuss academic goals and study strategies with peers"
            ],
            "priority": "MODERATE",
            "timeline": "Within 2 weeks",
            "color_class": "medium-risk-card"
        },
        "Low": {
            "actions": [
                "✅ Student is on track - continue current efforts",
                "🌟 Encourage continued engagement and effort",
                "🤝 Consider peer tutoring opportunities (as mentor)",
                "🎯 Explore advanced or enrichment programs",
                "📈 Set higher academic goals for growth"
            ],
            "priority": "MONITOR",
            "timeline": "Regular monitoring",
            "color_class": "low-risk-card"
        }
    }
    
    return recommendations.get(risk_level, {})

def get_model_feature_names():
    """
    Returns the ordered list of feature names that the model expects.
    This is derived from the internal column_order of create_feature_dataframe.
    """
    # Call create_feature_dataframe with empty inputs to get the column order
    return create_feature_dataframe({}).columns.tolist()


def map_feature_name(feature_name):
    """
    Maps technical feature names to more human-readable and consolidated labels.
    """
    # Consolidated mappings for one-hot encoded features
    if feature_name.startswith('Mjob_'):
        return "Mother's Job"
    if feature_name.startswith('Fjob_'):
        return "Father's Job"
    if feature_name.startswith('reason_'):
        return "Reason for School"
    if feature_name.startswith('guardian_'):
        return "Guardian"
    
    # Specific mappings for other one-hot encoded binary features
    mapping = {
        'failures': 'Past Failures',
        'higher_yes': 'Wants Higher Education',
        'subject_portuguese': 'Subject', # Consolidated to just 'Subject'
        'schoolsup_yes': 'School Support',
        'school_MS': 'School Type', # Consolidated to 'School Type'
        'age': 'Age',
        'Medu': "Mother's Education",
        'Fedu': "Father's Education",
        'traveltime': 'Travel Time to School',
        'studytime': 'Study Time',
        'famrel': 'Family Relations',
        'freetime': 'Free Time',
        'goout': 'Going Out Frequency',
        'Dalc': 'Weekday Alcohol Use',
        'Walc': 'Weekend Alcohol Use',
        'health': 'Health Status',
        'absences': 'Absences',
        'sex_M': 'Sex', # Consolidated to 'Sex'
        'address_U': 'Address Type', # Consolidated to 'Address Type'
        'famsize_LE3': 'Family Size', # Consolidated to 'Family Size'
        'Pstatus_T': 'Parental Status', # Consolidated to 'Parental Status'
        'paid_yes': 'Paid Classes',
        'activities_yes': 'School Activities',
        'nursery_yes': 'Nursery School Attended',
        'internet_yes': 'Internet Access',
        'romantic_yes': 'In a Romantic Relationship',
        'parent_edu_avg': 'Average Parent Education',
        'total_alcohol': 'Total Alcohol Consumption',
        'study_to_failure_ratio': 'Study/Failure Ratio',
        'high_absence': 'High Absences (>10)',
        'both_parents_educated': 'Both Parents Highly Educated',
        'social_score': 'Social Activity Score',
        'total_support': 'Has Any Support'
    }
    # Return mapped name or original if not found (with basic cleanup)
    return mapping.get(feature_name, feature_name.replace('_', ' ').title())


def get_feature_importance_explanation(model, form_inputs):
    """
    Get feature importance (coefficients for Logistic Regression) and create explanation of prediction.
    
    Parameters:
        model: Trained LogisticRegression model
        form_inputs: Dictionary of raw user inputs from the Streamlit form
        
    Returns:
        pd.DataFrame: Top 5 features with their absolute coefficients (importance) and student's input values.
    """
    try:
        # Get the feature names in the correct order using the new helper function
        model_feature_names = get_model_feature_names() 
        
        lr_coefs = np.mean(np.abs(model.coef_), axis=0)
        
        feature_importance_df = pd.DataFrame({
            'Feature': model_feature_names,
            'Importance': lr_coefs,
            'Student Raw Value': [form_inputs.get(f.split('_')[0], 0) if '_' in f and f.split('_')[0] in form_inputs else form_inputs.get(f, 0) for f in model_feature_names]
        }).sort_values('Importance', ascending=False)
        
        # Apply human-readable names and refine student values for display
        mapped_features = []
        refined_student_values = []
        
        for _, row in feature_importance_df.iterrows():
            original_feature = row['Feature']
            raw_input_value = row['Student Raw Value'] # This is the value from the form input
            
            mapped_name = map_feature_name(original_feature)
            mapped_features.append(mapped_name)
            
            # Refine student value for display based on original feature name
            # This logic needs to be robust for all types of features
            if original_feature.endswith('_yes'):
                refined_student_values.append('Yes' if raw_input_value == 'yes' else 'No')
            elif original_feature.startswith('school_') or original_feature.startswith('sex_') or original_feature.startswith('address_') or original_feature.startswith('famsize_') or original_feature.startswith('Pstatus_') or original_feature.startswith('subject_'):
                # For original categorical features like 'school_MS', etc.
                # Check if the original form input matches the one-hot encoded '1'
                original_form_key = original_feature.split('_')[0]
                if form_inputs.get(original_form_key) == original_feature.split('_')[-1]:
                    refined_student_values.append(form_inputs.get(original_form_key))
                else:
                    refined_student_values.append(form_inputs.get(original_form_key, 'N/A'))
            elif original_feature.startswith('Mjob_') or original_feature.startswith('Fjob_') or original_feature.startswith('reason_') or original_feature.startswith('guardian_'):
                original_form_key = original_feature.split('_')[0]
                if form_inputs.get(original_form_key) == original_feature.split('_')[-1]:
                    refined_student_values.append(form_inputs.get(original_form_key))
                else:
                    refined_student_values.append(form_inputs.get(original_form_key, 'N/A'))
            else:
                refined_student_values.append(raw_input_value)
                
        feature_importance_df['Feature'] = mapped_features
        feature_importance_df['Student Value'] = refined_student_values
        
        # Drop duplicates in 'Feature' column after mapping (e.g., multiple Mjob_ features become 'Mother's Job')
        feature_importance_df = feature_importance_df.groupby('Feature').agg({
            'Importance': 'max',
            'Student Value': 'first' 
        }).reset_index().sort_values('Importance', ascending=False)
        
        return feature_importance_df.head(5)
    except Exception as e:
        st.error(f"Error calculating feature importance for explanation: {e}")
        return None

def create_feature_importance_chart(top_features_df):
    """
    Create a visual chart for feature importance with minimalistic dark styling.
    
    Parameters:
        top_features_df: DataFrame with top features (already human-readable), their importance, and student values.
        
    Returns:
        Matplotlib figure
    """
    plt.style.use('dark_background') # Apply dark theme
    
    fig, ax = plt.subplots(figsize=(17, 6))# Adjusted size for better fit in Streamlit
    
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(top_features_df)))
    # Slimmer bars, no edge color, no linewidth
    bars = ax.barh(top_features_df['Feature'], top_features_df['Importance'], height=0.5, color=colors, edgecolor='none', linewidth=0)
    
    # Add importance score labels on bars with thinner font
    for i, (bar, importance) in enumerate(zip(bars, top_features_df['Importance'])):
        ax.text(importance + 0.005, i, f'{importance:.3f}', va='center', fontweight='light', fontsize=12, color='#f0f2f6')
    
    ax.set_xlabel('Absolute Coefficient Value (Importance)', fontsize=14, fontweight='light', color='#bbbbbb')
    ax.set_title('Top 5 Factors Influencing Prediction', fontsize=16, fontweight='light', pad=10, color='#f0f2f6')
    ax.tick_params(axis='y', labelsize=10, colors='#f0f2f6')
    ax.tick_params(axis='x', labelsize=9, colors='#bbbbbb')
    ax.grid(axis='x', alpha=0.2, linestyle='--', color='#555555')
    
    ax.invert_yaxis() # Invert y-axis to have the most important feature at the top
    
    # Set background color of the plot area
    ax.set_facecolor('#1e1e1e') # Darker plot area background
    fig.patch.set_facecolor('#0e1117') # Match Streamlit's main background
    
    plt.tight_layout()
    return fig


# ============================================================================
# MAIN APP
# ============================================================================

st.title("🎓 Student Academic Performance Predictor")
st.markdown("---")

# Load model
model, scaler = load_model_and_scaler()

if model is None or scaler is None:
    st.stop()

st.success("✅ Model loaded successfully!")

st.subheader("📋 Student Information")
st.write("Fill out the form below to predict student risk level.")

with st.form("prediction_form"):
    
    # Demographics
    with st.expander("📍 Demographics", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            school = st.selectbox("School", ["GP", "MS"])
            sex = st.selectbox("Sex", ["F", "M"])
        with col2:
            age = st.number_input("Age", min_value=15, max_value=22, value=17)
            address = st.selectbox("Address", ["U", "R"], help="U=Urban, R=Rural")
        with col3:
            famsize = st.selectbox("Family Size", ["LE3", "GT3"], help="LE3=≤3, GT3=>3")
            Pstatus = st.selectbox("Parent Status", ["T", "A"], help="T=Together, A=Apart")
    
    # Family
    with st.expander("👨‍👩‍👧‍👦 Family Background"):
        col1, col2 = st.columns(2)
        with col1:
            Medu = st.slider("Mother's Education (0–4)", 0, 4, 2)
            Fedu = st.slider("Father's Education (0–4)", 0, 4, 2)
            Mjob = st.selectbox("Mother's Job", ["at_home", "health", "other", "services", "teacher"])
        with col2:
            Fjob = st.selectbox("Father's Job", ["at_home", "health", "other", "services", "teacher"])
            guardian = st.selectbox("Guardian", ["mother", "father", "other"])
            famsup = st.selectbox("Family Support", ["yes", "no"])
    
    # School
    with st.expander("🏫 School Information"):
        col1, col2 = st.columns(2)
        with col1:
            reason = st.selectbox("Reason for School", ["home", "reputation", "course", "other"])
            traveltime = st.slider("Travel Time (1–4)", 1, 4, 2)
            studytime = st.slider("Study Time (1–4)", 1, 4, 2)
            failures = st.number_input("Past Failures", 0, 4, 0)
        with col2:
            schoolsup = st.selectbox("School Support", ["yes", "no"])
            paid = st.selectbox("Paid Classes", ["yes", "no"])
            activities = st.selectbox("Activities", ["yes", "no"])
            nursery = st.selectbox("Nursery School", ["yes", "no"])
            higher = st.selectbox("Wants Higher Ed", ["yes", "no"])
    
    # Social
    with st.expander("🎉 Social & Lifestyle"):
        col1, col2 = st.columns(2)
        with col1:
            internet = st.selectbox("Internet", ["yes", "no"])
            romantic = st.selectbox("Romantic", ["yes", "no"])
            famrel = st.slider("Family Relations (1–5)", 1, 5, 4)
            freetime = st.slider("Free Time (1–5)", 1, 5, 3)
        with col2:
            goout = st.slider("Going Out (1–5)", 1, 5, 3)
            Dalc = st.slider("Weekday Alcohol (1–5)", 1, 5, 1)
            Walc = st.slider("Weekend Alcohol (1–5)", 1, 5, 1)
    
    # Health
    with st.expander("🏥 Health"):
        col1, col2 = st.columns(2)
        with col1:
            health = st.slider("Health (1–5)", 1, 5, 3)
        with col2:
            absences = st.number_input("Absences", 0, 93, 0)
    
    # Subject
    with st.expander("📚 Subject"):
        subject = st.selectbox("Subject", ["math", "portuguese"])
    
    submitted = st.form_submit_button("🔮 Predict Student Risk Level", use_container_width=True)

# Handle prediction
if submitted:
    if age <= 0:
        st.error("❌ Age must be greater than 0")
    else:
        # Prepare inputs
        form_inputs = {
            'school': school, 'sex': sex, 'age': age, 'address': address,
            'famsize': famsize, 'Pstatus': Pstatus, 'Medu': Medu, 'Fedu': Fedu,
            'Mjob': Mjob, 'Fjob': Fjob, 'reason': reason, 'guardian': guardian,
            'traveltime': traveltime, 'studytime': studytime, 'failures': failures,
            'schoolsup': schoolsup, 'famsup': famsup, 'paid': paid,
            'activities': activities, 'nursery': nursery, 'higher': higher,
            'internet': internet, 'romantic': romantic, 'famrel': famrel,
            'freetime': freetime, 'goout': goout, 'Dalc': Dalc, 'Walc': Walc,
            'health': health, 'absences': absences, 'subject': subject
        }
        
        with st.spinner("🔍 Analyzing student data..."):
            risk, confidence, probs, error = make_prediction(form_inputs, model, scaler)
            
            if error:
                st.error(f"❌ {error}")
            else:
                st.markdown("---")
                st.subheader("📊 Prediction Results")
                
                # Display risk with emoji
                emojis = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
                emoji = emojis.get(risk, '⚪')
                
                st.markdown(f"## {emoji} Risk Level: **{risk}**")
                st.markdown(f"**Confidence:** {confidence*100:.1f}%")
                
                # Probabilities
                st.write("### Risk Probabilities")
                for level in ['High', 'Medium', 'Low']:
                    prob = probs.get(level, 0)
                    st.write(f"**{level} Risk:** {prob*100:.1f}%")
                    st.progress(prob)
                
                st.markdown("---")
                st.markdown("## 💡 Personalized Recommendations")
                
                # Get recommendations based on the predicted risk level
                rec_data = get_recommendations(risk) # Assuming 'risk' is defined from prediction
                
                # Display priority and timeline in a minimalistic way
                col_rec1, col_rec2 = st.columns(2)
                with col_rec1:
                    st.markdown(f"**Priority Level:** <span style='color: #bbbbbb;'>{rec_data['priority']}</span>", unsafe_allow_html=True)
                with col_rec2:
                    st.markdown(f"**Action Timeline:** <span style='color: #bbbbbb;'>{rec_data['timeline']}</span>", unsafe_allow_html=True)
                
                # Display action items
                st.markdown("### Recommended Actions:")
                st.markdown(f"<div class='recommendation-box'>", unsafe_allow_html=True) # Use the existing recommendation-box class
                for i, action in enumerate(rec_data["actions"], 1):
                    st.markdown(f"<p style='margin: 0; padding: 5px 0; font-weight: light;'>{i}. {action}</p>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

                # Optional: Action Progress Tracker (kept minimalistic)
                st.markdown("### 📌 Action Progress Tracker:")
                for action in rec_data["actions"]:
                    st.checkbox(action, value=False)

                          # --- Explain Prediction Section (Task C) ---
                st.markdown("---")
                st.markdown("## 🔍 Explain Prediction")
                st.markdown("### Top Factors Influencing This Assessment:")
                
                # Call get_feature_importance_explanation (no explicit feature_names argument needed)
                top_features = get_feature_importance_explanation(model, form_inputs) 
                
                if top_features is not None:
                    col_exp1, col_exp2 = st.columns([1.5, 1])
                    
                    with col_exp1:
                        fig_imp = create_feature_importance_chart(top_features)
                        st.pyplot(fig_imp)
                        plt.close(fig_imp) # Close figure to prevent memory issues
                    
                    with col_exp2:
                        st.markdown("<h3 style='font-weight: light; color: #f0f2f6;'>Student's Values:</h3>", unsafe_allow_html=True) # Styled header
                        for idx, row in top_features.iterrows():
                            st.write(f"**{row['Feature']}**") # Feature name is now human-readable
                            # Display value, handle numeric formatting
                            if isinstance(row['Student Value'], (int, float)):
                                st.metric("Value", f"{row['Student Value']:.2f}", label_visibility="collapsed")
                            else:
                                st.metric("Value", str(row['Student Value']), label_visibility="collapsed")
                    
                    st.markdown("""
                    #### 📖 What This Means:
                    <p style='font-weight: light;'>The factors listed above are the most important predictors of student risk in our model.
                    A higher absolute coefficient value means that feature has a stronger influence on the prediction.
                    A positive coefficient generally indicates the feature increases the likelihood of a higher risk category, 
                    while a negative coefficient decreases it.</p>
                    """, unsafe_allow_html=True)
                
                # This is where your original Debug section would follow, if you still want it.
                # For now, I'm assuming you want the recommendations here.
                # Debug
                with st.expander("🔍 Debug: Features"):
                    # Assuming create_feature_dataframe and form_inputs are available
                    df_debug = create_feature_dataframe(form_inputs) # Pass feature_names here
                    st.dataframe(df_debug)
                    st.write(f"Shape: {df_debug.shape}")