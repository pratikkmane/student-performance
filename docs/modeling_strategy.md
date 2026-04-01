# Modeling Strategy

## Objective
The goal of this project is to predict student performance using engineered features derived from the UCI Student Performance dataset. Our target variable is risk_category (High, Medium, Low).

---

## Target Variable
We are predicting:
- risk_category (classification problem)

We are excluding:
- G1
- G2
- G3

to prevent data leakage.

---

## Algorithm Selection

We will start with baseline models:

1. Logistic Regression
2. Decision Tree Classifier
3. Random Forest Classifier

Reasoning:
- Logistic Regression provides a simple baseline.
- Decision Tree helps interpret feature importance.
- Random Forest improves performance and reduces overfitting.

---

## Evaluation Metrics

Since this is a multi-class classification problem, we will evaluate using:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion Matrix

Primary metric:
- Accuracy (target ≥ 70%)

---

## Model Validation Strategy

- Use stratified train/validation/test splits (70/15/15)
- Apply scaling using StandardScaler (fit on training only)
- Prevent data leakage by excluding grade features (G1, G2, G3)
- Tune hyperparameters using validation set

---

## Hyperparameter Tuning Plan

- Logistic Regression: regularization strength (C)
- Decision Tree: max_depth, min_samples_split
- Random Forest: n_estimators, max_depth

---

## Risk Considerations

- Class imbalance
- Overfitting
- Data leakage
- Outliers affecting scaling

---

## Success Criteria

- Validation accuracy ≥ 65% (Week 5 checkpoint)
- Final model accuracy ≥ 70%

---

## Additional Techniques (implemented in Week 5 RF notebook)

### Class Imbalance — SMOTE
High Risk is the minority class (~22% of data). We use SMOTE (Synthetic Minority Oversampling Technique) to generate synthetic samples for the minority class in the training set only. The validation set is never resampled. When SMOTE is used, `class_weight` is not passed to the model (the two strategies should not be combined).

### Comparison Model — Gradient Boosting
A `GradientBoostingClassifier` is trained with fixed parameters (n_estimators=200, max_depth=4, learning_rate=0.1) as a comparison to the Random Forest. If it outperforms the RF on the validation set, it is saved as `gradient_boosting.pkl` for Week 7 consideration.

### Threshold Tuning for High Risk Recall
The default decision threshold (0.5) under-detects High Risk students. We evaluate thresholds from 0.20 to 0.50 and select the threshold that maximises High Risk recall while keeping High Risk precision ≥ 0.45. The best threshold is reported and applied at inference time.