import streamlit as st
from pathlib import Path
from datetime import datetime

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/pratikkmane/student-performance',
        'Report a bug': "https://github.com/pratikkmane/student-performance/issues",
        'About': "# Student Performance Predictor\nMS Applied Data Science - IU Luddy School"
    }
)

# ============================================================================
# LOAD CUSTOM CSS
# ============================================================================

def load_css():
    """Load custom CSS styling."""
    css_file = Path("assets/style.css")
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
    
    # Team Info
    st.markdown("### 👥 Team")
    st.markdown("""
    <small style="color: rgba(255,255,255,0.9);">
    <b>Lead:</b> Pratik Mane<br>
    <b>Members:</b> Emmanuel Atilola, Yugant Nagralawala, Hamza Almani<br>
    <b>Advisor:</b> Prof. Leon Johnson
    </small>
    """, unsafe_allow_html=True)

# ============================================================================
# MAIN CONTENT
# ============================================================================

# Hero Section
st.markdown("""
    <div class="fade-in">
        <h1 style="text-align: center; color: #1E88E5; margin-bottom: 0;">
            🎓 Student Academic Performance Predictor
        </h1>
        <p style="text-align: center; font-size: 1.2rem; color: #757575; margin-top: 0.5rem;">
            Identify at-risk students early with AI-powered predictions
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Feature Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-card">
            <h3 style="color: #1E88E5; text-align: center;">🎯 Early Intervention</h3>
            <p style="text-align: center;">
                Predict student performance at the start of the year to enable timely support
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <h3 style="color: #43A047; text-align: center;">📈 Data-Driven</h3>
            <p style="text-align: center;">
                Built on 1,044 student records with 43 features analyzing study habits and background
            </p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <h3 style="color: #FB8C00; text-align: center;">⚡ Instant Results</h3>
            <p style="text-align: center;">
                Get real-time risk predictions with confidence scores and actionable insights
            </p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# How It Works
st.markdown("## 🔄 How It Works")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h1 style="color: #1E88E5;">1️⃣</h1>
            <h4>Input Data</h4>
            <p style="font-size: 0.9rem;">Fill student information form</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h1 style="color: #1E88E5;">2️⃣</h1>
            <h4>AI Analysis</h4>
            <p style="font-size: 0.9rem;">Model processes 43 features</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h1 style="color: #1E88E5;">3️⃣</h1>
            <h4>Get Prediction</h4>
            <p style="font-size: 0.9rem;">Receive risk level & confidence</p>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h1 style="color: #1E88E5;">4️⃣</h1>
            <h4>Take Action</h4>
            <p style="font-size: 0.9rem;">Implement recommendations</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Quick Start
st.markdown("## 🚀 Quick Start")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### Getting Started
    
    1. **Navigate to Predict** - Click "🎯 Predict" in the sidebar
    2. **Fill the Form** - Enter student information across 5 sections:
       - Demographics (age, school, address)
       - Family Background (parent education, jobs)
       - School Information (study time, failures, support)
       - Social & Lifestyle (going out, alcohol consumption)
       - Health (absences, health status)
    3. **Click Predict** - Get instant risk assessment
    4. **Review Results** - See risk level, confidence, and probabilities
    5. **Explore Insights** - Visit Data Insights for patterns
    
    ### 📊 Understanding Risk Levels
    
    - 🔴 **High Risk** - Student may struggle, needs immediate intervention
    - 🟡 **Medium Risk** - Monitor closely, provide support as needed
    - 🟢 **Low Risk** - Student on track, maintain current approach
    """)

with col2:
    st.info("""
    ### 💡 Quick Tips
    
    **For Best Results:**
    - Fill all fields accurately
    - Be honest about study habits
    - Consider all support systems
    
    **Explore Features:**
    - 🔮 What-If Analysis
    - 📊 Data Insights
    - 📈 Model Performance
    - ℹ️ About the Project
    
    **Need Help?**
    - Check the About page
    - View GitHub repository
    """)

st.markdown("---")

# Dataset Overview
st.markdown("## 📚 Dataset Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Students",
        value="1,044",
        delta="Math + Portuguese"
    )

with col2:
    st.metric(
        label="Features",
        value="43",
        delta="39 base + 4 engineered"
    )

with col3:
    st.metric(
        label="Best Model",
        value="Random Forest",
        delta="61% accuracy"
    )

with col4:
    st.metric(
        label="Response Time",
        value="< 1s",
        delta="Real-time"
    )

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown("""
    <div class="footer">
        <h3 style="color: #1E88E5; margin-bottom: 1rem;">Student Performance Predictor</h3>
        <p><b>MS Applied Data Science Final Project</b></p>
        <p>Indiana University Luddy School of Informatics, Computing & Engineering</p>
        <p style="margin-top: 1rem;">
            <b>Team 4:</b> Pratik Mane, Emmanuel Atilola, Yugant Nagralawala, Hamza Almani | 
            <b>Advisor:</b> Prof. Leon Johnson
        </p>
        <p style="margin-top: 0.5rem;">
            <a href="https://github.com/pratikkmane/student-performance" target="_blank">
                📂 GitHub Repository
            </a> | 
            <a href="https://luddy.indianapolis.iu.edu/index.html" target="_blank">
                🏛️ IU Luddy School
            </a>
        </p>
        <p style="font-size: 0.85rem; color: #999; margin-top: 1rem;">
            Last Updated: {last_updated} | Built with Streamlit | Data: UCI ML Repository
        </p>
        <p style="font-size: 0.75rem; color: #999; margin-top: 0.5rem;">
            © 2026 Team 4. All rights reserved. | For educational purposes only.
        </p>
    </div>
""".format(last_updated=datetime.now().strftime("%B %d, %Y")), unsafe_allow_html=True)
