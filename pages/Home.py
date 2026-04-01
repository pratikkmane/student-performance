# import streamlit as st
# import pandas as pd
# import numpy as np
# import pickle
# from pathlib import Path
# import sys
# import matplotlib.pyplot as plt
# import seaborn as sns

# # Add src directory to path
# sys.path.append(str(Path(__file__).parent.parent / 'src'))

# from model_training import load_train_validation_data

# # Page configuration
# st.set_page_config(
#     page_title="Home - Student Risk Assessment",
#     page_icon="📊",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for better styling
# st.markdown("""
#     <style>
#     .main {
#         padding-top: 2rem;
#     }
#     .metric-card {
#         background-color: #f0f2f6;
#         padding: 20px;
#         border-radius: 10px;
#         margin: 10px 0;
#     }
#     .high-risk {
#         background-color: #ffebee;
#         border-left: 5px solid #ff4444;
#         padding: 15px;
#         border-radius: 5px;
#     }
#     .medium-risk {
#         background-color: #fff3e0;
#         border-left: 5px solid #ffa500;
#         padding: 15px;
#         border-radius: 5px;
#     }
#     .low-risk {
#         background-color: #e8f5e9;
#         border-left: 5px solid #44aa44;
#         padding: 15px;
#         border-radius: 5px;
#     }
#     .recommendation-box {
#         background-color: #e3f2fd;
#         padding: 15px;
#         border-radius: 8px;
#         margin: 10px 0;
#         border-left: 4px solid #2196f3;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Title and description
# st.title("📊 Student Risk Assessment System")
# st.markdown("""
# This tool predicts student risk levels based on early-year indicators 
# to enable timely intervention and support.
# """)

# # Load the trained Decision Tree model
# @st.cache_resource
# def load_model():
#     """Load the trained Decision Tree model"""
#     try:
#         model_path = Path(__file__).parent.parent / 'models' / 'decision_tree.pkl'
#         with open(model_path, 'rb') as f:
#             model = pickle.load(f)
#         return model
#     except FileNotFoundError:
#         st.error("Model file not found. Please ensure decision_tree.pkl exists in the models folder.")
#         return None

# # Load feature names
# @st.cache_resource
# def load_feature_names():
#     """Load feature names for the model"""
#     try:
#         feature_path = Path(__file__).parent.parent / 'models' / 'feature_names.pkl'
#         with open(feature_path, 'rb') as f:
#             features = pickle.load(f)
#         return features
#     except FileNotFoundError:
#         st.warning("Feature names file not found.")
#         return None

# # Load scaler
# @st.cache_resource
# def load_scaler():
#     """Load the fitted scaler for feature scaling"""
#     try:
#         scaler_path = Path(__file__).parent.parent / 'models' / 'scaler.pkl'
#         with open(scaler_path, 'rb') as f:
#             scaler = pickle.load(f)
#         return scaler
#     except FileNotFoundError:
#         st.warning("Scaler file not found.")
#         return None

# def prepare_input_data(input_dict, feature_names, scaler):
#     """
#     Prepare input data for model prediction.
    
#     Parameters:
#         input_dict: Dictionary of user inputs
#         feature_names: List of feature names in correct order
#         scaler: Fitted StandardScaler object
        
#     Returns:
#         Scaled input array ready for prediction
#     """
#     try:
#         # Create a DataFrame with the input data
#         input_df = pd.DataFrame([input_dict])
        
#         # Reorder columns to match feature names
#         input_df = input_df[feature_names]
        
#         # Scale the features
#         input_scaled = scaler.transform(input_df)
        
#         return input_scaled
#     except Exception as e:
#         st.error(f"Error preparing input data: {e}")
#         return None

# def make_prediction(model, input_scaled):
#     """
#     Make prediction using the trained model.
    
#     Parameters:
#         model: Trained DecisionTreeClassifier
#         input_scaled: Scaled input features
        
#     Returns:
#         Tuple of (prediction, probabilities)
#     """
#     try:
#         prediction = model.predict(input_scaled)[0]
#         probabilities = model.predict_proba(input_scaled)[0]
        
#         return prediction, probabilities
#     except Exception as e:
#         st.error(f"Error making prediction: {e}")
#         return None, None

# def get_recommendations(risk_level):
#     """
#     Get personalized recommendations based on risk level.
    
