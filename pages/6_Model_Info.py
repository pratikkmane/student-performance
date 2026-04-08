import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from joblib import load
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Model Performance & Info", layout="wide")

st.title("Model Performance & Info")
st.markdown("This page summarizes how the trained models performed and how to interpret the final model.")

BASE_DIR = Path(__file__).resolve().parent.parent


@st.cache_data
def load_validation_data():
    x_path = BASE_DIR / "data" / "processed" / "X_val.csv"
    y_class_path = BASE_DIR / "data" / "processed" / "y_val_class.csv"
    y_reg_path = BASE_DIR / "data" / "processed" / "y_val.csv"

    X_val = pd.read_csv(x_path)

    if y_class_path.exists():
        y_val = pd.read_csv(y_class_path).squeeze("columns")
    elif y_reg_path.exists():
        y_raw = pd.read_csv(y_reg_path).squeeze("columns")
        y_val = pd.cut(
            y_raw,
            bins=[-np.inf, 9, 13, np.inf],
            labels=["High", "Medium", "Low"],
            include_lowest=True
        ).astype(str)
    else:
        raise FileNotFoundError("Could not find y_val_class.csv or y_val.csv")

    return X_val, y_val


@st.cache_resource
def load_models():
    return {
        "Logistic Regression": load(BASE_DIR / "models" / "logistic_regression.pkl"),
        "Decision Tree": load(BASE_DIR / "models" / "decision_tree.pkl"),
        "Random Forest": load(BASE_DIR / "models" / "random_forest.pkl"),
    }


try:
    X_val, y_val = load_validation_data()
    models = load_models()
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

class_order = ["High", "Medium", "Low"]
available_classes = [c for c in class_order if c in set(y_val.astype(str))]


def get_model_predictions(model, X):
    try:
        return model.predict(X)
    except Exception:
        return model.predict(X.values)


def compute_metrics(y_true, y_pred):
    acc = accuracy_score(y_true, y_pred)
    p, r, f1, _ = precision_recall_fscore_support(
        y_true, y_pred,
        labels=available_classes,
        zero_division=0
    )
    return acc, p, r, f1


# -------------------------
# Model evaluation
# -------------------------
results = []
pred_store = {}

for name, model in models.items():
    y_pred = get_model_predictions(model, X_val)
    pred_store[name] = y_pred

    acc, p, r, f1 = compute_metrics(y_val, y_pred)
    high_idx = available_classes.index("High") if "High" in available_classes else 0

    results.append({
        "Model": name,
        "Accuracy": acc,
        "Precision (macro)": float(np.mean(p)),
        "Recall (macro)": float(np.mean(r)),
        "F1 (macro)": float(np.mean(f1)),
        "High Risk Recall": float(r[high_idx]) if len(r) > high_idx else np.nan,
    })

metrics_df = pd.DataFrame(results)
best_model_name = metrics_df.sort_values(
    ["Accuracy", "High Risk Recall"], ascending=False
).iloc[0]["Model"]

# -------------------------
# Top summary
# -------------------------
st.subheader("Performance Summary")

c1, c2, c3 = st.columns(3)
best_row = metrics_df[metrics_df["Model"] == best_model_name].iloc[0]

c1.metric("Best Model", best_model_name)
c2.metric("Accuracy", f"{best_row['Accuracy']:.3f}")
c3.metric("High Risk Recall", f"{best_row['High Risk Recall']:.3f}")

st.dataframe(
    metrics_df.style.format({
        "Accuracy": "{:.3f}",
        "Precision (macro)": "{:.3f}",
        "Recall (macro)": "{:.3f}",
        "F1 (macro)": "{:.3f}",
        "High Risk Recall": "{:.3f}",
    }),
    use_container_width=True
)

# -------------------------
# Accuracy comparison
# -------------------------
st.subheader("Model Comparison")

