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