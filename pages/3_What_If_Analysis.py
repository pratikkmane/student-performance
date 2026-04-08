import streamlit as st
import pandas as pd
import numpy as np
import pickle
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- Page Config ---
st.set_page_config(page_title="What-If Analysis", page_icon="🔄", layout="wide")
st.title("🔄 What-If Analysis Tool")
st.markdown("Explore how changes in student behavior could affect their predicted risk level.")

# --- Load Model ---
# UPDATE THIS PATH to wherever your saved model is
@st.cache_resource
def load_model():
    with open("models/random_forest.pkl", "rb") as f:
        model = pickle.load(f)
    return model

try:
    model = load_model()
except FileNotFoundError:
    st.error("Model file not found. Make sure 'models/random_forest.pkl' exists.")
    st.stop()

# --- Feature Engineering Function ---
# This must match EXACTLY what you did in your notebook
def engineer_features(profile):
    """
    Takes a dict of raw student inputs and returns
    a DataFrame with all 43 engineered features.
    UPDATE THIS to match your actual feature engineering pipeline.
    """
    df = pd.DataFrame([profile])

    # Example engineered features - UPDATE THESE to match your actual pipeline
    df["total_alcohol"] = df["Dalc"] + df["Walc"]
    df["avg_alcohol"] = (df["Dalc"] + df["Walc"]) / 2
    df["parent_edu_avg"] = (df["Medu"] + df["Fedu"]) / 2
    df["parent_edu_max"] = df[["Medu", "Fedu"]].max(axis=1)
    df["parent_edu_diff"] = abs(df["Medu"] - df["Fedu"])
    df["free_vs_study"] = df["freetime"] - df["studytime"]
    df["social_score"] = df["goout"] + df["freetime"]
    df["support_score"] = df["schoolsup"].astype(int) + df["famsup"].astype(int) + df["paid"].astype(int)
    df["risk_behavior"] = df["total_alcohol"] + df["goout"]
    df["engagement_score"] = df["studytime"] + df["activities"].astype(int) + df["higher"].astype(int)
    df["absence_rate"] = df["absences"] / (df["absences"].max() if df["absences"].max() > 0 else 1)
    df["high_alcohol"] = (df["total_alcohol"] >= 6).astype(int)
    df["high_absences"] = (df["absences"] >= 10).astype(int)
    df["no_support"] = ((df["schoolsup"].astype(int) + df["famsup"].astype(int)) == 0).astype(int)

    # Encode categorical variables - UPDATE to match your encoding
    categorical_cols = {
        "school": {"GP": 0, "MS": 1},
        "sex": {"F": 0, "M": 1},
        "address": {"U": 0, "R": 1},
        "famsize": {"LE3": 0, "GT3": 1},
        "Pstatus": {"T": 0, "A": 1},
        "schoolsup": {"no": 0, "yes": 1, False: 0, True: 1, 0: 0, 1: 1},
        "famsup": {"no": 0, "yes": 1, False: 0, True: 1, 0: 0, 1: 1},
        "paid": {"no": 0, "yes": 1, False: 0, True: 1, 0: 0, 1: 1},
        "activities": {"no": 0, "yes": 1, False: 0, True: 1, 0: 0, 1: 1},
        "nursery": {"no": 0, "yes": 1, False: 0, True: 1, 0: 0, 1: 1},
        "higher": {"no": 0, "yes": 1, False: 0, True: 1, 0: 0, 1: 1},
        "internet": {"no": 0, "yes": 1, False: 0, True: 1, 0: 0, 1: 1},
        "romantic": {"no": 0, "yes": 1, False: 0, True: 1, 0: 0, 1: 1},
    }
    for col, mapping in categorical_cols.items():
        if col in df.columns:
            df[col] = df[col].map(mapping).fillna(df[col])

    # One-hot encode nominal columns - UPDATE to match your pipeline
    nominal_cols = ["Mjob", "Fjob", "reason", "guardian"]
    df = pd.get_dummies(df, columns=nominal_cols, drop_first=False)

    # Ensure all expected columns exist (fill missing dummy columns with 0)
    # UPDATE this list to match your actual feature_names.txt
    # expected_features = open("feature_names.txt").read().strip().split("\n")
    # for feat in expected_features:
    #     if feat not in df.columns:
    #         df[feat] = 0
    # df = df[expected_features]

    return df


