# 🎓 Student Academic Performance Prediction

**Predicting student academic performance based on study habits, engagement, and demographic factors**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Project Overview

This project builds a data-driven Streamlit web application that predicts student academic performance in secondary education. Using machine learning and interactive visualizations, the app helps educators identify at-risk students early and understand the key factors that influence academic success.

**Key Goal:** Enable early intervention by predicting final grades (G3) without requiring mid-term grades (G1, G2), allowing schools to support struggling students from the start of the academic year.

---

## 📊 Dataset Information

### Source
- **Name:** UCI Student Performance Dataset
- **Link:** [https://archive.ics.uci.edu/dataset/320/student+performance](https://archive.ics.uci.edu/dataset/320/student+performance)
- **Research Paper:** Cortez, P., & Silva, A. M. G. (2008). "Using Data Mining to Predict Secondary School Student Performance"
- **Data Collection:** School reports and questionnaires from two Portuguese secondary schools

### Dataset Composition
- **Math Course:** 395 students
- **Portuguese Course:** 649 students
- **Combined Dataset:** 1,044 total records
- **Features:** 33 attributes + 1 target variable (G3)
- **Missing Values:** None
- **Date Range:** 2005-2006 academic year

### Key Features

#### Demographics (8 features)
- `school`: Student's school (GP or MS)
- `sex`: Student's gender (F/M)
- `age`: Student's age (15-22)
- `address`: Home address type (Urban/Rural)
- `famsize`: Family size (≤3 or >3)
- `Pstatus`: Parent cohabitation status
- `Medu`: Mother's education level (0-4)
- `Fedu`: Father's education level (0-4)

#### Academic & Study Habits (8 features)
- `studytime`: Weekly study time (1: <2hrs, 2: 2-5hrs, 3: 5-10hrs, 4: >10hrs)
- `failures`: Number of past class failures (0-4)
- `schoolsup`: Extra educational school support (yes/no)
- `famsup`: Family educational support (yes/no)
- `paid`: Extra paid classes (yes/no)
- `activities`: Extra-curricular activities (yes/no)
- `nursery`: Attended nursery school (yes/no)
- `higher`: Wants to pursue higher education (yes/no)

#### Social & Behavioral (11 features)
- `romantic`: In a romantic relationship (yes/no)
- `famrel`: Quality of family relationships (1-5)
- `freetime`: Free time after school (1-5)
- `goout`: Going out with friends (1-5)
- `Dalc`: Workday alcohol consumption (1-5)
- `Walc`: Weekend alcohol consumption (1-5)
- `health`: Current health status (1-5)
- `absences`: Number of school absences (0-93)
- `traveltime`: Home to school travel time (1-4)
- `reason`: Reason for choosing school
- `guardian`: Student's guardian

#### Target Variable
- **G3:** Final grade (0-20, Portuguese grading system)
- **Risk Categories:**
  - High Risk: G3 < 10 (below 50%)
  - Medium Risk: G3 = 10-13 (50-65%)
  - Low Risk: G3 ≥ 14 (70%+)

---

## 🎯 Project Goals

### Primary Objectives
1. **Predict final grades (G3)** using only demographic, social, and behavioral features (without G1/G2)
2. **Classify students** into risk categories for targeted intervention
3. **Identify key factors** that most strongly influence academic performance
4. **Provide actionable insights** for educators through interactive visualizations

### Success Metrics
- **Prediction Accuracy:** Target ≥70% accuracy (baseline without G1/G2)
- **Model Interpretability:** Feature importance clearly explained
- **User Experience:** Intuitive app interface for non-technical users
- **Deployment:** Publicly accessible Streamlit app

---

## 🛠️ Technologies Used

### Core Stack
- **Python 3.11** - Programming language
- **Streamlit** - Web app framework
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning

### Visualization
- **Plotly** - Interactive charts
- **Matplotlib** - Static visualizations
- **Seaborn** - Statistical graphics

### Development Tools
- **Jupyter Notebook** - Exploratory analysis
- **Git/GitHub** - Version control
- **Conda** - Environment management

---

## 👥 Team Members

| Name | GitHub |
|------|--------|
| **Pratik** | [@pratikkmane](https://github.com/pratikkmane) |
| **Emmanuel** | [@eatilola] (https://github.com/eatilola) |
| **Yugant** | TBD |
| **Hamza** | TBD |

---

## 📂 Project Structure

```
student-performance/
├── data/
│   ├── student-mat.csv              # Raw Math dataset
│   ├── student-por.csv              # Raw Portuguese dataset
│   └── processed/
│       └── combined_student_data.csv # Merged dataset (1,044 records)
├── notebooks/
│   ├── 01_initial_exploration.ipynb  # Initial data exploration
│   ├── 02_combine_datasets.ipynb     # Dataset merging
│   ├── 03_target_analysis.ipynb      # Target variable analysis
│   └── 04_feature_distributions.ipynb # Feature analysis
├── models/
│   └── (saved .pkl model files)
├── pages/
│   ├── 1_Home.py                     # App home page
│   ├── 2_EDA.py                      # Exploratory data analysis
│   ├── 3_Visualizations.py           # Interactive charts
│   ├── 4_Prediction.py               # Grade prediction tool
│   └── 5_About.py                    # Team & project info
├── docs/
│   ├── project_plan.md               # Timeline and milestones
│   ├── team_agreements.md            # Collaboration guidelines
│   └── project_proposal.pdf          # Original proposal
├── app.py                            # Main Streamlit entry point
├── requirements.txt                  # Python dependencies
├── environment.yml                   # Conda environment
└── README.md                         # This file
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Conda (recommended) or pip
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/pratikkmane/student-performance.git
cd student-performance
```

2. **Create and activate conda environment**
```bash
conda env create -f environment.yml
conda activate student-performance
```

Or with pip:
```bash
pip install -r requirements.txt
```

3. **Run the Streamlit app**
```bash
streamlit run app.py
```

4. **Open in browser**
- The app will automatically open at `http://localhost:8501`

---

## 📈 Project Progress

### ✅ Completed (Weeks 2-3)

#### Week 2: Setup & Initial Exploration
- [x] Repository structure created
- [x] GitHub collaboration setup (4 members)
- [x] Raw datasets loaded and validated
- [x] Initial exploratory analysis completed
- [x] Basic Streamlit app framework deployed

#### Week 3: Data Combination & Target Analysis
- [x] **Dataset Merging** (Emmanuel)
  - Combined Math and Portuguese datasets
  - Created unified dataset with 1,044 records
  - Added subject identifier column
  - Implemented risk categorization (High/Medium/Low)
  - Saved processed dataset
  
- [x] **Target Variable Analysis** (Yugant)
  - Analyzed G3 distribution across subjects
  - Created grade distribution visualizations
  - Calculated performance statistics
  - Documented subject-specific patterns
  
- [x] **Feature Distribution Analysis** (Hamza)
  - Visualized key features (studytime, failures, parent education, absences, age)
  - Created histograms and boxplots
  - Identified interesting patterns in student characteristics
  
- [x] **Project Documentation** (Pratik)
  - Comprehensive README with project details
  - Project timeline and milestones
  - Team collaboration agreements
  - Repository organization

### 🔄 In Progress (Week 4)
- [ ] Deep feature correlation analysis
- [ ] Feature engineering (new derived variables)
- [ ] Data encoding for categorical variables
- [ ] Baseline model development

### 📋 Upcoming

#### Week 5: EDA Finalization & Model Planning
- Comprehensive EDA summary
- Model selection and justification
- App page structure design

#### Weeks 6-11: MVP Development
- Machine learning model training
- Model evaluation and tuning
- Streamlit app page development
- Interactive feature implementation

#### Weeks 12-15: Deployment & Polish
- Streamlit Community Cloud deployment
- User testing and bug fixes
- Final documentation and presentation

---

## 🔬 Methodology

### Exploratory Data Analysis
1. **Data Quality Assessment** - Check for missing values, outliers, data types
2. **Univariate Analysis** - Distribution of each feature
3. **Bivariate Analysis** - Relationships between features and target (G3)
4. **Multivariate Analysis** - Correlation matrices, feature interactions

### Modeling Approach
1. **Data Preprocessing**
   - Handle categorical variables (one-hot encoding, label encoding)
   - Feature scaling (standardization/normalization)
   - Train-test split (80/20)
   
2. **Model Selection**
   - Decision Trees (baseline, interpretable)
   - Random Forest (improved accuracy)
   - Logistic Regression (for classification)
   - Support Vector Machines (if needed)
   
3. **Evaluation Metrics**
   - Accuracy, Precision, Recall, F1-Score
   - Confusion Matrix
   - Feature Importance Analysis
   - Cross-validation scores

4. **Model Interpretation**
   - SHAP values for explainability
   - Feature contribution analysis
   - Scenario testing ("what-if" analysis)

---

## 📊 Key Findings (Preliminary)

### Dataset Characteristics
- **Grade Distribution:** Grades range from 0-20, with mean around 10-11
- **Pass Rate:** Approximately 70% of students score 10 or above
- **Subject Differences:** Portuguese students have slightly better average performance than Math students
- **Data Quality:** No missing values, well-structured dataset

### Early Insights
- Study time shows positive correlation with final grades
- Past failures are strong negative predictors
- Parent education level correlates with student performance
- School support programs show mixed results
- High absence rates strongly associated with lower grades

*(Full analysis will be documented as EDA progresses)*

---

## 🌐 Deployment

**Live App:** Coming in Week 12  
**Platform:** Streamlit Community Cloud  
**URL:** TBD

---

## 📝 Academic Context

**Course:** INFO-H501 Intro to Data Science Programming
**Institution:** Indiana University Indianapolis
**Semester:** Spring 2026  
**Instructor:** Prof. Leon Johnson

This project fulfills the final project requirement for building a publicly accessible, data-driven Streamlit web application that serves a social or human-centered purpose.

---

## 📚 References

1. Cortez, P., & Silva, A. M. G. (2008). Using Data Mining to Predict Secondary School Student Performance. *Proceedings of 5th Annual Future Business Technology Conference*, EUROSIS, pp. 5-12.

2. UCI Machine Learning Repository. (2014). Student Performance Data Set. https://archive.ics.uci.edu/dataset/320/student+performance

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- UCI Machine Learning Repository for providing the dataset
- Paulo Cortez and Alice Silva for the original research
- Course instructors and TAs for guidance and support
- Gabriel Pereira and Mousinho da Silveira schools for data collection

---

## 📧 Contact

For questions or feedback about this project, please open an issue on GitHub or contact the team lead:

**Pratik Mane**  
Email: [manep@iu.edu]  
GitHub: [@pratikkmane](https://github.com/pratikkmane)

---

**Last Updated:** February 2026  
**Project Status:** 🟢 Active Development (Week 3 of 15)
