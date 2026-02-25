# Project Plan & Timeline

**Project:** Student Academic Performance Prediction  
**Duration:** 15 Weeks (Week 2 - Week 15)  
**Team:** Pratik, Emmanuel, Yugant, Hamza  

---

## Project Phases Overview

```
Phase 1: Discovery (Weeks 2-5)          ████████░░░░░░░ 4 weeks
Phase 2: MVP Development (Weeks 6-11)   ░░░░░░░░████████ 6 weeks  
Phase 3: Deployment (Weeks 12-15)       ░░░░░░░░░░░░░░██ 4 weeks
```

---

## Detailed Week-by-Week Plan

### PHASE 1: DISCOVERY (WEEKS 2-5)

#### **Week 2: Repository Setup & Initial Exploration** ✅ COMPLETED
**Dates:** Feb 11-17, 2026  
**Status:** ✅ Done

**Goals:**
- Set up GitHub repository with proper structure
- All team members clone and access repository
- Load and validate both datasets
- Initial data exploration

**Deliverables:**
- ✅ GitHub repository created with folder structure
- ✅ All 4 team members added as collaborators
- ✅ Math dataset loaded (395 records)
- ✅ Portuguese dataset loaded (649 records)
- ✅ Initial exploration notebook created
- ✅ README with basic project description
- ✅ First Stand-up Meeting completed

**Commits:** 8+ commits across team

---

#### **Week 3: Dataset Combination & Analysis** ✅ COMPLETED
**Dates:** Feb 18-24, 2026  
**Status:** ✅ Done

**Goals:**
- Combine Math and Portuguese datasets
- Analyze target variable (G3) distribution
- Explore feature distributions
- Complete project documentation

**Individual Tasks:**

| Member | Task | Status | Commits |
|--------|------|--------|---------|
| Emmanuel | Combine datasets, add risk categories | ✅ | 3 |
| Yugant | Target variable analysis & visualizations | ✅ | 3 |
| Hamza | Feature distribution analysis | ✅ | 3 |
| Pratik | Project documentation & README | ✅ | 3 |

**Deliverables:**
- ✅ Combined dataset: `data/processed/combined_student_data.csv` (1,044 records)
- ✅ Target analysis notebook with 3-4 visualizations
- ✅ Feature distribution notebook
- ✅ Comprehensive README
- ✅ `docs/project_plan.md` (this file)
- ✅ `docs/team_agreements.md`

**Commits:** 12+ commits across team

---

#### **Week 4: Deep EDA & Feature Engineering** 🔄 IN PROGRESS
**Dates:** Feb 25 - Mar 3, 2026  
**Status:** 🔄 In Progress

**Goals:**
- Deep dive into feature correlations
- Create new engineered features
- Encode categorical variables
- Prepare data for modeling

**Individual Tasks:**

| Member | Task | Expected Commits |
|--------|------|------------------|
| Pratik | Correlation analysis, create heatmaps | 2-3 |
| Emmanuel | Feature engineering (new derived variables) | 2-3 |
| Yugant | Encode categorical variables for modeling | 2-3 |
| Hamza | Identify feature interactions, outlier analysis | 2-3 |

**Deliverables:**
- [ ] Correlation analysis notebook with heatmaps
- [ ] Engineered features (e.g., parent_edu_avg, total_alcohol)
- [ ] Encoded dataset ready for ML
- [ ] Outlier analysis report
- [ ] Updated data preprocessing pipeline

**Target Commits:** 10-12 commits

**Stand-up Meeting:** Wednesday, Feb 26
- What we completed last week
- Current challenges (if any)
- Plan for this week

---

#### **Week 5: EDA Summary & Model Planning**
**Dates:** Mar 4-10, 2026  
**Status:** 📋 Planned

**Goals:**
- Finalize all EDA work
- Write comprehensive findings summary
- Research and select ML algorithms
- Design Streamlit app structure

**Individual Tasks:**

| Member | Task | Expected Commits |
|--------|------|------------------|
| Pratik | Write EDA summary document, plan app pages | 2-3 |
| Emmanuel | Data validation, final preprocessing checks | 2-3 |
| Yugant | Research ML algorithms, write comparison doc | 2-3 |
| Hamza | Select top visualizations for app (Plotly) | 2-3 |

**Deliverables:**
- [ ] `docs/eda_summary.md` with all key findings
- [ ] `docs/model_selection.md` comparing algorithms
- [ ] App wireframe/mockup (can be hand-drawn)
- [ ] GitHub Issues created for each app page
- [ ] Final cleaned dataset

**Milestone:** EDA Phase Complete ✓

---

### PHASE 2: MVP DEVELOPMENT (WEEKS 6-11)

#### **Week 6: Model Development Begins + App Foundation**
**Dates:** Mar 11-17, 2026  
**Status:** 📋 Planned

