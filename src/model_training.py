import pandas as pd
import numpy as np
from pathlib import Path


def load_train_validation_data(target='risk_category'):
    """
    Load pre-split and validated train/validation data.
    
    Parameters:
        target (str): Target variable to predict. Options:
            - 'risk_category': Predict High/Medium/Low risk (default)
            - 'G3': Predict exact final grade (0-20)
    
    Returns:
        tuple: (X_train, X_val, y_train, y_val, feature_names)
    """
    try:
        print("Loading train/validation data...")
        print("=" * 60)
        
        if target not in ['risk_category', 'G3']:
            raise ValueError(f"Invalid target '{target}'. Must be 'risk_category' or 'G3'")
        
        data_path = Path(__file__).parent.parent / 'data' / 'processed'
        
        print(f"\n[1/3] Loading training data...")
        X_train = pd.read_csv(data_path / 'X_train.csv')
        y_train_g3 = pd.read_csv(data_path / 'y_train.csv').values.ravel()
        
        print(f"[2/3] Loading validation data...")
        X_val = pd.read_csv(data_path / 'X_val.csv')
        y_val_g3 = pd.read_csv(data_path / 'y_val.csv').values.ravel()
        
        feature_names = X_train.columns.tolist()
        
        # Convert target if needed
        if target == 'risk_category':
            print(f"[3/3] Converting G3 to risk categories...")
            # Apply risk categorization: High (<10), Medium (10-13), Low (>=14)
            y_train = pd.cut(y_train_g3, bins=[-1, 9, 13, 20], labels=['High', 'Medium', 'Low']).astype(str)
            y_val = pd.cut(y_val_g3, bins=[-1, 9, 13, 20], labels=['High', 'Medium', 'Low']).astype(str)
        else:
            print(f"[3/3] Using G3 as target...")
            y_train = y_train_g3
            y_val = y_val_g3
        
        X_train = X_train.values
        X_val = X_val.values
        
        print("\n" + "=" * 60)
        print("Dataset Information:")
        print("=" * 60)
        print(f"  Training samples: {len(X_train)}")
        print(f"  Validation samples: {len(X_val)}")
        print(f"  Number of features: {len(feature_names)}")
        print(f"  Target variable: {target}")
        
        if target == 'risk_category':
            unique, counts = np.unique(y_train, return_counts=True)
            print(f"  Classes: {unique}")
            print(f"  Class distribution (train):")
            for cls, count in zip(unique, counts):
                print(f"    {cls}: {count} ({count/len(y_train)*100:.1f}%)")
        
        print("\n✓ Train/validation data ready for modeling!")
        print("=" * 60)
        
        return X_train, X_val, y_train, y_val, feature_names
        
    except Exception as e:
        print(f"\nError loading data: {e}")
        raise