#     Parameters:
#         risk_level: Predicted risk level (High, Medium, Low)
        
#     Returns:
#         Dictionary with recommendations
#     """
#     recommendations = {
#         "High": {
#             "actions": [
#                 "🎯 Schedule intervention meeting with school counselor",
#                 "📚 Recommend intensive tutoring services",
#                 "📋 Monitor attendance closely (weekly check-ins)",
#                 "👥 Connect with peer mentoring programs",
#                 "📞 Establish regular parent/guardian communication"
#             ],
#             "priority": "URGENT",
#             "timeline": "Within 1 week",
#             "color": "high-risk"
#         },
#         "Medium": {
#             "actions": [
#                 "📅 Check in bi-weekly with student",
#                 "👫 Encourage participation in study groups",
#                 "📊 Review progress at mid-semester",
#                 "💡 Suggest targeted academic support in weak areas",
#                 "🎓 Discuss academic goals and study strategies"
#             ],
#             "priority": "MODERATE",
#             "timeline": "Within 2 weeks",
#             "color": "medium-risk"
#         },
#         "Low": {
#             "actions": [
#                 "✅ Student is on track - continue current efforts",
#                 "🌟 Encourage continued engagement and effort",
#                 "🤝 Consider peer tutoring opportunities (as mentor)",
#                 "🎯 Explore advanced or enrichment programs",
#                 "📈 Set higher academic goals for growth"
#             ],
#             "priority": "MONITOR",
#             "timeline": "Regular monitoring",
#             "color": "low-risk"
#         }
#     }
    
#     return recommendations.get(risk_level, {})

# def get_feature_importance_explanation(model, feature_names, input_dict):
#     """
#     Get feature importance and create explanation of prediction.
    
#     Parameters:
#         model: Trained DecisionTreeClassifier
#         feature_names: List of feature names
#         input_dict: Dictionary of input values
        
#     Returns:
#         DataFrame with top features and their values
#     """
#     try:
#         # Get feature importances from the model
#         importances = model.feature_importances_
        
#         # Create a DataFrame with feature names and importances
#         feature_importance_df = pd.DataFrame({
#             'Feature': feature_names,
#             'Importance': importances,
#             'Student Value': [input_dict.get(feat, 0) for feat in feature_names]
#         }).sort_values('Importance', ascending=False)
        
#         # Get top 5 features
#         top_features = feature_importance_df.head(5)
        
#         return top_features
#     except Exception as e:
#         st.error(f"Error calculating feature importance: {e}")
#         return None

# def create_probability_chart(probabilities, classes):
#     """
#     Create a visual chart for probability breakdown.
    
#     Parameters:
#         probabilities: Array of probabilities for each class
#         classes: List of class names
        
#     Returns:
#         Matplotlib figure
#     """
#     fig, ax = plt.subplots(figsize=(8, 5))
    
#     colors = ['#FF4444', '#FFA500', '#44AA44']
#     bars = ax.barh(classes, probabilities, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
#     # Add percentage labels on bars
#     for i, (bar, prob) in enumerate(zip(bars, probabilities)):
#         ax.text(prob + 0.02, i, f'{prob*100:.1f}%', va='center', fontweight='bold', fontsize=11)
    
#     ax.set_xlabel('Probability', fontsize=12, fontweight='bold')
#     ax.set_xlim(0, 1)
#     ax.set_title('Risk Category Probabilities', fontsize=14, fontweight='bold', pad=20)
#     ax.grid(axis='x', alpha=0.3, linestyle='--')
    
#     plt.tight_layout()
#     return fig

# def create_feature_importance_chart(top_features):
#     """
#     Create a visual chart for feature importance.
    
#     Parameters:
#         top_features: DataFrame with top features
        
#     Returns:
#         Matplotlib figure
#     """
#     fig, ax = plt.subplots(figsize=(8, 5))
    
#     colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(top_features)))
#     bars = ax.barh(top_features['Feature'], top_features['Importance'], color=colors, edgecolor='black', linewidth=1.5)
    
#     # Add value labels on bars
#     for bar, importance in zip(bars, top_features['Importance']):
#         ax.text(importance + 0.01, bar.get_y() + bar.get_height()/2, 
#                 f'{importance:.3f}', va='center', fontweight='bold', fontsize=10)
    