**Goals:**
- Train first baseline model
- Build Streamlit home page
- Start EDA page in app
- Set up model pipeline

**Individual Tasks:**

| Member | Task | Expected Commits |
|--------|------|------------------|
| Pratik | Build Home page (title, description, dataset preview) | 2-3 |
| Emmanuel | Implement train/test split, create modeling notebook | 2-3 |
| Yugant | Train Decision Tree baseline model | 2-3 |
| Hamza | Build EDA page skeleton with 2-3 charts | 2-3 |

**Deliverables:**
- [ ] Decision Tree model trained (baseline accuracy)
- [ ] Home page functional in Streamlit
- [ ] EDA page with initial charts
- [ ] Model training pipeline documented

---

#### **Week 7: Model Improvement + Interactive Features**
**Dates:** Mar 18-24, 2026  
**Status:** 📋 Planned

**Goals:**
- Train second model (Random Forest)
- Feature importance analysis
- Add interactive filters to visualizations
- Start Prediction page UI

**Individual Tasks:**

| Member | Task | Expected Commits |
|--------|------|------------------|
| Pratik | Compare Decision Tree vs Random Forest | 2-3 |
| Emmanuel | Feature importance visualization | 2-3 |
| Yugant | Implement cross-validation | 2-3 |
| Hamza | Complete Visualizations page with filters | 2-3 |

**Deliverables:**
- [ ] Two models trained and compared
- [ ] Feature importance chart
- [ ] Interactive visualizations with filters
- [ ] Prediction page UI framework

---

#### **Week 8: Model Integration**
**Dates:** Mar 25-31, 2026  
**Status:** 📋 Planned

**Goals:**
- Connect best model to Prediction page
- Implement real-time predictions
- Add model evaluation metrics display

**Individual Tasks:**

| Member | Task | Expected Commits |
|--------|------|------------------|
| Pratik | Save model as .pkl, load in Streamlit | 2-3 |
| Emmanuel | Create prediction input form | 2-3 |
| Yugant | Display accuracy, confusion matrix | 2-3 |
| Hamza | Add prediction result visualization | 2-3 |

**Deliverables:**
- [ ] Functional end-to-end prediction in app
- [ ] Model metrics displayed
- [ ] User can input values and get prediction

**Milestone:** TA Meeting - Present MVP progress

---

#### **Week 9: Testing & Refinement**
**Dates:** Apr 1-7, 2026  
**Status:** 📋 Planned

**Goals:**
- Error handling and validation
- Test edge cases
- Improve user experience
- Add scenario testing feature

**Individual Tasks:**

| Member | Task | Expected Commits |
|--------|------|------------------|
| Pratik | Implement error handling for all inputs | 2-3 |
| Emmanuel | Validate input ranges, add defaults | 2-3 |
| Yugant | Build "what-if" scenario comparison | 2-3 |
| Hamza | Test app thoroughly, file bug Issues | 2-3 |

**Deliverables:**
- [ ] App handles invalid inputs gracefully
- [ ] Scenario testing feature working
- [ ] Bug Issues filed and prioritized

---

#### **Week 10: About Page & Documentation**
**Dates:** Apr 8-14, 2026  
**Status:** 📋 Planned

**Goals:**
- Build About page
- Add model interpretability
- Improve UI design
- Update all documentation

**Individual Tasks:**

| Member | Task | Expected Commits |
|--------|------|------------------|
| Pratik | Build About page (team info, background) | 2-3 |
| Emmanuel | Add "How to Use" guide to app | 2-3 |
| Yugant | Implement SHAP or feature contribution display | 2-3 |
| Hamza | UI/UX improvements (colors, layout, CSS) | 2-3 |

**Deliverables:**
- [ ] Complete About page
- [ ] Model interpretation feature
- [ ] Polished UI design

---

#### **Week 11: Final MVP Testing**
**Dates:** Apr 15-21, 2026  
**Status:** 📋 Planned

**Goals:**
- Cross-team testing
- Bug fixes
- Code cleanup
- Prepare for deployment

**Tasks (Everyone):**
- [ ] Each member tests every other member's pages
- [ ] Fix all critical bugs
- [ ] Clean up code (remove comments, add docstrings)
- [ ] Update README with current status

**Deliverables:**
- [ ] Bug-free MVP
- [ ] Clean, documented code
- [ ] README reflects current app state

**Milestone:** MVP Complete ✓

---

### PHASE 3: DEPLOYMENT & VALIDATION (WEEKS 12-15)

#### **Week 12: Deployment**
**Dates:** Apr 22-28, 2026  
**Status:** 📋 Planned

**Goals:**
- Deploy to Streamlit Community Cloud
- Test deployed app
- Fix deployment issues