def train_random_forest(X_train, y_train, X_val, y_val, n_iter=50):
    """
    Train a Random Forest classifier with RandomizedSearchCV hyperparameter tuning.

    Mirrors the tuning approach in notebooks/15_random_forest.ipynb so the
    Streamlit app (Week 6) can retrain the model from the UI without needing
    to re-run the full notebook.

    Parameters:
        X_train (np.ndarray): Training features (scaled)
        y_train (np.ndarray): Training target labels (risk_category strings)
        X_val (np.ndarray): Validation features (scaled)
        y_val (np.ndarray): Validation target labels
        n_iter (int): Number of RandomizedSearchCV iterations (default 50)

    Returns:
        tuple: (best_model, best_params, val_accuracy)
            - best_model: Trained RandomForestClassifier with best parameters
            - best_params: Dictionary of best hyperparameters found
            - val_accuracy: Validation accuracy of the best model (float)

    Example:
        >>> X_train, X_val, y_train, y_val, features = load_train_validation_data()
        >>> model, params, acc = train_random_forest(X_train, y_train, X_val, y_val)
        >>> print(f"Validation accuracy: {acc:.4f}")
    """
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import RandomizedSearchCV, StratifiedKFold
    from sklearn.metrics import accuracy_score

    try:
        print("Training Random Forest model with RandomizedSearchCV...")
        print("=" * 60)

        param_dist = {
            'n_estimators': [100, 200, 300, 500],
            'max_depth': [5, 8, 10, 12, 15, None],
            'min_samples_split': [5, 10, 15, 20],
            'min_samples_leaf': [2, 4, 5, 8],
            'max_features': ['sqrt', 'log2'],
            'class_weight': ['balanced', 'balanced_subsample', None],
        }

        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

        search = RandomizedSearchCV(
            estimator=RandomForestClassifier(random_state=42, n_jobs=-1),
            param_distributions=param_dist,
            n_iter=n_iter,
            cv=cv,
            scoring='accuracy',
            random_state=42,
            n_jobs=-1,
            verbose=0,
        )

        print(f"\nRunning RandomizedSearchCV ({n_iter} iterations, 5-fold CV)...")
        search.fit(X_train, y_train)

        best_model = search.best_estimator_
        best_params = search.best_params_
        val_accuracy = accuracy_score(y_val, best_model.predict(X_val))

        print(f"\n✓ RandomizedSearchCV complete!")
        print(f"  Best CV score (train):  {search.best_score_*100:.2f}%")
        print(f"  Validation accuracy:    {val_accuracy*100:.2f}%")
        print(f"  Best params: {best_params}")

        if val_accuracy >= 0.70:
            print("\n🎉 SUCCESS: Achieved 70%+ target!")
        elif val_accuracy >= 0.65:
            print("\n✓ Good: Above 65% minimum (Week 5 success criterion)")
        else:
            print(f"\n⚠️  Below 65% target ({val_accuracy*100:.2f}%)")

        print("\n" + "=" * 60)
        print("✓ Random Forest training complete!")
        print("=" * 60)

        return best_model, best_params, val_accuracy

    except Exception as e:
        print(f"Error training Random Forest: {e}")
        raise