# --- Default Student Profile ---
DEFAULT_PROFILE = {
    "school": "GP",
    "sex": "F",
    "age": 17,
    "address": "U",
    "famsize": "GT3",
    "Pstatus": "T",
    "Medu": 2,
    "Fedu": 2,
    "Mjob": "other",
    "Fjob": "other",
    "reason": "course",
    "guardian": "mother",
    "traveltime": 2,
    "studytime": 2,
    "failures": 0,
    "schoolsup": 0,
    "famsup": 1,
    "paid": 0,
    "activities": 0,
    "nursery": 1,
    "higher": 1,
    "internet": 1,
    "romantic": 0,
    "famrel": 4,
    "freetime": 3,
    "goout": 3,
    "Dalc": 1,
    "Walc": 1,
    "health": 3,
    "absences": 4,
}

# --- Session State for Reset ---
if "modified_profile" not in st.session_state:
    st.session_state.modified_profile = None
if "current_profile" not in st.session_state:
    st.session_state.current_profile = DEFAULT_PROFILE.copy()


# --- Prediction Helper ---
RISK_LABELS = ["High Risk", "Medium Risk", "Low Risk"]  # UPDATE to match your model's class order
RISK_COLORS = {"High Risk": "#FF4B4B", "Medium Risk": "#FFA500", "Low Risk": "#00CC66"}
THRESHOLD = 0.25  # Your tuned threshold for High Risk


def get_prediction(profile):
    """Run the model on a profile and return class + probabilities."""
    features_df = engineer_features(profile)
    probabilities = model.predict_proba(features_df)[0]

    # Apply threshold tuning for High Risk
    # Assuming class order is [High, Low, Medium] or [High, Medium, Low]
    # UPDATE the index based on your model's model.classes_
    predicted_class = model.predict(features_df)[0]

    return {
        "class": predicted_class,
        "probabilities": {label: prob for label, prob in zip(model.classes_, probabilities)},
    }


# ========================================
# SIDEBAR - Set Current Student Profile
# ========================================
st.sidebar.header("📋 Set Student Profile")
st.sidebar.markdown("Configure the baseline student profile here.")

profile = st.session_state.current_profile.copy()

with st.sidebar.expander("Demographics", expanded=False):
    profile["school"] = st.selectbox("School", ["GP", "MS"], index=["GP", "MS"].index(profile["school"]))
    profile["sex"] = st.selectbox("Sex", ["F", "M"], index=["F", "M"].index(profile["sex"]))
    profile["age"] = st.slider("Age", 15, 22, profile["age"])
    profile["address"] = st.selectbox("Address", ["U", "R"], index=["U", "R"].index(profile["address"]))
    profile["famsize"] = st.selectbox("Family Size", ["LE3", "GT3"], index=["LE3", "GT3"].index(profile["famsize"]))
    profile["Pstatus"] = st.selectbox("Parent Status", ["T", "A"], index=["T", "A"].index(profile["Pstatus"]))

with st.sidebar.expander("Family & Background", expanded=False):
    profile["Medu"] = st.slider("Mother's Education", 0, 4, profile["Medu"])
    profile["Fedu"] = st.slider("Father's Education", 0, 4, profile["Fedu"])
    profile["Mjob"] = st.selectbox("Mother's Job", ["teacher", "health", "services", "at_home", "other"], index=["teacher", "health", "services", "at_home", "other"].index(profile["Mjob"]))
    profile["Fjob"] = st.selectbox("Father's Job", ["teacher", "health", "services", "at_home", "other"], index=["teacher", "health", "services", "at_home", "other"].index(profile["Fjob"]))
    profile["guardian"] = st.selectbox("Guardian", ["mother", "father", "other"], index=["mother", "father", "other"].index(profile["guardian"]))
    profile["reason"] = st.selectbox("Reason for School", ["home", "reputation", "course", "other"], index=["home", "reputation", "course", "other"].index(profile["reason"]))

