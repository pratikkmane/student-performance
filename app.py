import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Performance Predictor", layout="wide")

st.title("🎓 Student Academic Performance Predictor")
st.markdown("---")

st.write("""
### About This Project
This app predicts student academic performance based on study habits, engagement levels, 
and demographic factors using data from two Portuguese secondary schools.

**Dataset:** 1,044 students across Math and Portuguese courses  
**Goal:** Identify at-risk students early to enable timely academic intervention
""")

# Load and show dataset preview
try:
    df_math = pd.read_csv('data/student-mat.csv', sep=';')
    df_por = pd.read_csv('data/student-por.csv', sep=';')
    
    st.subheader("Dataset Preview")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Math Course (395 students)**")
        st.dataframe(df_math.head(5))
    
    with col2:
        st.write("**Portuguese Course (649 students)**")
        st.dataframe(df_por.head(5))
        
except FileNotFoundError:
    st.error("Dataset files not found. Please ensure CSV files are in the data/ folder.")

st.markdown("---")
st.info("👈 Use the sidebar to navigate to different pages (coming soon)")