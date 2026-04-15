import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

st.set_page_config(page_title="About - Student Performance Predictor", layout="wide")

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

# ── Shared CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .section-header {
        background: linear-gradient(90deg, #1565C0, #1976D2);
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        margin: 16px 0 8px 0;
        font-size: 1.15rem;
        font-weight: 600;
    }
    .info-card {
        background: #F3F6FA;
        border-left: 4px solid #1976D2;
        padding: 14px 18px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 10px;
    }
    .metric-card {
        background: #E8F5E9;
        border-left: 4px solid #43A047;
        padding: 14px 18px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 10px;
    }
    .warning-card {
        background: #FFF8E1;
        border-left: 4px solid #FFA000;
        padding: 14px 18px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 10px;
    }
    .step-box {
        background: #EDE7F6;
        border-radius: 8px;
        padding: 10px 16px;
        margin: 6px 0;
        font-size: 0.97rem;
    }
    .risk-high  { color: #C62828; font-weight: 700; }
    .risk-med   { color: #E65100; font-weight: 700; }
    .risk-low   { color: #2E7D32; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ── Title ─────────────────────────────────────────────────────────────────────
st.title("About This Project")
st.markdown("*Student Academic Performance Predictor — Early Intervention System*")
st.markdown("---")

# ── Tabs ──────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "Project Overview",
    "How It Works",
    "Dataset",
    "Model Performance",
    "Team & Repo",
    "Ethics",
    "How to Use",
    "FAQs",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — PROJECT OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown('<div class="section-header">Project Overview</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="info-card">
            <b>Goal</b><br>
            Build an early-intervention system that identifies students at academic risk
            <em>before</em> mid-term exams — enabling educators to provide targeted support
            when it can still make a difference.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="info-card">
            <b>Dataset</b><br>
            UCI Student Performance Dataset — <b>1,044 records</b>, <b>30 raw features</b>
            (expanded to 43 after encoding &amp; feature engineering).<br>
            Covers Math and Portuguese secondary-school courses.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <b>Selected Model</b><br>
            <b>Random Forest</b> with RandomizedSearchCV hyperparameter tuning
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="metric-card">
            <b>Validation Accuracy</b><br>
            <span style="font-size:1.6rem; font-weight:700; color:#2E7D32;">60.5%</span>
            &nbsp; on held-out validation set (157 samples)
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Risk Categories")
    rc_col1, rc_col2, rc_col3 = st.columns(3)
    with rc_col1:
        st.error("**High Risk** — Final grade < 10\nStudent likely to fail without intervention.")
    with rc_col2:
        st.warning("**Medium Risk** — Final grade 10–13\nStudent is borderline; monitoring recommended.")
    with rc_col3:
        st.success("**Low Risk** — Final grade ≥ 14\nStudent is on track to pass comfortably.")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — HOW IT WORKS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="section-header">How It Works</div>', unsafe_allow_html=True)

    st.markdown("### Prediction Pipeline")

    steps = [
        ("1", "Collect student background data", "Demographics, family background, study habits, social behaviour — all available at enrollment time."),
        ("2", "Feature encoding & engineering", "Categorical variables are one-hot encoded. Three engineered features are computed: parent education average, total alcohol consumption, and support availability flag."),
        ("3", "Feature scaling", "All 43 features are standardised using the same StandardScaler fitted on training data."),
        ("4", "Random Forest prediction", "The trained model outputs a risk category (High / Medium / Low) and per-class probabilities."),
        ("5", "Personalised recommendations", "Results are presented with an explanation and actionable suggestions tailored to the predicted risk level."),
    ]

    for num, title, detail in steps:
        st.markdown(f"""
        <div class="step-box">
            <b>Step {num}: {title}</b><br>
            <span style="color:#555;">{detail}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div class="warning-card">
        <b>No mid-term grades required</b><br>
        Every feature used by this model is collected at or before enrolment.
        The prediction is made purely from socio-demographic and behavioural data,
        enabling intervention at the very start of the academic year.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Feature Categories Used")
    feat_col1, feat_col2, feat_col3 = st.columns(3)
    with feat_col1:
        st.markdown("**Demographics**")
        st.markdown("- School, Sex, Age\n- Address (Urban/Rural)\n- Family size\n- Parent cohabitation status")
    with feat_col2:
        st.markdown("**Family & School**")
        st.markdown("- Mother/Father education & job\n- Guardian\n- Travel time, Study time\n- Past failures\n- Extra support flags")
    with feat_col3:
        st.markdown("**Social & Lifestyle**")
        st.markdown("- Internet access\n- Romantic relationship\n- Family relations quality\n- Free time, Going-out frequency\n- Alcohol consumption (weekday/weekend)\n- Health status, Absences")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — DATASET
# ══════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div class="section-header">Dataset Information</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("""
        ### UCI Student Performance Dataset

        This dataset was collected from two Portuguese secondary schools
        (*Gabriel Pereira* and *Mousinho da Silveira*) and covers two subjects:

        | Attribute | Value |
        |---|---|
        | Source | UCI Machine Learning Repository |
        | Total records (combined) | **1,044** |
        | Math course records | 395 |
        | Portuguese course records | 649 |
        | Raw features | 30 |
        | Features after processing | **43** |
        | Target variable | Final grade G3 → risk category |
        | Train / Validation split | 887 / 157 (85% / 15%) |

        The grades (G1, G2, G3) range from 0–20.
        Only G3 (the final grade) is used as the prediction target;
        G1 and G2 are **excluded** to enable true early prediction.
        """)

    with col2:
        # Class distribution chart
        labels = ["High Risk\n(< 10)", "Medium Risk\n(10–13)", "Low Risk\n(≥ 14)"]
        sizes  = [224, 500, 320]   # approximate from dataset analysis
        colors = ["#EF5350", "#FFA726", "#66BB6A"]

        fig, ax = plt.subplots(figsize=(4, 4))
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, colors=colors,
            autopct="%1.0f%%", startangle=90,
            textprops={"fontsize": 9}
        )
        ax.set_title("Approximate Class Distribution", fontsize=10)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.markdown("---")
    st.markdown("""
    <div class="info-card">
        <b>Data source:</b>
        P. Cortez and A. Silva. "Using Data Mining to Predict Secondary School Student Performance."
        In A. Brito and J. Teixeira Eds., <em>Proceedings of 5th Annual Future Business Technology Conference</em>,
        Porto, 2008, pp. 5-12.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — MODEL PERFORMANCE
# ══════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div class="section-header">Model Performance</div>', unsafe_allow_html=True)

    st.markdown("### Model Comparison")
    comparison_data = {
        "Model": ["Logistic Regression", "Decision Tree", "Random Forest"],
        "Accuracy": ["55.4%", "50.3%", "**60.5%** ✓"],
        "Macro Precision": ["53.5%", "56.5%", "67.7%"],
        "Macro Recall": ["50.1%", "51.8%", "50.6%"],
    }
    st.table(pd.DataFrame(comparison_data).set_index("Model"))

    st.markdown("""
    <div class="metric-card">
        <b>Selected model: Random Forest</b> — highest accuracy and most consistent
        performance across all three risk classes. Especially better at avoiding
        false negatives for Medium-risk students.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Random Forest — Per-class Metrics")

    perf_data = {
        "Risk Category": ["High", "Medium", "Low"],
        "Precision": [0.78, 0.57, 0.68],
        "Recall":    [0.20, 0.88, 0.43],
        "F1 Score":  [0.32, 0.70, 0.53],
        "Support":   [35, 78, 44],
    }
    perf_df = pd.DataFrame(perf_data).set_index("Risk Category")
    st.dataframe(perf_df.style.format({
        "Precision": "{:.0%}", "Recall": "{:.0%}", "F1 Score": "{:.0%}"
    }), use_container_width=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Confusion Matrix (Random Forest, validation set)")
        cm = np.array([
            [ 7, 26,  2],   # High  (actual)
            [ 2, 69,  7],   # Medium (actual)
            [ 3, 22, 19],   # Low   (actual)
        ])
        labels = ["High", "Medium", "Low"]
        fig, ax = plt.subplots(figsize=(5, 4))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                    xticklabels=labels, yticklabels=labels, ax=ax)
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        ax.set_title("Confusion Matrix")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        st.markdown("#### Feature Importance (Top 10)")
        # Top features derived from model training analysis
        features = [
            "failures", "absences", "studytime", "age",
            "Medu", "Fedu", "goout", "Walc",
            "health", "higher_yes",
        ]
        importances = [0.18, 0.13, 0.10, 0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.04]
        fig2, ax2 = plt.subplots(figsize=(5, 4))
        colors = sns.color_palette("viridis", len(features))
        ax2.barh(features[::-1], importances[::-1], color=colors)
        ax2.set_xlabel("Relative Importance")
        ax2.set_title("Top 10 Features")
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close()

    st.markdown("---")
    st.markdown("### Accuracy vs Precision/Recall Trade-off")
    st.info("""
    **High Risk** students have high precision (78%) but low recall (20%) —
    the model is conservative: when it predicts High Risk, it is usually right,
    but it misses many at-risk students. This is an important limitation educators
    should be aware of when using the tool.
    """)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — TEAM & REPO
# ══════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown('<div class="section-header">Team Members & Repository</div>', unsafe_allow_html=True)

    team = [
        ("Yugant",  "About page, documentation, project structure"),
        ("Pratik",  "Streamlit app integration, prediction pipeline"),
        ("Emmanuel","Recommendations engine, model evaluation"),
    ]

    for name, role in team:
        st.markdown(f"""
        <div class="info-card">
            <b>{name}</b><br>
            <span style="color:#555;">{role}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### GitHub Repository")
    st.markdown("""
    <div class="info-card">
        Source code, notebooks, and data processing scripts are available on GitHub.<br>
        <b>Repository:</b> <a href="https://github.com/pratikkmane/student-performance" target="_blank">
        github.com/pratikkmane/student-performance</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Contact")
    st.markdown("""
    For questions or feedback about this project, please open an issue on the GitHub repository
    or reach out to any team member via their GitHub profile.
    """)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — ETHICAL CONSIDERATIONS
# ══════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown('<div class="section-header">Ethical Considerations</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="warning-card">
        <b>This tool is designed to support educators, not replace their judgement.</b>
        Read the considerations below before using predictions in any decision-making context.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Model Limitations")
    st.markdown("""
    - **Accuracy is ~60.5%** — roughly 4 in 10 predictions may be incorrect.
    - The model has **low recall for High-Risk students** (20%), meaning many genuinely at-risk
      students will be classified as Medium or Low Risk.
    - The training data comes from **two Portuguese schools** only; performance may differ in
      other educational contexts, countries, or demographic groups.
    - Socio-demographic proxies (alcohol, absences, parental education) may encode structural
      inequalities present in the original data.
    """)

    st.markdown("### Not for Punitive Use")
    st.markdown("""
    <div class="warning-card">
        Predictions must <b>never</b> be used to penalise, label, or stigmatise students.
        The sole intended purpose is to trigger <em>supportive</em> interventions — additional
        tutoring, counselling check-ins, or resource allocation — not disciplinary action.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Privacy Considerations")
    st.markdown("""
    - No personally identifiable information (name, ID, contact details) is collected or stored by this app.
    - Prediction results are **not persisted** between sessions.
    - If deployed in a real school setting, all data handling must comply with applicable
      privacy regulations (e.g., FERPA, GDPR).
    """)

    st.markdown("### Human Oversight Required")
    st.markdown("""
    <div class="info-card">
        A trained educator or counsellor must review every prediction before any action is taken.
        The model is a <b>decision-support tool</b>, not an autonomous decision-maker.
        Context that the model cannot see — a student's personal circumstances, recent events,
        or classroom observations — should always take precedence.
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 7 — HOW TO USE
# ══════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    st.markdown('<div class="section-header">How to Use This Tool</div>', unsafe_allow_html=True)

    st.markdown("### Step-by-Step Guide")

    guide_steps = [
        ("Step 1 — Navigate to the Prediction page",
         "Click **Home** or **Prediction** in the left sidebar to open the prediction form."),
        ("Step 2 — Fill in Demographics",
         "Select the student's school, sex, age, address type, family size, and parent cohabitation status."),
        ("Step 3 — Enter Family Background",
         "Provide mother's and father's education level (0–4 scale) and occupation, "
         "select the primary guardian, and indicate whether the family provides academic support."),
        ("Step 4 — Complete School Information",
         "Choose the reason the student selected this school, travel time to school, "
         "weekly study hours, number of past failures, and any extra support (school support, paid classes, activities)."),
        ("Step 5 — Add Social & Lifestyle Details",
         "Fill in internet access, romantic relationship status, family relations quality, "
         "free time, going-out frequency, weekday and weekend alcohol consumption."),
        ("Step 6 — Health & Absences",
         "Rate the student's health (1–5) and enter the number of school absences."),
        ("Step 7 — Select Subject",
         "Choose whether the student is enrolled in Math or Portuguese."),
        ("Step 8 — Submit",
         "Click **Predict Student Risk Level**. Results appear immediately below the form."),
        ("Step 9 — Interpret results",
         "Review the predicted risk category, confidence score, and per-class probabilities. "
         "Use the recommendations to plan next steps."),
    ]

    for title, detail in guide_steps:
        st.markdown(f"""
        <div class="step-box">
            <b>{title}</b><br>
            <span style="color:#444;">{detail}</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Tips for Best Results")
    st.markdown("""
    - **Answer every field honestly** — the model was trained on real self-reported data;
      inflated or guessed values will reduce prediction quality.
    - **Use the most recent information** — update values like absences and alcohol consumption
      to reflect the current term, not historical averages.
    - **Run predictions periodically** — risk can change as circumstances change.
      Re-run the prediction after significant life events or mid-term check-ins.
    - **Combine with teacher observation** — the model sees only the features listed above.
      A teacher who notices in-class disengagement has information the model does not.
    - **Do not share raw probabilities with students** — communicate conclusions
      (e.g., "we'd like to offer you extra tutoring") rather than numeric scores.
    """)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 8 — FAQs
# ══════════════════════════════════════════════════════════════════════════════
with tabs[7]:
    st.markdown('<div class="section-header">Frequently Asked Questions</div>', unsafe_allow_html=True)

    faqs = [
        (
            "Why doesn't the predictor ask for G1 or G2 (mid-term grades)?",
            "By design. The goal is **early** prediction — identifying at-risk students "
            "before any graded assessment takes place, so support can be offered at the "
            "start of the school year rather than after students have already fallen behind."
        ),
        (
            "How accurate is the model?",
            "The Random Forest model achieves **60.5% accuracy** on the validation set. "
            "This means approximately 1 in 3 predictions is incorrect. "
            "Always treat predictions as one signal among many, not a definitive verdict."
        ),
        (
            "What does 'High Risk' actually mean?",
            "High Risk means the model predicts the student will receive a final grade below 10 "
            "(out of 20), which corresponds to a failing grade in the Portuguese secondary system. "
            "It does not mean the student will definitely fail — it is a statistical indicator."
        ),
        (
            "Why does the model sometimes miss High-Risk students?",
            "High Risk has the lowest recall (20%) in our evaluation. The model tends to be "
            "conservative — it only labels a student High Risk when the evidence is strong. "
            "This reduces false alarms but means many genuinely at-risk students are classified "
            "as Medium. Educators should treat Medium-Risk predictions with attention as well."
        ),
        (
            "Can this model be used for students outside Portugal?",
            "With caution. The model was trained on data from two Portuguese schools. "
            "Grading scales, cultural norms, and educational systems differ across countries. "
            "Re-training on local data would significantly improve reliability."
        ),
        (
            "Is student data stored or shared?",
            "No. This application does not collect, store, or transmit any data entered into "
            "the prediction form. All processing happens locally within the app session, "
            "and no information persists after the browser tab is closed."
        ),
        (
            "Can a student's risk level change?",
            "Yes. Risk is not fixed — it reflects the student's current circumstances. "
            "A student initially predicted as High Risk who starts receiving tutoring, "
            "reduces absences, or improves study habits may move to a lower risk category "
            "if the prediction is re-run with updated values."
        ),
        (
            "What should I do if a student is predicted High Risk?",
            "Treat this as a prompt to start a conversation, not a cause for alarm. "
            "Consider: arranging a check-in with the student, offering school or paid tutoring, "
            "connecting the family with support resources, or monitoring attendance more closely. "
            "All actions should be supportive and voluntary."
        ),
        (
            "Which features have the most impact on the prediction?",
            "Based on feature importance analysis, the top predictors are: "
            "**number of past failures**, **school absences**, **weekly study time**, "
            "**student age**, and **parental education level**. "
            "Social factors (going-out frequency, alcohol consumption) also contribute "
            "but carry less weight than academic and family background features."
        ),
        (
            "How was the model trained?",
            "A Random Forest classifier was trained using RandomizedSearchCV with 5-fold "
            "stratified cross-validation on 887 training samples. "
            "The best hyperparameters were selected based on cross-validation accuracy, "
            "then the final model was evaluated on a separate held-out validation set of 157 samples."
        ),
    ]

    for question, answer in faqs:
        with st.expander(question):
            st.markdown(answer)