with st.sidebar.expander("Other Fixed Attributes", expanded=False):
    profile["traveltime"] = st.slider("Travel Time", 1, 4, profile["traveltime"])
    profile["failures"] = st.slider("Past Failures", 0, 4, profile["failures"])
    profile["nursery"] = st.selectbox("Nursery", [0, 1], index=profile["nursery"], format_func=lambda x: "Yes" if x else "No")
    profile["higher"] = st.selectbox("Wants Higher Ed", [0, 1], index=profile["higher"], format_func=lambda x: "Yes" if x else "No")
    profile["internet"] = st.selectbox("Internet at Home", [0, 1], index=profile["internet"], format_func=lambda x: "Yes" if x else "No")
    profile["romantic"] = st.selectbox("Romantic Relationship", [0, 1], index=profile["romantic"], format_func=lambda x: "Yes" if x else "No")
    profile["famrel"] = st.slider("Family Relationship (1-5)", 1, 5, profile["famrel"])
    profile["freetime"] = st.slider("Free Time (1-5)", 1, 5, profile["freetime"])
    profile["activities"] = st.selectbox("Activities", [0, 1], index=profile["activities"], format_func=lambda x: "Yes" if x else "No")

st.session_state.current_profile = profile

# ========================================
# MAIN AREA - Two Column Layout
# ========================================
col_current, col_divider, col_modified = st.columns([5, 0.5, 5])