acc_fig = px.bar(
    metrics_df,
    x="Model",
    y="Accuracy",
    color="Model",
    text=metrics_df["Accuracy"].round(3),
    title="Validation Accuracy Comparison"
)
acc_fig.update_traces(textposition="outside")
acc_fig.update_layout(yaxis_range=[0, 1])
st.plotly_chart(acc_fig, use_container_width=True)

# -------------------------
# Confusion matrix
# -------------------------
st.subheader("Confusion Matrix")

selected_model = st.selectbox("Select a model", list(models.keys()))
view_mode = st.radio("Display mode", ["Counts", "Percentages"], horizontal=True)

y_pred_sel = pred_store[selected_model]
cm = confusion_matrix(y_val, y_pred_sel, labels=available_classes)

if view_mode == "Percentages":
    cm_plot = cm / cm.sum(axis=1, keepdims=True)
    cm_text = np.where(np.isnan(cm_plot), "", (cm_plot * 100).round(1).astype(str) + "%")
    zmin, zmax = 0, 1
    hover_values = cm_plot
    title_suffix = " (Percentages)"
else:
    cm_plot = cm
    cm_text = cm.astype(str)
    zmin, zmax = None, None
    hover_values = cm
    title_suffix = " (Counts)"

cm_fig = go.Figure(
    data=go.Heatmap(
        z=cm_plot,
        x=available_classes,
        y=available_classes,
        colorscale="Blues",
        text=cm_text,
        texttemplate="%{text}",
        zmin=zmin,
        zmax=zmax,
        hovertemplate="Actual=%{y}<br>Predicted=%{x}<br>Value=%{z}<extra></extra>",
    )
)
cm_fig.update_layout(
    title=f"{selected_model} Confusion Matrix{title_suffix}",
    xaxis_title="Predicted",
    yaxis_title="Actual",
    height=500
)
st.plotly_chart(cm_fig, use_container_width=True)

# -------------------------
# Feature importance
# -------------------------
st.subheader("Feature Importance")

rf_model = models["Random Forest"]

if hasattr(rf_model, "feature_importances_"):
    feature_names = X_val.columns.tolist()
    importances = rf_model.feature_importances_

    fi_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": importances
    }).sort_values("Importance", ascending=False).head(20)

    fi_fig = px.bar(
        fi_df.sort_values("Importance"),
        x="Importance",
        y="Feature",
        orientation="h",
        title="Top 20 Feature Importances (Random Forest)"
    )
    fi_fig.update_layout(height=600)
    st.plotly_chart(fi_fig, use_container_width=True)
else:
    st.warning("Feature importance is not available for the selected model.")

# -------------------------
# How the model works
# -------------------------
st.subheader("How the Model Works")

st.markdown(
    """
The app takes student inputs, converts them into the same feature format used during training, 
scales the values, and passes them into the trained model. The model then predicts a risk class 
and returns probabilities for each class.
"""
)

st.code(
    """
User input
  ↓
Feature encoding
  ↓
Scaling
  ↓
Model prediction
  ↓
Risk level + probabilities
"""
)

# -------------------------
# Limitations
# -------------------------
st.subheader("Model Limitations")

st.markdown(
    """
- The model is based on historical data, so it may not capture every real-world situation.
- It should support, not replace, human judgment.
- Predictions depend on the quality of the input data.
- Accuracy is good for a baseline, but not perfect.
"""
)

# -------------------------
# Interpretation guide
# -------------------------
st.subheader("How to Interpret Results")

st.markdown(
    """
- **High Risk**: student may need immediate support or intervention.
- **Medium Risk**: student may benefit from monitoring and early support.
- **Low Risk**: student is generally on track.
"""
)

# -------------------------
# FAQ
# -------------------------
with st.expander("FAQs"):
    st.markdown(
        """
**What does the model predict?**  
It predicts student risk level.

**Why are there three models?**  
We compared Logistic Regression, Decision Tree, and Random Forest before choosing the final model.

**Why is Random Forest selected?**  
It had the best overall performance in validation.
"""
    )

st.markdown("---")
st.caption("Model training date: Week 5 | Version: Final validation model")