def train_decision_tree(X_train, y_train, X_val, y_val):
    """
    Train a Decision Tree classifier with hyperparameter tuning.
    
    This function trains a Decision Tree model and tunes hyperparameters to find
    the best configuration for predicting student final grades.
    
    Hyperparameters tuned:
    - max_depth: [5, 10, 15, 20]
    - min_samples_split: [10, 20, 50]
    - min_samples_leaf: [5, 10, 20]
    
    Parameters:
        X_train (np.ndarray): Training features
        y_train (np.ndarray): Training target values
        X_val (np.ndarray): Validation features
        y_val (np.ndarray): Validation target values
        
    Returns:
        tuple: (best_model, best_params, results_df)
            - best_model: Trained DecisionTreeClassifier with best parameters
            - best_params: Dictionary of best hyperparameters
            - results_df: DataFrame with all tuning results
    """
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.metrics import accuracy_score
    import pandas as pd
    
    try:
        print("Training Decision Tree model...")
        print("=" * 60)
        
        # Step 1: Train a baseline model first
        print("\n[1/3] Training baseline Decision Tree...")
        baseline_model = DecisionTreeClassifier(
            random_state=42,
            class_weight="balanced"
        )
        baseline_model.fit(X_train, y_train)
        
        # Evaluate baseline
        train_acc = accuracy_score(y_train, baseline_model.predict(X_train))
        val_acc = accuracy_score(y_val, baseline_model.predict(X_val))
        
        print(f"  Baseline model trained")
        print(f"  Training accuracy: {train_acc:.4f}")
        print(f"  Validation accuracy: {val_acc:.4f}")
        
        # Step 2: Hyperparameter tuning
        print("\n[2/3] Performing hyperparameter tuning...")
        
        # Define hyperparameter grid
        param_grid = {
            'max_depth': [5, 10, 15, 20],
            'min_samples_split': [10, 20, 50],
            'min_samples_leaf': [5, 10, 20]
        }
        
        # Store results
        results = []
        best_val_acc = 0
        best_model = None
        best_params = {}
        
        # Grid search
        total_combinations = len(param_grid['max_depth']) * len(param_grid['min_samples_split']) * len(param_grid['min_samples_leaf'])
        print(f"  Testing {total_combinations} hyperparameter combinations...")
        
        iteration = 0
        for max_depth in param_grid['max_depth']:
            for min_samples_split in param_grid['min_samples_split']:
                for min_samples_leaf in param_grid['min_samples_leaf']:
                    iteration += 1
                    
                    # Train model with current parameters
                    model = DecisionTreeClassifier(
                        max_depth=max_depth,
                        min_samples_split=min_samples_split,
                        min_samples_leaf=min_samples_leaf,
                        class_weight="balanced",
                        random_state=42
                    )
                    model.fit(X_train, y_train)
                    
                    # Evaluate
                    train_accuracy = accuracy_score(y_train, model.predict(X_train))
                    val_accuracy = accuracy_score(y_val, model.predict(X_val))
                    
                    # Store results
                    results.append({
                        'max_depth': max_depth,
                        'min_samples_split': min_samples_split,
                        'min_samples_leaf': min_samples_leaf,
                        'train_accuracy': train_accuracy,
                        'val_accuracy': val_accuracy,
                        'overfit_gap': train_accuracy - val_accuracy
                    })
                    
                    # Update best model
                    if val_accuracy > best_val_acc:
                        best_val_acc = val_accuracy
                        best_model = model
                        best_params = {
                            'max_depth': max_depth,
                            'min_samples_split': min_samples_split,
                            'min_samples_leaf': min_samples_leaf
                        }
                    
                    # Progress update every 10 iterations
                    if iteration % 10 == 0:
                        print(f"    Progress: {iteration}/{total_combinations} combinations tested...")
        
        # Convert results to DataFrame
        results_df = pd.DataFrame(results)
        results_df = results_df.sort_values('val_accuracy', ascending=False)
        
        print(f"\n  ✓ Hyperparameter tuning complete!")
        print(f"  Best validation accuracy: {best_val_acc:.4f}")
        print(f"  Best parameters: {best_params}")
        
        print("\n[3/3] Training final model with best parameters...")
        print(f"  max_depth: {best_params['max_depth']}")
        print(f"  min_samples_split: {best_params['min_samples_split']}")
        print(f"  min_samples_leaf: {best_params['min_samples_leaf']}")
        
        print("\n" + "=" * 60)
        print("✓ Decision Tree training complete!")
        print("=" * 60)
        
        return best_model, best_params, results_df
        
    except Exception as e:
        print(f"Error training decision tree: {e}")
        raise

def predict_validation(model, X_val, y_val):
    """
    Make predictions on the validation set.
    
    This function uses the trained model to predict on validation data
    and returns both predictions and prediction probabilities.
    
    Parameters:
        model: Trained DecisionTreeClassifier
        X_val (np.ndarray): Validation features
        y_val (np.ndarray): Validation target values (for comparison)
        
    Returns:
        tuple: (y_pred, y_pred_proba)
            - y_pred: Predicted class labels (numpy array)
            - y_pred_proba: Prediction probabilities for each class (numpy array)
            
    Example:
        >>> y_pred, y_pred_proba = predict_validation(model, X_val, y_val)
        >>> print(f"Predictions shape: {y_pred.shape}")
    """
    try:
        print("Making predictions on validation set...")
        print("=" * 60)
        
        # Make predictions
        print("\n[1/2] Generating predictions...")
        y_pred = model.predict(X_val)
        
        print("[2/2] Generating prediction probabilities...")
        y_pred_proba = model.predict_proba(X_val)
        
        print(f"\n✓ Predictions complete!")
        print(f"  Validation samples: {len(y_val)}")
        print(f"  Predictions generated: {len(y_pred)}")
        print(f"  Number of classes: {y_pred_proba.shape[1]}")
        
        # Quick preview
        print(f"\nPrediction Preview (first 10 samples):")
        print(f"  Actual:    {y_val[:10]}")
        print(f"  Predicted: {y_pred[:10]}")
        
        print("\n" + "=" * 60)
        print("✓ Prediction complete!")
        print("=" * 60)
        
        return y_pred, y_pred_proba
        
    except Exception as e:
        print(f"Error making predictions: {e}")
        raise