# --- Left Column: Current Profile ---
with col_current:
    st.subheader("📊 Current Prediction")

    current_pred = get_prediction(profile)
    current_class = current_pred["class"]
    current_probs = current_pred["probabilities"]

    # Risk level badge
    color = RISK_COLORS.get(current_class, "#888")
    st.markdown(
        f'<div style="background-color:{color}; padding:20px; border-radius:10px; text-align:center;">'
        f'<h2 style="color:white; margin:0;">{current_class}</h2></div>',
        unsafe_allow_html=True,
    )

    st.markdown("**Current Changeable Features:**")
    current_changeable = {
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
    for k, v in current_changeable.items():
        st.markdown(f"- **{k}:** {v}")

# --- Divider ---
with col_divider:
    st.markdown(
        '<div style="border-left:2px solid #ccc; height:600px; margin:auto;"></div>',
        unsafe_allow_html=True,
    )

# --- Right Column: Modified Profile ---
with col_modified:
    st.subheader("🔧 What-If Scenario")
    st.markdown("Adjust the sliders below to simulate interventions:")

    modified = profile.copy()

    modified["studytime"] = st.slider(
        "📚 Study Time", 1, 4, profile["studytime"], key="wif_study",
        help="1: <2hrs, 2: 2-5hrs, 3: 5-10hrs, 4: >10hrs"
    )
    modified["absences"] = st.slider(
        "📅 Absences", 0, 93, profile["absences"], key="wif_abs"
    )
    modified["schoolsup"] = st.toggle("🏫 Extra School Support", value=bool(profile["schoolsup"]), key="wif_ss")
    modified["famsup"] = st.toggle("👨‍👩‍👧 Family Support", value=bool(profile["famsup"]), key="wif_fs")
    modified["paid"] = st.toggle("💰 Paid Classes", value=bool(profile["paid"]), key="wif_paid")
    modified["Dalc"] = st.slider("🍺 Workday Alcohol", 1, 5, profile["Dalc"], key="wif_dalc")
    modified["Walc"] = st.slider("🍻 Weekend Alcohol", 1, 5, profile["Walc"], key="wif_walc")
    modified["goout"] = st.slider("🚶 Going Out", 1, 5, profile["goout"], key="wif_goout")
    modified["health"] = st.slider("❤️ Health", 1, 5, profile["health"], key="wif_health")

    # Convert toggles back to int
    modified["schoolsup"] = int(modified["schoolsup"])
    modified["famsup"] = int(modified["famsup"])
    modified["paid"] = int(modified["paid"])

    # Reset button
    if st.button("🔄 Reset to Original", use_container_width=True):
        st.rerun()

    # Modified prediction
    mod_pred = get_prediction(modified)
    mod_class = mod_pred["class"]
    mod_probs = mod_pred["probabilities"]

    mod_color = RISK_COLORS.get(mod_class, "#888")
    st.markdown(
        f'<div style="background-color:{mod_color}; padding:20px; border-radius:10px; text-align:center;">'
        f'<h2 style="color:white; margin:0;">{mod_class}</h2></div>',
        unsafe_allow_html=True,
    )

# ========================================
# COMPARISON VISUALIZATIONS
# ========================================
st.markdown("---")
st.subheader("📈 Impact Visualization")

viz_col1, viz_col2 = st.columns(2)

# --- Before/After Probability Comparison ---
with viz_col1:
    classes = list(current_probs.keys())
    current_vals = [current_probs[c] * 100 for c in classes]
    modified_vals = [mod_probs[c] * 100 for c in classes]

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name="Current",
        x=classes,
        y=current_vals,
        marker_color=["#FF6B6B", "#FFB84D", "#51D88A"],
        opacity=0.7,
        text=[f"{v:.1f}%" for v in current_vals],
        textposition="auto",
    ))
    fig_bar.add_trace(go.Bar(
        name="What-If",
        x=classes,
        y=modified_vals,
        marker_color=["#CC0000", "#CC8400", "#008844"],
        text=[f"{v:.1f}%" for v in modified_vals],
        textposition="auto",
    ))
    fig_bar.update_layout(
        title="Probability Comparison",
        barmode="group",
        yaxis_title="Probability (%)",
        yaxis_range=[0, 100],
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# --- Probability Shift Visualization ---
with viz_col2:
    shifts = {c: (mod_probs[c] - current_probs[c]) * 100 for c in classes}
    colors = ["#00CC66" if s < 0 else "#FF4B4B" if "High" in c else "#FFB84D" if s > 0 else "#00CC66"
              for c, s in shifts.items()]

    # For High Risk: decrease is good (green), increase is bad (red)
    # For Low Risk: increase is good (green), decrease is bad (red)
    bar_colors = []
    for c, s in shifts.items():
        if "High" in c:
            bar_colors.append("#00CC66" if s <= 0 else "#FF4B4B")
        elif "Low" in c:
            bar_colors.append("#00CC66" if s >= 0 else "#FF4B4B")
        else:
            bar_colors.append("#FFB84D")

    fig_shift = go.Figure(go.Bar(
        x=list(shifts.keys()),
        y=list(shifts.values()),
        marker_color=bar_colors,
        text=[f"{s:+.1f}%" for s in shifts.values()],
        textposition="auto",
    ))
    fig_shift.update_layout(
        title="Probability Shift (Current → What-If)",
        yaxis_title="Change in Probability (%)",
        height=400,
        shapes=[dict(type="line", x0=-0.5, x1=2.5, y0=0, y1=0,
                     line=dict(color="gray", dash="dash"))],
    )
    st.plotly_chart(fig_shift, use_container_width=True)

# ========================================
# RISK LEVEL CHANGE INDICATOR
# ========================================
st.markdown("---")

if current_class != mod_class:
    # Determine if improvement or worsening
    risk_order = {"High Risk": 2, "Medium Risk": 1, "Low Risk": 0}
    curr_level = risk_order.get(current_class, 1)
    mod_level = risk_order.get(mod_class, 1)

    if mod_level < curr_level:
        st.success(f"✅ **Risk level improved:** {current_class} → {mod_class}")
    else:
        st.error(f"⚠️ **Risk level worsened:** {current_class} → {mod_class}")
else:
    st.info(f"ℹ️ **Risk level unchanged:** {current_class} — Try adjusting more features to see an impact.")

# ========================================
# INTERPRETATION TEXT
# ========================================
st.markdown("---")
st.subheader("💡 Interpretation")

changes = []
if modified["studytime"] != profile["studytime"]:
    direction = "increases" if modified["studytime"] > profile["studytime"] else "decreases"
    changes.append(
        f"📚 If study time **{direction} from {profile['studytime']} to {modified['studytime']}**, "
        f"this could shift the student's academic engagement and predicted risk."
    )
if modified["absences"] != profile["absences"]:
    diff = profile["absences"] - modified["absences"]
    if diff > 0:
        changes.append(
            f"📅 **Reducing absences by {diff} days** (from {profile['absences']} to {modified['absences']}) "
            f"could improve the student's predicted outcome."
        )
    else:
        changes.append(
            f"📅 **Increasing absences by {abs(diff)} days** would likely worsen the prediction."
        )
if modified["Dalc"] != profile["Dalc"] or modified["Walc"] != profile["Walc"]:
    old_total = profile["Dalc"] + profile["Walc"]
    new_total = modified["Dalc"] + modified["Walc"]
    if new_total < old_total:
        changes.append(
            f"🍺 **Reducing total alcohol consumption from {old_total} to {new_total}** "
            f"could lower the student's risk profile."
        )
    elif new_total > old_total:
        changes.append(
            f"🍺 **Increasing total alcohol consumption** would likely raise the risk level."
        )
if int(modified["schoolsup"]) != int(profile["schoolsup"]):
    if modified["schoolsup"]:
        changes.append("🏫 **Adding extra school support** could help reduce academic risk.")
    else:
        changes.append("🏫 **Removing school support** may increase the student's risk.")
if int(modified["paid"]) != int(profile["paid"]):
    if modified["paid"]:
        changes.append("💰 **Enrolling in paid classes** could provide additional academic support.")
    else:
        changes.append("💰 **Dropping paid classes** may negatively affect performance.")
if modified["goout"] != profile["goout"]:
    if modified["goout"] < profile["goout"]:
        changes.append(
            f"🚶 **Reducing going out from {profile['goout']} to {modified['goout']}** "
            f"could help the student focus more on academics."
        )
if modified["health"] != profile["health"]:
    if modified["health"] > profile["health"]:
        changes.append(
            f"❤️ **Improving health status from {profile['health']} to {modified['health']}** "
            f"is associated with better academic outcomes."
        )

if changes:
    for change in changes:
        st.markdown(change)
else:
    st.markdown("*Adjust the sliders in the What-If column to see how changes could impact the prediction.*")

# ========================================
# MULTIPLE SCENARIO TESTING
# ========================================
st.markdown("---")
st.subheader("🧪 Quick Scenarios")
st.markdown("Test common intervention strategies with one click:")

scen_col1, scen_col2, scen_col3 = st.columns(3)

with scen_col1:
    if st.button("📚 Study More", use_container_width=True, help="Increase study time to max"):
        scenario = profile.copy()
        scenario["studytime"] = 4
        pred = get_prediction(scenario)
        st.markdown(f"**Result:** {pred['class']}")
        for cls, prob in pred["probabilities"].items():
            st.markdown(f"- {cls}: {prob*100:.1f}%")

with scen_col2:
    if st.button("🚫 No Alcohol", use_container_width=True, help="Set all alcohol to minimum"):
        scenario = profile.copy()
        scenario["Dalc"] = 1
        scenario["Walc"] = 1
        pred = get_prediction(scenario)
        st.markdown(f"**Result:** {pred['class']}")
        for cls, prob in pred["probabilities"].items():
            st.markdown(f"- {cls}: {prob*100:.1f}%")

with scen_col3:
    if st.button("🌟 Full Support", use_container_width=True, help="Enable all support options"):
        scenario = profile.copy()
        scenario["schoolsup"] = 1
        scenario["famsup"] = 1
        scenario["paid"] = 1
        pred = get_prediction(scenario)
        st.markdown(f"**Result:** {pred['class']}")
        for cls, prob in pred["probabilities"].items():
            st.markdown(f"- {cls}: {prob*100:.1f}%")

# --- Footer ---
st.markdown("---")
st.caption(
    "⚠️ This tool is for educational exploration only. Predictions are based on a Random Forest model "
    "trained on the UCI Student Performance dataset with ~61% accuracy. Results should not be used "
    "as the sole basis for academic decisions."
)