import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import pickle
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

st.cache_data.clear()
st.cache_resource.clear()

# Feature names
FEATURES = [
    'age', 'Medu', 'Fedu', 'traveltime', 'studytime', 'failures', 'famrel', 
    'freetime', 'goout', 'Dalc', 'Walc', 'health', 'absences', 'school_MS', 
    'sex_M', 'address_U', 'famsize_LE3', 'Pstatus_T', 'Mjob_health', 'Mjob_other', 
    'Mjob_services', 'Mjob_teacher', 'Fjob_health', 'Fjob_other', 'Fjob_services', 
    'Fjob_teacher', 'reason_home', 'reason_other', 'reason_reputation', 
    'guardian_mother', 'guardian_other', 'schoolsup_yes', 'famsup_yes', 'paid_yes', 
    'activities_yes', 'nursery_yes', 'higher_yes', 'internet_yes', 'romantic_yes', 
    'subject_portuguese', 'parent_edu_avg', 'total_alcohol', 'has_support'
]

@st.cache_resource
def load_models():
    """Load the trained Random Forest model"""
    import joblib
    try:
        model = joblib.load('models/random_forest.pkl')
        st.success("✓ Random Forest model loaded successfully")
        return model
    except FileNotFoundError:
        st.error("❌ Random Forest model not found at models/random_forest.pkl")
        return None
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        return None

