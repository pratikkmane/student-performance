import streamlit as st
import pandas as pd
import numpy as np
import pickle
from pathlib import Path

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
                st.info("👉 **Emmanuel:** Add recommendations here (Task C)")
                
                # Debug
                with st.expander("🔍 Debug: Features"):
                    df = create_feature_dataframe(form_inputs)
                    st.dataframe(df)
                    st.write(f"Shape: {df.shape}")
