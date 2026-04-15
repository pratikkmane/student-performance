import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
from pathlib import Path

# --- Page Config ---
st.set_page_config(page_title="What-If Analysis", page_icon="🔄", layout="wide")
st.title("🔄 What-If Analysis Tool")
st.markdown("Explore how changes in student behavior could affect their predicted risk level.")

# ============================================================================
# LOAD CUSTOM CSS
# ============================================================================

def load_css():
    """Load custom CSS styling."""
    css_file = Path(__file__).parent.parent / "assets" / "style.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ============================================================================
# SIDEBAR BRANDING
# ============================================================================

with st.sidebar:
    st.markdown("""
        <div class="logo-container">
            <h1 style="color: white; font-size: 1.5rem; margin-bottom: 0;">🎓</h1>
            <h2 style="color: white; font-size: 1.2rem; margin-top: 0;">Student Performance</h2>
            <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">AI-Powered Risk Predictor</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 👥 Team")
    st.markdown("""
    <small style="color: rgba(255,255,255,0.9);">
    <b>Lead:</b> Pratik Mane<br>
    <b>Members:</b> Emmanuel Atilola, Yugant Nagralawala, Hamza Almani<br>
    <b>Advisor:</b> Prof. Leon Johnson
    </small>
    """, unsafe_allow_html=True)
    st.markdown("---")

# --- Load Model ---
@st.cache_resource
def load_model():
    return joblib.load("models/random_forest.pkl")

try:
    model = load_model()
except FileNotFoundError:
    st.error("Model file not found. Make sure 'models/random_forest.pkl' exists.")
    st.stop()

# --- Exact 43 features the model expects (in order) ---
EXPECTED_FEATURES = [
    'age', 'Medu', 'Fedu', 'traveltime', 'studytime', 'failures',
    'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences',
    'school_MS', 'sex_M', 'address_U', 'famsize_LE3', 'Pstatus_T',
    'Mjob_health', 'Mjob_other', 'Mjob_services', 'Mjob_teacher',
    'Fjob_health', 'Fjob_other', 'Fjob_services', 'Fjob_teacher',
    'reason_home', 'reason_other', 'reason_reputation',
    'guardian_mother', 'guardian_other',
    'schoolsup_yes', 'famsup_yes', 'paid_yes', 'activities_yes',
    'nursery_yes', 'higher_yes', 'internet_yes', 'romantic_yes',
    'subject_portuguese',
    'parent_edu_avg', 'total_alcohol', 'has_support'
]

RISK_COLORS = {"High": "#FF4B4B", "Medium": "#FFA500", "Low": "#00CC66"}


def engineer_features(profile):
    """Convert raw profile dict into the exact 43-feature DataFrame the model expects."""
    row = {}

    # 1-13: Numeric features passed through directly
    row['age'] = profile['age']
    row['Medu'] = profile['Medu']
    row['Fedu'] = profile['Fedu']
    row['traveltime'] = profile['traveltime']
    row['studytime'] = profile['studytime']
    row['failures'] = profile['failures']
    row['famrel'] = profile['famrel']
    row['freetime'] = profile['freetime']
    row['goout'] = profile['goout']
    row['Dalc'] = profile['Dalc']
    row['Walc'] = profile['Walc']
    row['health'] = profile['health']
    row['absences'] = profile['absences']

    # 14-18: Binary dummies (drop-first encoded)
    row['school_MS'] = 1 if profile['school'] == 'MS' else 0
    row['sex_M'] = 1 if profile['sex'] == 'M' else 0
    row['address_U'] = 1 if profile['address'] == 'U' else 0
    row['famsize_LE3'] = 1 if profile['famsize'] == 'LE3' else 0
    row['Pstatus_T'] = 1 if profile['Pstatus'] == 'T' else 0

    # 19-22: Mjob dummies (at_home is the dropped base)
    row['Mjob_health'] = 1 if profile['Mjob'] == 'health' else 0
    row['Mjob_other'] = 1 if profile['Mjob'] == 'other' else 0
    row['Mjob_services'] = 1 if profile['Mjob'] == 'services' else 0
    row['Mjob_teacher'] = 1 if profile['Mjob'] == 'teacher' else 0

    # 23-26: Fjob dummies (at_home is the dropped base)
    row['Fjob_health'] = 1 if profile['Fjob'] == 'health' else 0
    row['Fjob_other'] = 1 if profile['Fjob'] == 'other' else 0
    row['Fjob_services'] = 1 if profile['Fjob'] == 'services' else 0
    row['Fjob_teacher'] = 1 if profile['Fjob'] == 'teacher' else 0

    # 27-29: Reason dummies (course is the dropped base)
    row['reason_home'] = 1 if profile['reason'] == 'home' else 0
    row['reason_other'] = 1 if profile['reason'] == 'other' else 0
    row['reason_reputation'] = 1 if profile['reason'] == 'reputation' else 0

    # 30-31: Guardian dummies (father is the dropped base)
    row['guardian_mother'] = 1 if profile['guardian'] == 'mother' else 0
    row['guardian_other'] = 1 if profile['guardian'] == 'other' else 0

    # 32-39: Binary yes/no dummies
    row['schoolsup_yes'] = profile['schoolsup']
    row['famsup_yes'] = profile['famsup']
    row['paid_yes'] = profile['paid']
    row['activities_yes'] = profile['activities']
    row['nursery_yes'] = profile['nursery']
    row['higher_yes'] = profile['higher']
    row['internet_yes'] = profile['internet']
    row['romantic_yes'] = profile['romantic']

    # 40: Subject
    row['subject_portuguese'] = profile['subject_portuguese']

    # 41-43: Engineered features
    row['parent_edu_avg'] = (profile['Medu'] + profile['Fedu']) / 2
    row['total_alcohol'] = profile['Dalc'] + profile['Walc']
    row['has_support'] = 1 if (profile['schoolsup'] + profile['famsup'] + profile['paid']) > 0 else 0

    df = pd.DataFrame([row])
    return df[EXPECTED_FEATURES]


def get_prediction(profile):
    features_df = engineer_features(profile)
    probabilities = model.predict_proba(features_df)[0]
    predicted_class = model.predict(features_df)[0]
    probs_dict = {label: prob for label, prob in zip(model.classes_, probabilities)}
    return {"class": predicted_class, "probabilities": probs_dict}


# --- Default Student Profile ---
DEFAULT_PROFILE = {
    "school": "GP", "sex": "F", "age": 17, "address": "U",
    "famsize": "GT3", "Pstatus": "T", "Medu": 2, "Fedu": 2,
    "Mjob": "other", "Fjob": "other", "reason": "course", "guardian": "mother",
    "traveltime": 2, "studytime": 2, "failures": 0,
    "schoolsup": 0, "famsup": 1, "paid": 0, "activities": 0,
    "nursery": 1, "higher": 1, "internet": 1, "romantic": 0,
    "famrel": 4, "freetime": 3, "goout": 3,
    "Dalc": 1, "Walc": 1, "health": 3, "absences": 4,
    "subject_portuguese": 0,
}

if "current_profile" not in st.session_state:
    st.session_state.current_profile = DEFAULT_PROFILE.copy()


# ========================================
# SIDEBAR - Baseline Student Profile
# ========================================
st.sidebar.header("📋 Set Student Profile")

profile = st.session_state.current_profile.copy()

with st.sidebar.expander("Demographics", expanded=False):
    profile["school"] = st.selectbox("School", ["GP", "MS"], index=["GP", "MS"].index(profile["school"]))
    profile["sex"] = st.selectbox("Sex", ["F", "M"], index=["F", "M"].index(profile["sex"]))
    profile["age"] = st.slider("Age", 15, 22, profile["age"])
    profile["address"] = st.selectbox("Address", ["U", "R"], index=["U", "R"].index(profile["address"]))
    profile["famsize"] = st.selectbox("Family Size", ["LE3", "GT3"], index=["LE3", "GT3"].index(profile["famsize"]))
    profile["Pstatus"] = st.selectbox("Parent Status", ["T", "A"], index=["T", "A"].index(profile["Pstatus"]))

with st.sidebar.expander("Family & Background", expanded=False):
    profile["Medu"] = st.slider("Mother's Education (0-4)", 0, 4, profile["Medu"])
    profile["Fedu"] = st.slider("Father's Education (0-4)", 0, 4, profile["Fedu"])
    profile["Mjob"] = st.selectbox("Mother's Job", ["teacher", "health", "services", "at_home", "other"],
                                   index=["teacher", "health", "services", "at_home", "other"].index(profile["Mjob"]))
    profile["Fjob"] = st.selectbox("Father's Job", ["teacher", "health", "services", "at_home", "other"],
                                   index=["teacher", "health", "services", "at_home", "other"].index(profile["Fjob"]))
    profile["guardian"] = st.selectbox("Guardian", ["mother", "father", "other"],
                                      index=["mother", "father", "other"].index(profile["guardian"]))
    profile["reason"] = st.selectbox("Reason for School", ["home", "reputation", "course", "other"],
                                     index=["home", "reputation", "course", "other"].index(profile["reason"]))

with st.sidebar.expander("Other Attributes", expanded=False):
    profile["traveltime"] = st.slider("Travel Time (1-4)", 1, 4, profile["traveltime"])
    profile["failures"] = st.slider("Past Failures (0-4)", 0, 4, profile["failures"])
    profile["nursery"] = 1 if st.selectbox("Nursery", ["No", "Yes"], index=profile["nursery"]) == "Yes" else 0
    profile["higher"] = 1 if st.selectbox("Wants Higher Ed", ["No", "Yes"], index=profile["higher"]) == "Yes" else 0
    profile["internet"] = 1 if st.selectbox("Internet at Home", ["No", "Yes"], index=profile["internet"]) == "Yes" else 0
    profile["romantic"] = 1 if st.selectbox("Romantic Relationship", ["No", "Yes"], index=profile["romantic"]) == "Yes" else 0
    profile["activities"] = 1 if st.selectbox("Activities", ["No", "Yes"], index=profile["activities"]) == "Yes" else 0
    profile["famrel"] = st.slider("Family Relationship (1-5)", 1, 5, profile["famrel"])
    profile["freetime"] = st.slider("Free Time (1-5)", 1, 5, profile["freetime"])
    profile["subject_portuguese"] = 1 if st.selectbox("Subject", ["Math", "Portuguese"], index=profile["subject_portuguese"]) == "Portuguese" else 0

st.session_state.current_profile = profile


# ========================================
# MAIN - Two Column Layout
# ========================================
col_current, col_modified = st.columns(2)

# --- Left: Current Profile ---
with col_current:
    st.subheader("📊 Current Prediction")
    current_pred = get_prediction(profile)
    current_class = current_pred["class"]
    current_probs = current_pred["probabilities"]

    color = RISK_COLORS.get(current_class, "#888")
    st.markdown(
        f'<div style="background-color:{color}; padding:20px; border-radius:10px; text-align:center;">'
        f'<h2 style="color:white; margin:0;">{current_class} Risk</h2></div>',
        unsafe_allow_html=True,
    )
    st.markdown("")

    st.markdown("**Current Changeable Features:**")
    info = {
        "Study Time": profile["studytime"],
        "Absences": profile["absences"],
        "School Support": "Yes" if profile["schoolsup"] else "No",
        "Family Support": "Yes" if profile["famsup"] else "No",
        "Paid Classes": "Yes" if profile["paid"] else "No",
        "Workday Alcohol": profile["Dalc"],
        "Weekend Alcohol": profile["Walc"],
        "Going Out": profile["goout"],
        "Health": profile["health"],
    }
    for k, v in info.items():
        st.markdown(f"- **{k}:** {v}")

# --- Right: What-If Scenario ---
with col_modified:
    st.subheader("🔧 What-If Scenario")
    st.markdown("Adjust sliders to simulate interventions:")

    modified = profile.copy()

    modified["studytime"] = st.slider("📚 Study Time", 1, 4, profile["studytime"], key="wif_study",
                                      help="1: <2hrs, 2: 2-5hrs, 3: 5-10hrs, 4: >10hrs")
    modified["absences"] = st.slider("📅 Absences", 0, 93, profile["absences"], key="wif_abs")
    modified["schoolsup"] = 1 if st.toggle("🏫 Extra School Support", value=bool(profile["schoolsup"]), key="wif_ss") else 0
    modified["famsup"] = 1 if st.toggle("👨‍👩‍👧 Family Support", value=bool(profile["famsup"]), key="wif_fs") else 0
    modified["paid"] = 1 if st.toggle("💰 Paid Classes", value=bool(profile["paid"]), key="wif_paid") else 0
    modified["Dalc"] = st.slider("🍺 Workday Alcohol", 1, 5, profile["Dalc"], key="wif_dalc")
    modified["Walc"] = st.slider("🍻 Weekend Alcohol", 1, 5, profile["Walc"], key="wif_walc")
    modified["goout"] = st.slider("🚶 Going Out", 1, 5, profile["goout"], key="wif_goout")
    modified["health"] = st.slider("❤️ Health", 1, 5, profile["health"], key="wif_health")

    if st.button("🔄 Reset to Original", use_container_width=True):
        st.session_state.current_profile = DEFAULT_PROFILE.copy()
        st.rerun()

    mod_pred = get_prediction(modified)
    mod_class = mod_pred["class"]
    mod_probs = mod_pred["probabilities"]

    mod_color = RISK_COLORS.get(mod_class, "#888")
    st.markdown(
        f'<div style="background-color:{mod_color}; padding:20px; border-radius:10px; text-align:center;">'
        f'<h2 style="color:white; margin:0;">{mod_class} Risk</h2></div>',
        unsafe_allow_html=True,
    )


# ========================================
# RISK CHANGE INDICATOR
# ========================================
st.markdown("---")
risk_order = {"High": 2, "Medium": 1, "Low": 0}
if current_class != mod_class:
    if risk_order[mod_class] < risk_order[current_class]:
        st.success(f"✅ **Risk level improved:** {current_class} → {mod_class}")
    else:
        st.error(f"⚠️ **Risk level worsened:** {current_class} → {mod_class}")
else:
    st.info(f"ℹ️ **Risk level unchanged:** {current_class} — Try adjusting more features.")


# ========================================
# COMPARISON CHARTS
# ========================================
st.subheader("📈 Impact Visualization")
viz_col1, viz_col2 = st.columns(2)

classes = list(current_probs.keys())
current_vals = [current_probs[c] * 100 for c in classes]
modified_vals = [mod_probs[c] * 100 for c in classes]

with viz_col1:
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name="Current", x=classes, y=current_vals,
        marker_color=["#FF6B6B", "#51D88A", "#FFB84D"], opacity=0.7,
        text=[f"{v:.1f}%" for v in current_vals], textposition="auto",
    ))
    fig_bar.add_trace(go.Bar(
        name="What-If", x=classes, y=modified_vals,
        marker_color=["#CC0000", "#008844", "#CC8400"],
        text=[f"{v:.1f}%" for v in modified_vals], textposition="auto",
    ))
    fig_bar.update_layout(
        title="Probability Comparison", barmode="group",
        yaxis_title="Probability (%)", yaxis_range=[0, 100], height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with viz_col2:
    shifts = {c: (mod_probs[c] - current_probs[c]) * 100 for c in classes}
    bar_colors = []
    for c, s in shifts.items():
        if c == "High":
            bar_colors.append("#00CC66" if s <= 0 else "#FF4B4B")
        elif c == "Low":
            bar_colors.append("#00CC66" if s >= 0 else "#FF4B4B")
        else:
            bar_colors.append("#FFB84D")

    fig_shift = go.Figure(go.Bar(
        x=list(shifts.keys()), y=list(shifts.values()),
        marker_color=bar_colors,
        text=[f"{s:+.1f}%" for s in shifts.values()], textposition="auto",
    ))
    fig_shift.update_layout(
        title="Probability Shift (Current → What-If)",
        yaxis_title="Change (%)", height=400,
        shapes=[dict(type="line", x0=-0.5, x1=2.5, y0=0, y1=0, line=dict(color="gray", dash="dash"))],
    )
    st.plotly_chart(fig_shift, use_container_width=True)


# ========================================
# INTERPRETATION TEXT
# ========================================
st.markdown("---")
st.subheader("💡 Interpretation")

changes = []
if modified["studytime"] != profile["studytime"]:
    d = "increases" if modified["studytime"] > profile["studytime"] else "decreases"
    changes.append(f"📚 If study time **{d} from {profile['studytime']} to {modified['studytime']}**, this could shift academic engagement and predicted risk.")

if modified["absences"] != profile["absences"]:
    diff = profile["absences"] - modified["absences"]
    if diff > 0:
        changes.append(f"📅 **Reducing absences by {diff} days** (from {profile['absences']} to {modified['absences']}) could improve the prediction.")
    else:
        changes.append(f"📅 **Increasing absences by {abs(diff)} days** would likely worsen the prediction.")

if modified["Dalc"] != profile["Dalc"] or modified["Walc"] != profile["Walc"]:
    old_t = profile["Dalc"] + profile["Walc"]
    new_t = modified["Dalc"] + modified["Walc"]
    if new_t < old_t:
        changes.append(f"🍺 **Reducing total alcohol from {old_t} to {new_t}** could lower the risk profile.")
    elif new_t > old_t:
        changes.append(f"🍺 **Increasing total alcohol** would likely raise the risk level.")

if modified["schoolsup"] != profile["schoolsup"]:
    changes.append("🏫 **Adding school support** could help reduce risk." if modified["schoolsup"] else "🏫 **Removing school support** may increase risk.")

if modified["paid"] != profile["paid"]:
    changes.append("💰 **Enrolling in paid classes** could provide additional support." if modified["paid"] else "💰 **Dropping paid classes** may negatively affect performance.")

if modified["goout"] != profile["goout"] and modified["goout"] < profile["goout"]:
    changes.append(f"🚶 **Reducing going out from {profile['goout']} to {modified['goout']}** could help focus on academics.")

if modified["health"] != profile["health"] and modified["health"] > profile["health"]:
    changes.append(f"❤️ **Improving health from {profile['health']} to {modified['health']}** is associated with better outcomes.")

if changes:
    for c in changes:
        st.markdown(c)
else:
    st.markdown("*Adjust the sliders above to see how changes could impact the prediction.*")


# ========================================
# QUICK SCENARIOS
# ========================================
st.markdown("---")
st.subheader("🧪 Quick Scenarios")
st.markdown("Test common intervention strategies:")

s1, s2, s3, s4 = st.columns(4)

with s1:
    if st.button("📚 Max Study", use_container_width=True):
        sc = profile.copy(); sc["studytime"] = 4
        p = get_prediction(sc)
        st.markdown(f"**{p['class']} Risk**")
        for cls, prob in p["probabilities"].items():
            st.markdown(f"- {cls}: {prob*100:.1f}%")

with s2:
    if st.button("🚫 No Alcohol", use_container_width=True):
        sc = profile.copy(); sc["Dalc"] = 1; sc["Walc"] = 1
        p = get_prediction(sc)
        st.markdown(f"**{p['class']} Risk**")
        for cls, prob in p["probabilities"].items():
            st.markdown(f"- {cls}: {prob*100:.1f}%")

with s3:
    if st.button("🌟 Full Support", use_container_width=True):
        sc = profile.copy(); sc["schoolsup"] = 1; sc["famsup"] = 1; sc["paid"] = 1
        p = get_prediction(sc)
        st.markdown(f"**{p['class']} Risk**")
        for cls, prob in p["probabilities"].items():
            st.markdown(f"- {cls}: {prob*100:.1f}%")

with s4:
    if st.button("✨ Best Case", use_container_width=True):
        sc = profile.copy()
        sc["studytime"] = 4; sc["absences"] = 0; sc["Dalc"] = 1; sc["Walc"] = 1
        sc["goout"] = 1; sc["health"] = 5; sc["schoolsup"] = 1; sc["famsup"] = 1; sc["paid"] = 1
        p = get_prediction(sc)
        st.markdown(f"**{p['class']} Risk**")
        for cls, prob in p["probabilities"].items():
            st.markdown(f"- {cls}: {prob*100:.1f}%")

# --- Footer ---
st.markdown("---")
st.caption(
    "⚠️ This tool is for educational exploration only. Predictions are based on a Random Forest model "
    "trained on the UCI Student Performance dataset with ~61% accuracy. Results should not be used "
    "as the sole basis for academic decisions."
)