@st.cache_resource
def load_scaler():
    """Load the scaler for feature normalization"""
    try:
        with open('models/scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
            st.success("✓ Scaler loaded successfully")
            return scaler
    except FileNotFoundError:
        st.warning("⚠️ Scaler not found at models/scaler.pkl")
        return None

def create_template_csv():
    """Create a sample CSV template for batch predictions"""
    
    # Sample data - 3 example rows
    sample_data = {
        'age': [15, 16, 17],
        'Medu': [4, 3, 2],
        'Fedu': [3, 4, 2],
        'traveltime': [1, 2, 1],
        'studytime': [2, 3, 1],
        'failures': [0, 0, 1],
        'famrel': [4, 5, 3],
        'freetime': [3, 4, 2],
        'goout': [3, 2, 4],
        'Dalc': [1, 1, 2],
        'Walc': [1, 2, 3],
        'health': [3, 4, 2],
        'absences': [4, 2, 8],
        'school_MS': [1, 0, 1],
        'sex_M': [1, 0, 1],
        'address_U': [1, 0, 1],
        'famsize_LE3': [1, 0, 1],
        'Pstatus_T': [1, 0, 1],
        'Mjob_health': [0, 1, 0],
        'Mjob_other': [0, 0, 1],
        'Mjob_services': [1, 0, 0],
        'Mjob_teacher': [0, 0, 0],
        'Fjob_health': [0, 0, 0],
        'Fjob_other': [1, 0, 1],
        'Fjob_services': [0, 1, 0],
        'Fjob_teacher': [0, 0, 0],
        'reason_home': [1, 0, 1],
        'reason_other': [0, 1, 0],
        'reason_reputation': [0, 0, 0],
        'guardian_mother': [1, 0, 1],
        'guardian_other': [0, 0, 0],
        'schoolsup_yes': [0, 1, 0],
        'famsup_yes': [1, 1, 0],
        'paid_yes': [0, 1, 1],
        'activities_yes': [1, 0, 1],
        'nursery_yes': [1, 1, 0],
        'higher_yes': [1, 1, 1],
        'internet_yes': [1, 1, 0],
        'romantic_yes': [0, 1, 0],
        'subject_portuguese': [1, 1, 0],
        'parent_edu_avg': [3.5, 3.0, 2.5],
        'total_alcohol': [2, 3, 5],
        'has_support': [1, 1, 0]
    }
    
    df_template = pd.DataFrame(sample_data)
    return df_template

def download_template():
    """Generate download button for CSV template"""
    st.subheader("📥 Download Batch Prediction Template")
    
    df_template = create_template_csv()
    
    # Convert to CSV
    csv = df_template.to_csv(index=False)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.download_button(
            label="⬇️ Download Template",
            data=csv,
            file_name="batch_prediction_template.csv",
            mime="text/csv",
            help="Download this template and fill in your student data"
        )
    
    with col2:
        st.info(f"✓ Template includes all {len(FEATURES)} required features with 3 sample rows")
    
    # Show preview
    st.write("**Template Preview:**")
    st.dataframe(df_template, use_container_width=True)
    
    # Feature guide
    with st.expander("📋 Feature Guide"):
        st.write("""
        **Numeric Features:**
        - age: Student age (15-22)
        - Medu/Fedu: Mother/Father education (1-4)
        - traveltime: Travel time to school (1-4)
        - studytime: Study time per week (1-4)
        - failures: Number of past class failures (0-4)
        - famrel: Family relationships (1-5)
        - freetime: Free time after school (1-5)
        - goout: Going out with friends (1-5)
        - Dalc/Walc: Weekday/Weekend alcohol consumption (1-5)
        - health: Current health status (1-5)
        - absences: Number of absences (0-93)
        - parent_edu_avg: Average parent education (1-4)
        - total_alcohol: Total alcohol consumption score
        
        **Binary Features (0 or 1):**
        - school_MS: School (1=MS, 0=GP)
        - sex_M: Gender (1=Male, 0=Female)
        - address_U: Urban address (1=Urban, 0=Rural)
        - famsize_LE3: Family size (1=≤3, 0=>3)
        - Pstatus_T: Parent cohabitation (1=Together, 0=Apart)
        - Mjob_*/Fjob_*: Mother/Father job categories
        - reason_*: Reason for school choice
        - guardian_*: Guardian type
        - schoolsup_yes: Extra school support
        - famsup_yes: Family support
        - paid_yes: Extra paid classes
        - activities_yes: Extracurricular activities
        - nursery_yes: Attended nursery school
        - higher_yes: Wants higher education
        - internet_yes: Internet access at home
        - romantic_yes: In a romantic relationship
        - subject_portuguese: Portuguese subject (1=Yes, 0=Math)
        - has_support: Has any support system
        """)

def validate_columns(df):
    """Validate that uploaded CSV has all required columns"""
    uploaded_cols = set(df.columns)
    required_cols = set(FEATURES)
    
    missing_cols = required_cols - uploaded_cols
    extra_cols = uploaded_cols - required_cols
    
    validation_result = {
        'is_valid': len(missing_cols) == 0,
        'missing_cols': missing_cols,
        'extra_cols': extra_cols,
        'num_rows': len(df)
    }
    
    return validation_result

def check_missing_values(df):
    """Check for missing values in the dataframe"""
    missing_info = {
        'has_missing': df.isnull().any().any(),
        'missing_by_column': df.isnull().sum(),
        'total_missing': df.isnull().sum().sum(),
        'missing_percentage': (df.isnull().sum() / len(df) * 100).round(2)
    }
    
    return missing_info

def handle_missing_values(df):
    """Handle missing values with appropriate strategy"""
    df_processed = df.copy()
    
    for col in df_processed.columns:
        if df_processed[col].isnull().any():
            if df_processed[col].dtype in ['float64', 'int64']:
                # Fill numeric columns with median
                df_processed[col].fillna(df_processed[col].median(), inplace=True)
            else:
                # Fill categorical with mode
                df_processed[col].fillna(df_processed[col].mode()[0], inplace=True)
    
    return df_processed

def process_predictions(df, model, scaler):
    """Process each row through prediction pipeline"""
    df_processed = df.copy()
    
    # Ensure correct column order
    df_processed = df_processed[FEATURES]
    
    # Scale features
    if scaler:
        df_scaled = scaler.transform(df_processed)
        df_scaled = pd.DataFrame(df_scaled, columns=FEATURES)
    else:
        df_scaled = df_processed
    
    # Get predictions and probabilities from Random Forest
    predictions = model.predict(df_scaled)
    probabilities = model.predict_proba(df_scaled)
    
     # Add prediction columns
    df_processed['Risk_Prediction'] = predictions
    df_processed['Risk_Label'] = predictions
    
    # Map probabilities to correct columns based on model.classes_
    for i, class_label in enumerate(model.classes_):
        df_processed[f'Prob_{class_label}_Risk'] = probabilities[:, i]
    
    # Add confidence score
    df_processed['Confidence'] = probabilities.max(axis=1)
    
    return df_processed


def create_summary_statistics(df_results):
    """Create summary statistics and visualizations"""
    st.subheader("📊 Summary Statistics")
    
    # Total students processed
    total_students = len(df_results)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Students Processed", total_students)
    
    with col2:
        avg_confidence = df_results['Confidence'].mean()
        st.metric("Average Confidence", f"{avg_confidence:.2%}")
    
    with col3:
        high_risk_count = (df_results['Risk_Label'] == 'High').sum()
        high_risk_pct = (high_risk_count / total_students * 100)
        st.metric("High Risk Students", f"{high_risk_count} ({high_risk_pct:.1f}%)")
    
    with col4:
        med_risk_count = (df_results['Risk_Label'] == 'Medium').sum()
        med_risk_pct = (med_risk_count / total_students * 100)
        st.metric("Medium Risk Students", f"{med_risk_count} ({med_risk_pct:.1f}%)")
    
    # Risk distribution pie chart
    st.subheader("📈 Risk Distribution")
    
    risk_counts = df_results['Risk_Label'].value_counts()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Pie chart
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Create color mapping for actual labels
        color_map = {
            'Low': '#2ecc71',      # Green
            'Medium': '#f39c12',   # Orange
            'High': '#e74c3c'      # Red
        }
        
        # Get colors based on actual categories present
        colors = [color_map.get(label, '#808080') for label in risk_counts.index]
        
        # Create dynamic explode (only for categories that exist)
        explode = tuple([0.1 if label == 'High' else 0.05 for label in risk_counts.index])
        
        ax.pie(
            risk_counts.values,
            labels=risk_counts.index,
            autopct='%1.1f%%',
            colors=colors,
            explode=explode,
            startangle=90,
            textprops={'fontsize': 12, 'weight': 'bold'}
        )
        ax.set_title('Risk Distribution', fontsize=14, weight='bold', pad=20)
        
        st.pyplot(fig)
    
    with col2:
        # Risk distribution table
        st.write("**Risk Distribution Breakdown:**")
        
        risk_summary = pd.DataFrame({
            'Risk Level': risk_counts.index,
            'Count': risk_counts.values,
            'Percentage': (risk_counts.values / total_students * 100).round(2)
        })
        
        st.dataframe(risk_summary, use_container_width=True, hide_index=True)
    
    # Confidence statistics
    st.subheader("📊 Confidence Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        min_confidence = df_results['Confidence'].min()
        st.metric("Min Confidence", f"{min_confidence:.2%}")
    
    with col2:
        max_confidence = df_results['Confidence'].max()
        st.metric("Max Confidence", f"{max_confidence:.2%}")
    
    with col3:
        median_confidence = df_results['Confidence'].median()
        st.metric("Median Confidence", f"{median_confidence:.2%}")
    
    with col4:
        std_confidence = df_results['Confidence'].std()
        st.metric("Std Dev Confidence", f"{std_confidence:.4f}")
    
    # Confidence distribution histogram
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(df_results['Confidence'], bins=20, color='#3498db', edgecolor='black', alpha=0.7)
    ax.set_xlabel('Confidence Score', fontsize=12, weight='bold')
    ax.set_ylabel('Number of Students', fontsize=12, weight='bold')
    ax.set_title('Confidence Score Distribution', fontsize=14, weight='bold')
    ax.grid(axis='y', alpha=0.3)
    
    st.pyplot(fig)

def validate_csv_format(df, filename):
    """Validate CSV format and handle errors"""
    try:
        # Check if dataframe is empty
        if len(df) == 0:
            st.error("❌ CSV file is empty. Please provide a file with at least one row.")
            return False
        
        # Check for completely empty columns
        if df.isnull().all().any():
            empty_cols = df.columns[df.isnull().all()].tolist()
            st.error(f"❌ The following columns are completely empty: {', '.join(empty_cols)}")
            return False
        
        # Check for non-numeric data in numeric columns
        numeric_features = ['age', 'Medu', 'Fedu', 'traveltime', 'studytime', 'failures', 
                           'famrel', 'freetime', 'goout', 'Dalc', 'Walc', 'health', 
                           'absences', 'parent_edu_avg', 'total_alcohol']
        
        for col in numeric_features:
            if col in df.columns:
                try:
                    pd.to_numeric(df[col], errors='coerce')
                    if df[col].isnull().all():
                        st.warning(f"⚠️ Column '{col}' contains non-numeric values and will be filled with median")
                except:
                    st.warning(f"⚠️ Column '{col}' has invalid data types")
        
        # Check for binary columns (should be 0 or 1)
        binary_features = ['school_MS', 'sex_M', 'address_U', 'famsize_LE3', 'Pstatus_T',
                          'Mjob_health', 'Mjob_other', 'Mjob_services', 'Mjob_teacher',
                          'Fjob_health', 'Fjob_other', 'Fjob_services', 'Fjob_teacher',
                          'reason_home', 'reason_other', 'reason_reputation',
                          'guardian_mother', 'guardian_other', 'schoolsup_yes', 'famsup_yes',
                          'paid_yes', 'activities_yes', 'nursery_yes', 'higher_yes',
                          'internet_yes', 'romantic_yes', 'subject_portuguese', 'has_support']
        
        invalid_binary = []
        for col in binary_features:
            if col in df.columns:
                unique_vals = df[col].dropna().unique()
                non_binary = [v for v in unique_vals if v not in [0, 1]]
                if len(non_binary) > 0:
                    invalid_binary.append(col)
        
        if invalid_binary:
            st.warning(f"⚠️ Binary columns should contain only 0 or 1: {', '.join(invalid_binary)}")
        
        return True
        
    except Exception as e:
        st.error(f"❌ Error validating CSV format: {str(e)}")
        return False

def process_uploaded_csv():
    """Main function to process uploaded CSV"""
    st.subheader("📤 Upload & Process Batch Data")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            # Read CSV with error handling
            try:
                df = pd.read_csv(uploaded_file)
            except pd.errors.ParserError as e:
                st.error(f"❌ CSV parsing error: The file may be malformed. {str(e)}")
                return
            except UnicodeDecodeError:
                st.error("❌ Encoding error: The file may not be a valid UTF-8 CSV file.")
                return
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
                return
            
            # Validate CSV format
            if not validate_csv_format(df, uploaded_file.name):
                return
            
            # Step 1: Validate columns
            st.write("**Step 1: Validating Columns...**")
            validation = validate_columns(df)
            
            if not validation['is_valid']:
                st.error(f"❌ Validation Failed")
                if validation['missing_cols']:
                    st.error(f"Missing columns: {', '.join(validation['missing_cols'])}")
                if validation['extra_cols']:
                    st.warning(f"Extra columns (will be ignored): {', '.join(validation['extra_cols'])}")
                return
            else:
                st.success(f"✓ All {len(FEATURES)} required columns present")
                st.info(f"✓ {validation['num_rows']} rows ready for processing")
            
            # Step 2: Check missing values
            st.write("**Step 2: Checking Missing Values...**")
            missing_info = check_missing_values(df)
            
            if missing_info['has_missing']:
                st.warning(f"⚠️ Found {missing_info['total_missing']} missing values")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("Missing values by column:")
                    missing_cols = missing_info['missing_by_column'][missing_info['missing_by_column'] > 0]
                    if len(missing_cols) > 0:
                        st.dataframe(missing_cols)
                
                with col2:
                    st.write("Missing percentage:")
                    missing_pct = missing_info['missing_percentage'][missing_info['missing_percentage'] > 0]
                    if len(missing_pct) > 0:
                        st.dataframe(missing_pct)
                
                # Handle missing values
                with st.spinner("Handling missing values..."):
                    df = handle_missing_values(df)
                st.success("✓ Missing values handled")
            else:
                st.success("✓ No missing values found")
            
            # Step 3: Load models and process predictions
            st.write("**Step 3: Running Prediction Pipeline...**")
            
            with st.spinner("Loading model..."):
                model = load_models()
                scaler = load_scaler()
            
            if model is None:
                st.error("❌ Model failed to load. Cannot proceed with predictions.")
                return
            
            with st.spinner("Processing predictions..."):
                df_results = process_predictions(df, model, scaler)
            
            st.success("✓ Predictions completed")

            # Display summary statistics
            create_summary_statistics(df_results)
            
            # Filtering and Sorting Section
            st.subheader("🔍 Filter & Sort Results")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                risk_filter = st.multiselect(
                    "Filter by Risk Level:",
                    options=['Low', 'Medium', 'High'],
                    default=['Low', 'Medium', 'High'],
                    help="Select which risk levels to display"
                )

            
            with col2:
                sort_by = st.selectbox(
                    "Sort by:",
                    options=[
                        'Risk Level (High to Low)',
                        'Risk Level (Low to High)',
                        'Confidence (High to Low)',
                        'Confidence (Low to High)',
                        'Student ID / Row Number'
                    ],
                    help="Choose how to sort the results"
                )
            
            with col3:
                show_high_risk_only = st.checkbox(
                    "⚠️ Show only High Risk students",
                    value=False,
                    help="Quickly filter to see only students at high risk"
                )
            
            # Apply filters
            df_filtered = df_results[df_results['Risk_Label'].isin(risk_filter)].copy()
            
            if show_high_risk_only:
                df_filtered = df_filtered[df_filtered['Risk_Label'] == 'High Risk'].copy()
            
            # Apply sorting
            if sort_by == 'Risk Level (High to Low)':
                df_filtered = df_filtered.sort_values('Risk_Prediction', ascending=False)
            elif sort_by == 'Risk Level (Low to High)':
                df_filtered = df_filtered.sort_values('Risk_Prediction', ascending=True)
            elif sort_by == 'Confidence (High to Low)':
                df_filtered = df_filtered.sort_values('Confidence', ascending=False)
            elif sort_by == 'Confidence (Low to High)':
                df_filtered = df_filtered.sort_values('Confidence', ascending=True)
            else:  # Default sort by index
                df_filtered = df_filtered.reset_index(drop=True)
            
            # Display filtered results
            st.write(f"**Showing {len(df_filtered)} of {len(df_results)} students**")
            
            # Format display dataframe
            display_cols = ['Risk_Label', 'Risk_Prediction', 'Prob_Low_Risk', 
                           'Prob_Medium_Risk', 'Prob_High_Risk', 'Confidence']
            
            df_display = df_filtered[display_cols].copy()
            df_display['Prob_Low_Risk'] = df_display['Prob_Low_Risk'].apply(lambda x: f"{x:.2%}")
            df_display['Prob_Medium_Risk'] = df_display['Prob_Medium_Risk'].apply(lambda x: f"{x:.2%}")
            df_display['Prob_High_Risk'] = df_display['Prob_High_Risk'].apply(lambda x: f"{x:.2%}")
            df_display['Confidence'] = df_display['Confidence'].apply(lambda x: f"{x:.2%}")
            
            # Display with styling
            st.dataframe(
                df_display,
                use_container_width=True,
                height=400,
                hide_index=False
            )
            
            # Download section
            st.subheader("💾 Download Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Download filtered results
                csv_filtered = df_filtered.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download Filtered Results (CSV)",
                    data=csv_filtered,
                    file_name="batch_predictions_filtered.csv",
                    mime="text/csv",
                    help="Download the filtered and sorted results"
                )
            
            with col2:
                # Download all results
                csv_all = df_results.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download All Results (CSV)",
                    data=csv_all,
                    file_name="batch_predictions_all.csv",
                    mime="text/csv",
                    help="Download all predictions without filters"
                )
            
            # Summary statistics for filtered results
            if len(df_filtered) > 0:
                st.subheader("📈 Filtered Results Summary")
                
                summary_col1, summary_col2, summary_col3 = st.columns(3)
                
                with summary_col1:
                    filtered_low = (df_filtered['Risk_Label'] == 'Low').sum()
                    st.metric("Low Risk (Filtered)", filtered_low)
                
                with summary_col2:
                    filtered_med = (df_filtered['Risk_Label'] == 'Medium').sum()
                    st.metric("Medium Risk (Filtered)", filtered_med)
                
                with summary_col3:
                    filtered_high = (df_filtered['Risk_Label'] == 'High').sum()
                    st.metric("High Risk (Filtered)", filtered_high)
            else:
                st.warning("No results match the selected filters")
        
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}")
            st.info("Please check your file format and try again.")

# Main function
def main():
    st.set_page_config(page_title="Batch Predictions", layout="wide")
    st.title("🎓 Batch Student Performance Predictions")
    
    # Add tabs for template and processing
    tab1, tab2 = st.tabs(["📥 Download Template", "📤 Process Data"])
    
    with tab1:
        download_template()
    
    with tab2:
        process_uploaded_csv()

if __name__ == "__main__":
    main()