**Individual Tasks:**

| Member | Task | Expected Commits |
|--------|------|------------------|
| Pratik | Deploy to Streamlit Cloud, configure settings | 1-2 |
| Emmanuel | Test deployment, ensure data loads correctly | 1-2 |
| Yugant | Verify model predictions work on cloud | 1-2 |
| Hamza | Test responsiveness on different devices | 1-2 |

**Deliverables:**
- [ ] Live Streamlit app URL
- [ ] App works identically to local version
- [ ] README updated with deployment link

**Milestone:** Public App Deployed ✓

---

#### **Week 13: Validation & User Testing**
**Dates:** Apr 29 - May 5, 2026  
**Status:** 📋 Planned

**Goals:**
- Validate predictions make sense
- Get feedback from classmates
- Verify project meets requirements

**Tasks (Everyone):**
- [ ] Test app with real scenarios
- [ ] Collect feedback from 3-5 users
- [ ] Validate against project rubric
- [ ] Document any limitations

**Deliverables:**
- [ ] Validation report
- [ ] User feedback incorporated
- [ ] Rubric checklist completed

---

#### **Week 14: Final Polish**
**Dates:** May 6-12, 2026  
**Status:** 📋 Planned

**Goals:**
- Final bug fixes
- Improve documentation
- Prepare presentation

**Tasks (Everyone):**
- [ ] Fix remaining minor bugs
- [ ] Improve chart labels and formatting
- [ ] Finalize README
- [ ] Prepare 5-minute demo presentation

**Deliverables:**
- [ ] Polished final app
- [ ] Complete documentation
- [ ] Presentation slides

**Milestone:** Final TA Review Meeting

---

#### **Week 15: Submission**
**Dates:** May 13-19, 2026  
**Status:** 📋 Planned

**Goals:**
- Final submission
- Ensure everything is on GitHub
- Celebrate completion

**Tasks (Everyone):**
- [ ] Final commit and push
- [ ] Verify GitHub repo is complete
- [ ] Submit project link to instructor
- [ ] Team retrospective meeting

**Deliverables:**
- [ ] Project submitted
- [ ] GitHub repo complete
- [ ] App publicly accessible

**Milestone:** Project Complete! 🎉

---

## Milestone Summary

| Milestone | Target Date | Status |
|-----------|-------------|--------|
| Repository Setup | Week 2 | ✅ Complete |
| Dataset Combined | Week 3 | ✅ Complete |
| EDA Complete | Week 5 | 📋 Planned |
| First Model Trained | Week 6 | 📋 Planned |
| MVP Complete | Week 11 | 📋 Planned |
| App Deployed | Week 12 | 📋 Planned |
| Final Submission | Week 15 | 📋 Planned |

---

## Risk Management

### Identified Risks

| Risk | Probability | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| Team member unavailable | Medium | High | Cross-training, backup assignments |
| Merge conflicts | Medium | Medium | Frequent pulls, communication |
| Model accuracy too low | Low | High | Try multiple algorithms, feature engineering |
| Deployment issues | Medium | Medium | Test early (Week 12), allocate buffer time |
| Data quality problems | Low | High | Thorough EDA in Phase 1 |

### Contingency Plans

**If we fall behind schedule:**
1. Prioritize core features (prediction working > fancy UI)
2. Cut optional features (advanced interpretability, extra visualizations)
3. Team meeting to redistribute work
4. Instructor consultation for guidance

**If team member drops out:**
1. Redistribute their assignments
2. Focus on deliverables over polish
3. Document what was accomplished
4. Continue with reduced scope if needed

---

## Success Criteria

### Technical Requirements
- [x] Public GitHub repository with 4 collaborators
- [ ] 1,000+ row dataset with 5+ columns
- [ ] Streamlit app with multiple pages
- [ ] Machine learning model predicting target variable
- [ ] Interactive visualizations
- [ ] Deployed to Streamlit Community Cloud

### Evaluation Criteria
- [ ] All members have consistent commit history
- [ ] Everyone can explain all project components
- [ ] Code is well-documented and organized
- [ ] App solves stated problem statement
- [ ] Professional presentation quality

### Learning Objectives
- [ ] Experience full data science pipeline (EDA → modeling → deployment)
- [ ] Practice collaborative coding with Git/GitHub
- [ ] Build production-ready web application
- [ ] Create portfolio-worthy project

---

## Notes & Updates

**Week 3 Update (Feb 24, 2026):**
- On track! All Week 2-3 deliverables completed
- Dataset combination went smoothly (1,044 records confirmed)
- Team collaboration is working well
- Ready to start Week 4 EDA work

---

**Document Maintained By:** Pratik (Team Lead)  
**Last Updated:** February 24, 2026  
**Next Review:** End of Week 5
