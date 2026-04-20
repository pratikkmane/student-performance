import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from pathlib import Path

# Page config
st.set_page_config(page_title="Data Insights", page_icon="📊", layout="wide")

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

# Title
st.title("📊 Data Insights & Visualizations")
st.markdown("---")

# Load data
@st.cache_data
def load_data():
    """Load the combined student dataset."""
    try:
        df = pd.read_csv('data/processed/combined_student_data.csv')
        return df
    except FileNotFoundError:
        st.error("❌ Dataset not found at data/processed/combined_student_data.csv")
        return None

df = load_data()

if df is None:
    st.stop()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Subject filter
subject_options = ['Both'] + df['subject'].unique().tolist()
subject_filter = st.sidebar.selectbox("Subject", subject_options)

# Risk level filter
risk_options = ['All'] + df['risk_category'].unique().tolist()
risk_filter = st.sidebar.selectbox("Risk Level", risk_options)

# Apply filters
df_filtered = df.copy()

if subject_filter != 'Both':
    df_filtered = df_filtered[df_filtered['subject'] == subject_filter]

if risk_filter != 'All':
    df_filtered = df_filtered[df_filtered['risk_category'] == risk_filter]

# Show filter stats
st.sidebar.markdown("---")
st.sidebar.metric("Total Students", len(df_filtered))
st.sidebar.metric("Math Students", len(df_filtered[df_filtered['subject'] == 'math']))
st.sidebar.metric("Portuguese Students", len(df_filtered[df_filtered['subject'] == 'portuguese']))

# Main content
st.info(f"📌 Showing **{len(df_filtered)}** students out of **{len(df)}** total")

# ============================================================================
# VISUALIZATION 1: Grade Distribution
# ============================================================================

st.header("1️⃣ Final Grade Distribution (G3)")

col1, col2 = st.columns([2, 1])

with col1:
    # Overall histogram with subject comparison
    fig1 = px.histogram(
        df_filtered, 
        x='G3', 
        color='subject',
        nbins=20,
        title='Final Grade Distribution by Subject',
        labels={'G3': 'Final Grade (0-20)', 'count': 'Number of Students'},
        color_discrete_map={'math': '#FF6B6B', 'portuguese': '#4ECDC4'},
        barmode='overlay',
        opacity=0.7
    )
    fig1.update_layout(
        xaxis_title="Final Grade (G3)",
        yaxis_title="Number of Students",
        showlegend=True,
        hovermode='x unified'
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("### 📈 Key Takeaways")
    st.markdown(f"""
    - **Average Grade:** {df_filtered['G3'].mean():.2f}/20
    - **Passing Rate (≥10):** {(df_filtered['G3'] >= 10).sum() / len(df_filtered) * 100:.1f}%
    - **Math Avg:** {df_filtered[df_filtered['subject']=='math']['G3'].mean():.2f}
    - **Portuguese Avg:** {df_filtered[df_filtered['subject']=='portuguese']['G3'].mean():.2f}
    
    📊 Portuguese students generally score higher than Math students.
    """)

# Download button
csv1 = df_filtered[['subject', 'G3']].to_csv(index=False)
st.download_button("⬇️ Download Grade Data", csv1, "grade_distribution.csv", "text/csv", type="primary")

st.markdown("---")

# ============================================================================
# VISUALIZATION 2: Risk Category Breakdown
# ============================================================================

st.header("2️⃣ Risk Category Distribution")

col1, col2 = st.columns([2, 1])

with col1:
    # Pie chart
    risk_counts = df_filtered['risk_category'].value_counts()
    
    fig2 = px.pie(
        values=risk_counts.values,
        names=risk_counts.index,
        title='Student Risk Level Distribution',
        color=risk_counts.index,
        color_discrete_map={'High': '#FF6B6B', 'Medium': '#FFD93D', 'Low': '#6BCF7F'},
        hole=0.4
    )
    fig2.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.markdown("### 📈 Key Takeaways")
    for risk_level in ['High', 'Low', 'Medium']:
        count = (df_filtered['risk_category'] == risk_level).sum()
        pct = count / len(df_filtered) * 100
        emoji = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}[risk_level]
        st.markdown(f"**{emoji} {risk_level}:** {count} ({pct:.1f}%)")
    
    st.markdown(f"""
    
    💡 Most students are **{risk_counts.idxmax()}** risk, indicating the model 
    can identify struggling students for early intervention.
    """)

# Download
csv2 = df_filtered['risk_category'].value_counts().to_csv()
st.download_button("⬇️ Download Risk Data", csv2, "risk_distribution.csv", "text/csv", type="primary")