#     ax.set_xlabel('Importance Score', fontsize=12, fontweight='bold')
#     ax.set_title('Top 5 Features Influencing Prediction', fontsize=14, fontweight='bold', pad=20)
#     ax.grid(axis='x', alpha=0.3, linestyle='--')
    
#     plt.tight_layout()
#     return fig

# # Main content
# st.markdown("---")

# # Initialize model and features
# model = load_model()
# feature_names = load_feature_names()
# scaler = load_scaler()

# if model is None or feature_names is None or scaler is None:
#     st.error("❌ Cannot proceed without the trained model, features, and scaler.")
# else:
#     # Create two columns for layout
#     col1, col2 = st.columns([1, 1])
    
#     with col1:
#         st.subheader("📋 Student Input Data")
#         st.info("📝 Enter student information to generate a risk assessment.")
        
#         # Create input form
#         with st.form("student_input_form"):
#             st.markdown("**🎓 Academic Background**")
#             col1a, col1b = st.columns(2)
#             with col1a:
#                 failures = st.slider("Past Failures", 0, 4, 0, help="Number of times student failed a class")
#             with col1b:
#                 studytime = st.slider("Study Time (hours/week)", 1, 4, 2, help="Weekly study hours")
            
#             st.markdown("**🤝 Support Systems**")
#             col2a, col2b = st.columns(2)
#             with col2a:
#                 schoolsup = st.selectbox("School Support", ["No", "Yes"], help="Does student receive extra school support?")
#             with col2b:
#                 famsup = st.selectbox("Family Support", ["No", "Yes"], help="Does family provide educational support?")
            
#             st.markdown("**💪 Personal Factors**")
#             col3a, col3b = st.columns(2)
#             with col3a:
#                 absences = st.slider("Absences", 0, 30, 5, help="Number of school absences")
#             with col3b:
#                 health = st.slider("Health Status (1-5)", 1, 5, 3, help="Self-reported health (1=poor, 5=excellent)")
            
#             st.markdown("**🎉 Behavioral & Social**")
#             col4a, col4b = st.columns(2)
#             with col4a:
#                 goout = st.slider("Going Out (1-5)", 1, 5, 3, help="Frequency of going out (1=very low, 5=very high)")
#             with col4b:
#                 freetime = st.slider("Free Time (1-5)", 1, 5, 3, help="Amount of free time (1=very low, 5=very high)")
            
#             st.markdown("**🍷 Substance Use**")
#             col5a, col5b = st.columns(2)
#             with col5a:
#                 dalc = st.slider("Weekday Alcohol (0-5)", 0, 5, 1, help="Weekday alcohol consumption")
#             with col5b:
#                 walc = st.slider("Weekend Alcohol (0-5)", 0, 5, 1, help="Weekend alcohol consumption")
            
#             st.markdown("**👨‍👩‍👧 Demographics**")
#             col6a, col6b = st.columns(2)
#             with col6a:
#                 age = st.slider("Age", 15, 22, 18)
#             with col6b:
#                 medu = st.slider("Mother's Education (0-4)", 0, 4, 2, help="0=none, 1=primary, 2=5to9, 3=secondary, 4=higher")
            
#             col6c, col6d = st.columns(2)
#             with col6c:
#                 fedu = st.slider("Father's Education (0-4)", 0, 4, 2, help="0=none, 1=primary, 2=5to9, 3=secondary, 4=higher")
#             with col6d:
#                 famsize = st.selectbox("Family Size", ["LE3", "GT3"], help="LE3=Less than or Equal to 3, GT3=greater than 3")
            
#             # Submit button
#             submit_button = st.form_submit_button("🔮 Generate Risk Assessment", use_container_width=True)
    
#     with col2:
#         st.subheader("📈 Prediction Results")
        
#         if submit_button:
#             # Convert inputs to model-compatible format
#             input_dict = {
#                 'failures': failures,
#                 'studytime': studytime,
#                 'schoolsup_yes': 1 if schoolsup == "Yes" else 0,
#                 'famsup_yes': 1 if famsup == "Yes" else 0,
#                 'absences': absences,
#                 'health': health,
#                 'goout': goout,
#                 'freetime': freetime,
#                 'Dalc': dalc,
#                 'Walc': walc,
#                 'age': age,
#                 'Medu': medu,
#                 'Fedu': fedu,
#                 'famsize_GT3': 1 if famsize == "GT3" else 0,
#             }
            