def calculate_metrics(y_true, y_pred):
    """
    Calculate detailed classification metrics for model evaluation.
    """
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
    import pandas as pd
    
    try:
        print("Calculating detailed metrics...")
        print("=" * 60)
        
        # Overall accuracy
        overall_accuracy = accuracy_score(y_true, y_pred)
        
        # Per-class metrics
        classes = ['High', 'Medium', 'Low']
        metrics_data = []
        
        precisions = precision_score(y_true, y_pred, labels=classes, average=None, zero_division=0)
        recalls    = recall_score(   y_true, y_pred, labels=classes, average=None, zero_division=0)
        f1s        = f1_score(       y_true, y_pred, labels=classes, average=None, zero_division=0)

        for i, cls in enumerate(classes):
            metrics_data.append({
                'Risk Category': cls,
                'Precision': precisions[i],
                'Recall':    recalls[i],
                'F1 Score':  f1s[i]
            })
        
        metrics_df = pd.DataFrame(metrics_data)
        
        # Get full classification report
        classification_rep = classification_report(y_true, y_pred, labels=classes)
        
        print(f"✓ Metrics calculated successfully!")
        print("=" * 60)
        
        return {
            'overall_accuracy': overall_accuracy,
            'metrics_df': metrics_df,
            'classification_report': classification_rep
        }
        
    except Exception as e:
        print(f"Error calculating metrics: {e}")
        raise

def visualize_model_insights(model, feature_names, class_names):
    """
    Create visualizations to understand the Decision Tree's logic.
    
    This function generates two key plots:
    1. Feature Importance: Shows which variables the model relied on most.
    2. Tree Structure: Shows the top-level 'if-then' logic of the model.
    
    Parameters:
        model: Trained DecisionTreeClassifier
        feature_names (list): List of names for the 43 features
        class_names (list): List of names for the risk categories
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.tree import plot_tree
    import pandas as pd
    import numpy as np

    try:
        print("Generating model insights and visualizations...")
        print("=" * 60)

        # Create a figure with two subplots
        fig, axes = plt.subplots(2, 1, figsize=(15, 20))

        # 1. Feature Importance Plot
        print("[1/2] Calculating feature importance...")
        importances = model.feature_importances_
        feat_imp_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importances
        }).sort_values(by='Importance', ascending=False).head(10)

        sns.barplot(x='Importance', y='Feature', data=feat_imp_df, ax=axes[0], palette='viridis')
        axes[0].set_title('Top 10 Most Important Features')
        axes[0].set_xlabel('Relative Importance Score')

        # 2. Decision Tree Structure Plot
        print("[2/2] Plotting decision tree structure...")
        plot_tree(model, 
                  feature_names=feature_names, 
                  class_names=class_names, 
                  filled=True, 
                  rounded=True, 
                  max_depth=3, # Limit to 3 levels as per task
                  fontsize=10,
                  ax=axes[1])
        axes[1].set_title('Decision Tree Structure (First 3 Levels)')

        plt.tight_layout()
        plt.show()
        
        print("\n" + "=" * 60)
        print("✓ Visualizations complete!")
        print("=" * 60)

    except Exception as e:
        print(f"Error generating visualizations: {e}")
        raise

def save_model(model, filename):
    """
    Save the trained model to a file using pickle.
    
    Parameters:
        model: The trained model object (e.g., DecisionTreeClassifier)
        filename (str): Name of the file, e.g., 'decision_tree.pkl'
    """
    import pickle
    from pathlib import Path
    
    try:
        # Ensure the models directory exists
        model_dir = Path(__file__).parent.parent / 'models'
        model_dir.mkdir(parents=True, exist_ok=True)
        
        save_path = model_dir / filename
        
        # Save the model
        with open(save_path, 'wb') as f:
            pickle.dump(model, f)
            
        print(f"✓ Model successfully saved to {save_path}")
        
    except Exception as e:
        print(f"Error saving model: {e}")
        raise

