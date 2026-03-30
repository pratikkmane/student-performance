import streamlit as st

st.set_page_config(page_title="Student Performance Predictor", layout="wide")

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

st.title("Student Performance Predictor")

st.write("Fill out the form below to predict student risk level.")

with st.form("prediction_form"):

    st.header("Student Information")

    # Demographics
    with st.expander("Demographics"):
        school = st.selectbox("School", ["GP", "MS"])
        sex = st.selectbox("Sex", ["F", "M"])
        age = st.number_input("Age", min_value=15, max_value=22, value=16, help="Student age (15–22)")
        address = st.selectbox("Address", ["U", "R"])
        famsize = st.selectbox("Family Size", ["LE3", "GT3"])
        Pstatus = st.selectbox("Parent Status", ["T", "A"])

    # Family
    with st.expander("Family Background"):
        Medu = st.slider("Mother Education (0–4)", 0, 4, 2)
        Fedu = st.slider("Father Education (0–4)", 0, 4, 2)

    # School
    with st.expander("School Information"):
        reason = st.selectbox("Reason", ["home", "reputation", "course", "other"])
        traveltime = st.slider("Travel Time (1–4)", 1, 4, 2)
        studytime = st.slider("Study Time (1–4)", 1, 4, 2, help="1 = low, 4 = high study time")
        failures = st.number_input("Failures", 0, 5, 0, help="Number of past class failures")

    # Social
    with st.expander("Social & Behavior"):
        goout = st.slider("Going Out (1–5)", 1, 5, 3, help="1 = rarely, 5 = very frequent")
        Dalc = st.slider("Weekday Alcohol (1–5)", 1, 5, 1)
        Walc = st.slider("Weekend Alcohol (1–5)", 1, 5, 2)

    # Health
    with st.expander("Health"):
        health = st.slider("Health (1–5)", 1, 5, 3)
        absences = st.number_input("Absences", 0, 100, 5)

    # Subject
    with st.expander("Subject"):
        subject = st.selectbox("Subject", ["math", "portuguese"])

    submit = st.form_submit_button("Predict Student Risk")

if submit:
    if age <= 0:
        st.error("Age must be greater than 0")
    else:
        st.success("Form submitted successfully!")