#             # Prepare data for prediction
#             input_scaled = prepare_input_data(input_dict, feature_names, scaler)
            
#             if input_scaled is not None:
#                 # Make prediction
#                 prediction, probabilities = make_prediction(model, input_scaled)
                
#                 if prediction is not None:
#                     # Color coding
#                     if prediction == "High":
#                         color = "🔴"
#                         risk_color = "#FF4444"
#                         css_class = "high-risk"
#                     elif prediction == "Medium":
#                         color = "🟠"
#                         risk_color = "#FFA500"
#                         css_class = "medium-risk"
#                     else:  # Low
#                         color = "🟢"
#                         risk_color = "#44AA44"
#                         css_class = "low-risk"
                    
#                     # Display risk level with styling
#                     st.markdown(f"""
#                     <div class="{css_class}">
#                         <h2 style='margin: 0;'>{color} <b>Risk Level: {prediction}</b></h2>
#                     </div>
#                     """, unsafe_allow_html=True)
                    
#                     # Display confidence
#                     confidence = max(probabilities) * 100
#                     st.metric("🎯 Prediction Confidence", f"{confidence:.1f}%")
                    
#                     # Display probability breakdown with chart
#                     st.markdown("### 📊 Probability Breakdown")
                    
#                     col_chart1, col_chart2 = st.columns([1, 1])
#                     with col_chart1:
#                         fig = create_probability_chart(probabilities, ['High Risk', 'Medium Risk', 'Low Risk'])
#                         st.pyplot(fig, use_container_width=True)
                    
#                     with col_chart2:
#                         classes = ['High', 'Medium', 'Low']
#                         for i, cls in enumerate(classes):
#                             prob = probabilities[i] * 100
#                             st.write(f"**{cls} Risk:** {prob:.1f}%")
#                             st.progress(probabilities[i])
#         else:
#             st.info("📝 Fill in the student information and click 'Generate Risk Assessment' to see results.")
    
#     # Recommendations section (full width)
#     if submit_button and prediction is not None:
#         st.markdown("---")
#         st.markdown("## 💡 Personalized Recommendations")
        
#         # Get recommendations based on risk level
#         rec = get_recommendations(prediction)
        
#         # Display priority and timeline
#         col_rec1, col_rec2, col_rec3 = st.columns(3)
#         with col_rec1:
#             st.metric("🚨 Priority Level", rec["priority"])
#         with col_rec2:
#             st.metric("⏰ Action Timeline", rec["timeline"])
#         with col_rec3:
#             st.metric("📋 Actions Required", len(rec["actions"]))
        
#         # Display action items with styling
#         st.markdown("### ✅ Recommended Actions:")
#         for i, action in enumerate(rec["actions"], 1):
#             st.markdown(f"""
#             <div class="recommendation-box">
#                 <b>{i}. {action}</b>
#             </div>
#             """, unsafe_allow_html=True)
        
#         # Visual representation of actions
#         st.markdown("### 📌 Action Progress Tracker:")
#         for action in rec["actions"]:
#             st.checkbox(action, value=False)
        
#         # Explain Prediction section
#         st.markdown("---")
#         st.markdown("## 🔍 Explain Prediction")
#         st.markdown("### 📌 Top Factors Influencing This Assessment:")
        
#         # Get feature importance explanation
#         top_features = get_feature_importance_explanation(model, feature_names, input_dict)
        
#         if top_features is not None:
#             col_exp1, col_exp2 = st.columns([1.5, 1])
            
#             with col_exp1:
#                 fig = create_feature_importance_chart(top_features)
#                 st.pyplot(fig, use_container_width=True)
            
#             with col_exp2:
#                 st.markdown("### Feature Values:")
#                 for idx, row in top_features.iterrows():
#                     st.write(f"**{row['Feature']}**")
#                     st.metric("Value", f"{row['Student Value']:.2f}", label_visibility="collapsed")
            
#             st.markdown("""
#             #### 📖 What This Means:
#             The factors listed above are the most important predictors of student risk in our model.
#             A higher importance score means that feature has a stronger influence on the prediction.
#             Your student's values for these factors are key drivers of their risk assessment.
#             """)