st.markdown("---")

# ============================================================================
# VISUALIZATION 3: Feature Correlations
# ============================================================================

st.header("3️⃣ Top Features Affecting Final Grade")

# Calculate correlations
numeric_cols = ['age', 'Medu', 'Fedu', 'traveltime', 'studytime', 'failures', 
                'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences']

correlations = df_filtered[numeric_cols + ['G3']].corr()['G3'].drop('G3').sort_values(key=abs, ascending=False).head(10)

col1, col2 = st.columns([2, 1])

with col1:
    fig3 = px.bar(
        x=correlations.values,
        y=correlations.index,
        orientation='h',
        title='Top 10 Features Correlated with Final Grade',
        labels={'x': 'Correlation Coefficient', 'y': 'Feature'},
        color=correlations.values,
        color_continuous_scale=['red', 'yellow', 'green']
    )
    fig3.update_layout(showlegend=False, yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.markdown("### 📈 Key Takeaways")
    top_positive = correlations[correlations > 0].head(3)
    top_negative = correlations[correlations < 0].head(3)
    
    st.markdown("**Positive Factors:**")
    for feat, val in top_positive.items():
        st.markdown(f"- {feat}: +{val:.3f}")
    
    st.markdown("**Negative Factors:**")
    for feat, val in top_negative.items():
        st.markdown(f"- {feat}: {val:.3f}")
    
    st.markdown(f"""
    
    ⚠️ **Past failures** is the strongest predictor - students with 
    prior failures are much more likely to struggle.
    """)

# Download
csv3 = correlations.to_csv()
st.download_button("⬇️ Download Correlation Data", csv3, "correlations.csv", "text/csv", type="primary")

st.markdown("---")

# ============================================================================
# VISUALIZATION 4: Study Time Impact
# ============================================================================

st.header("4️⃣ Study Time Impact on Grades")

col1, col2 = st.columns([2, 1])

with col1:
    fig4 = px.box(
        df_filtered,
        x='studytime',
        y='G3',
        color='studytime',
        title='Final Grade by Weekly Study Time',
        labels={'studytime': 'Study Time Level', 'G3': 'Final Grade'},
        category_orders={'studytime': [1, 2, 3, 4]}
    )
    fig4.update_layout(showlegend=False)
    fig4.update_xaxes(ticktext=['<2 hrs', '2-5 hrs', '5-10 hrs', '>10 hrs'], tickvals=[1, 2, 3, 4])
    st.plotly_chart(fig4, use_container_width=True)

with col2:
    st.markdown("### 📈 Key Takeaways")
    study_stats = df_filtered.groupby('studytime')['G3'].agg(['mean', 'count'])
    
    for level in [1, 2, 3, 4]:
        if level in study_stats.index:
            avg = study_stats.loc[level, 'mean']
            cnt = study_stats.loc[level, 'count']
            label = ['<2hrs', '2-5hrs', '5-10hrs', '>10hrs'][level-1]
            st.markdown(f"**{label}:** {avg:.1f} avg ({cnt} students)")
    
    st.markdown(f"""
    
    📚 Students who study more tend to score higher, but the relationship 
    isn't perfectly linear - quality matters more than quantity!
    """)

# Download
csv4 = df_filtered[['studytime', 'G3']].to_csv(index=False)
st.download_button("⬇️ Download Study Time Data", csv4, "studytime_impact.csv", "text/csv", type="primary")

st.markdown("---")

# ============================================================================
# VISUALIZATION 5: Parent Education Effect
# ============================================================================

st.header("5️⃣ Parent Education Impact")

col1, col2 = st.columns([2, 1])

with col1:
    # Create average parent education
    df_filtered['parent_avg_edu'] = (df_filtered['Medu'] + df_filtered['Fedu']) / 2
    
    parent_stats = df_filtered.groupby('parent_avg_edu')['G3'].mean().reset_index()
    
    fig5 = px.bar(
        parent_stats,
        x='parent_avg_edu',
        y='G3',
        title='Average Student Grade by Parent Education Level',
        labels={'parent_avg_edu': 'Average Parent Education (0-4)', 'G3': 'Average Final Grade'},
        color='G3',
        color_continuous_scale='Viridis'
    )
    fig5.update_layout(showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    st.markdown("### 📈 Key Takeaways")
    
    low_edu = df_filtered[df_filtered['parent_avg_edu'] <= 1]['G3'].mean()
    high_edu = df_filtered[df_filtered['parent_avg_edu'] >= 3]['G3'].mean()
    
    st.markdown(f"""
    - **Low Parent Edu (≤1):** {low_edu:.2f} avg
    - **High Parent Edu (≥3):** {high_edu:.2f} avg
    - **Difference:** {high_edu - low_edu:.2f} points
    
    👨‍👩‍👧 Parent education level strongly correlates with student 
    performance - students with educated parents score **{((high_edu/low_edu - 1)*100):.1f}% higher** 
    on average.
    """)

# Download
csv5 = df_filtered[['Medu', 'Fedu', 'G3']].to_csv(index=False)
st.download_button("⬇️ Download Parent Education Data", csv5, "parent_education.csv", "text/csv", type="primary")

st.markdown("---")

# ============================================================================
# VISUALIZATION 6: Absences vs Grades
# ============================================================================

st.header("6️⃣ Attendance Impact on Performance")

col1, col2 = st.columns([2, 1])

with col1:
    # Scatter plot with trend line
    fig6 = px.scatter(
        df_filtered,
        x='absences',
        y='G3',
        color='risk_category',
        title='Absences vs Final Grade',
        labels={'absences': 'Number of Absences', 'G3': 'Final Grade'},
        trendline='ols',
        color_discrete_map={'High': '#FF6B6B', 'Medium': '#FFD93D', 'Low': '#6BCF7F'},
        opacity=0.6
    )
    fig6.update_layout(hovermode='closest')
    st.plotly_chart(fig6, use_container_width=True)

with col2:
    st.markdown("### 📈 Key Takeaways")
    
    correlation = df_filtered[['absences', 'G3']].corr().iloc[0, 1]
    
    low_absent = df_filtered[df_filtered['absences'] <= 5]['G3'].mean()
    high_absent = df_filtered[df_filtered['absences'] > 10]['G3'].mean()
    
    st.markdown(f"""
    - **Correlation:** {correlation:.3f}
    - **Low Absences (≤5):** {low_absent:.2f} avg
    - **High Absences (>10):** {high_absent:.2f} avg
    - **Grade Drop:** {low_absent - high_absent:.2f} points
    
    ⚠️ Students with high absences score significantly lower. Each 
    additional absence is associated with lower performance.
    """)

# Download
csv6 = df_filtered[['absences', 'G3', 'risk_category']].to_csv(index=False)
st.download_button("⬇️ Download Absence Data", csv6, "absences_grades.csv", "text/csv", type="primary")

st.markdown("---")

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================

st.header("📋 Summary Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Average Grade", f"{df_filtered['G3'].mean():.2f}/20")
    st.metric("Median Grade", f"{df_filtered['G3'].median():.2f}/20")

with col2:
    passing = (df_filtered['G3'] >= 10).sum()
    passing_rate = passing / len(df_filtered) * 100
    st.metric("Passing Rate", f"{passing_rate:.1f}%")
    st.metric("Total Students", len(df_filtered))

with col3:
    high_risk = (df_filtered['risk_category'] == 'High').sum()
    high_risk_pct = high_risk / len(df_filtered) * 100
    st.metric("High Risk Students", f"{high_risk_pct:.1f}%")
    st.metric("Average Absences", f"{df_filtered['absences'].mean():.1f}")

with col4:
    avg_study = df_filtered['studytime'].mean()
    study_labels = {1: '<2hrs', 2: '2-5hrs', 3: '5-10hrs', 4: '>10hrs'}
    st.metric("Avg Study Time", study_labels.get(round(avg_study), f"{avg_study:.1f}"))
    st.metric("Avg Parent Edu", f"{((df_filtered['Medu'] + df_filtered['Fedu'])/2).mean():.2f}/4")

st.markdown("---")

# Footer
st.markdown("""
### 💡 Overall Insights

**Key Findings:**
1. **Failures matter most** - Past academic failures are the strongest predictor of future performance
2. **Parent education helps** - Students with educated parents perform significantly better
3. **Attendance is critical** - High absences correlate with lower grades
4. **Study time helps** - More study time generally leads to better performance
5. **Portuguese > Math** - Students tend to score higher in Portuguese than Math

**Actionable Recommendations:**
- 🎯 Focus intervention resources on students with prior failures
- 👨‍👩‍👧 Provide extra support for students from less-educated families
- 📅 Monitor and reduce absences through attendance programs
- 📚 Encourage consistent study habits (quality over quantity)
- 🔢 Provide additional Math tutoring resources

---
*Data based on 1,044 Portuguese secondary school students (Math & Portuguese courses)*
""")
