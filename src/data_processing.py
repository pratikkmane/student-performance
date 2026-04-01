import pandas as pd
import numpy as np
from pathlib import Path

def load_and_combine_data():
    """
    Load and combine student performance datasets.
    
    This function loads the combined student data CSV file from the processed data directory.
    It handles file path resolution and provides informative error messages if the file is not found.
    
    Returns:
        pd.DataFrame: Combined dataset containing all student-course records with 35 features
        
    Raises:
        FileNotFoundError: If the data file cannot be found at the expected location
        pd.errors.EmptyDataError: If the CSV file is empty
        Exception: For any other errors during file loading
        
    Example:
        >>> df = load_and_combine_data()
        >>> print(f"Loaded {len(df)} records with {df.shape[1]} columns")
        Loaded 1044 records with 35 columns
    """
    try:
        # Define the path to the combined dataset
        data_path = Path('../data/processed/combined_student_data.csv')
        
        # Check if file exists
        if not data_path.exists():
            raise FileNotFoundError(
                f"Data file not found at {data_path}. "
                "Please ensure the combined_student_data.csv file exists in the data/processed directory."
            )
        
        # Load the dataset
        df = pd.read_csv(data_path)
        
        # Validate that data was loaded
        if df.empty:
            raise pd.errors.EmptyDataError("The CSV file is empty.")
        
        print(f"✓ Dataset loaded successfully: {len(df)} student-course records")
        print(f"✓ Columns: {df.shape[1]}")
        
        return df
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
        
    except pd.errors.EmptyDataError as e:
        print(f"Error: {e}")
        raise
        
    except Exception as e:
        print(f"Unexpected error loading data: {e}")
        raise

def create_risk_categories(df):
    """
    Create risk categories based on final grades (G3).
    
    This function categorizes students into risk levels (Low, Medium, High) based on their
    final grade performance. The categories help identify students who may need additional support.
    
    Risk Categories:
    - Low: G3 >= 14 (good performance)
    - Medium: 10 <= G3 <= 13 (average performance)
    - High: G3 <= 9 (at-risk, needs intervention)
    
    Parameters:
        df (pd.DataFrame): DataFrame containing student data with 'G3' column
        
    Returns:
        pd.DataFrame: Original DataFrame with added 'risk_category' column
        
    Raises:
        KeyError: If 'G3' column is not found in the DataFrame
        ValueError: If DataFrame is empty or G3 contains invalid values
        
    Example:
        >>> df = load_and_combine_data()
        >>> df = create_risk_categories(df)
        >>> print(df['risk_category'].value_counts())
        Low       450
        Medium    320
        High      274
    """
    try:
        # Validate input DataFrame
        if df.empty:
            raise ValueError("Input DataFrame is empty.")
        
        # Check if G3 column exists
        if 'G3' not in df.columns:
            raise KeyError(
                "Column 'G3' not found in DataFrame. "
                "Available columns: " + ", ".join(df.columns.tolist())
            )
        
        # Check for valid G3 values
        if df['G3'].isnull().any():
            print(f"Warning: Found {df['G3'].isnull().sum()} missing values in G3. These will be categorized separately.")
        
        # Create risk categories based on G3 (final grade)
        df['risk_category'] = pd.cut(
            df['G3'],
            bins=[-1, 9, 13, 20],
            labels=['High', 'Medium', 'Low'],
            include_lowest=True
        )
        
        # Convert to string for consistency
        df['risk_category'] = df['risk_category'].astype(str)
        
        print(f"✓ Risk categories created successfully")
        print(f"✓ Distribution:")
        print(df['risk_category'].value_counts().sort_index())
        
        return df
        
    except KeyError as e:
        print(f"Error: {e}")
        raise
        
    except ValueError as e:
        print(f"Error: {e}")
        raise
        
    except Exception as e:
        print(f"Unexpected error creating risk categories: {e}")
        raise


def engineer_features(df):
    """
    Engineer new features from existing student data.
    
    This function creates meaningful derived features that can improve model performance
    by capturing relationships and patterns in the data. All features use only baseline
    data available at the start of the year (no G1/G2 grades).
    
    New Features Created (14 total):
    - total_alcohol: Sum of weekday and weekend alcohol consumption (Dalc + Walc)
    - parent_edu_avg: Average of mother's and father's education levels
    - study_time_binary: Binary indicator for high study time (studytime >= 3)
    - failure_flag: Binary indicator for past failures (failures > 0)
    - social_score: Average social activity score (goout + freetime) / 2
    - total_support: Has any academic support (schoolsup OR famsup)
    - study_to_failure_ratio: Study effort relative to past challenges
    - high_absence: Flag for excessive absences (> 10)
    - both_parents_educated: Both parents have secondary education or higher
    - academic_support_score: Count of active academic support channels (0–3)
    - family_quality_score: Family relationship quality + family support
    - health_risk_flag: Poor health indicator (health <= 2)
    - absence_risk_flag: High absence risk (absences > 15)
    - weekend_alcohol_flag: High weekend drinking indicator (Walc >= 4)
    
    Parameters:
        df (pd.DataFrame): DataFrame containing student data with required columns
        
    Returns:
        pd.DataFrame: DataFrame with additional engineered features
        
    Raises:
        KeyError: If required columns are missing from the DataFrame
        ValueError: If DataFrame is empty
        
    Example:
        >>> df = load_and_combine_data()
        >>> df = engineer_features(df)
        >>> print(f"Total features created: 14")
    """
    try:
        # Validate input DataFrame
        if df.empty:
            raise ValueError("Input DataFrame is empty.")
        
        # Required columns for feature engineering
        required_cols = ['Dalc', 'Walc', 'studytime', 'failures', 'Medu', 'Fedu',
                        'goout', 'freetime', 'schoolsup', 'famsup', 'absences',
                        'famrel', 'health', 'paid', 'activities']
        
        # Check if all required columns exist
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise KeyError(
                f"Missing required columns: {', '.join(missing_cols)}. "
                f"Available columns: {', '.join(df.columns.tolist())}"
            )
        
        print("Creating engineered features...")
        print("=" * 60)
        
        # KEEP THESE 5 FEATURES
        
        # 1. Total alcohol consumption
        df['total_alcohol'] = df['Dalc'] + df['Walc']
        print("✓ Created 'total_alcohol' (Dalc + Walc)")
        
        # 2. Parent education average
        df['parent_edu_avg'] = (df['Medu'] + df['Fedu']) / 2
        print("✓ Created 'parent_edu_avg' (average of Medu and Fedu)")
        
        # 3. Study time binary (high vs low)
        df['study_time_binary'] = (df['studytime'] >= 3).astype(int)
        print("✓ Created 'study_time_binary' (studytime >= 3)")
        
        # 4. Failure flag
        df['failure_flag'] = (df['failures'] > 0).astype(int)
        print("✓ Created 'failure_flag' (failures > 0)")
        
        # 5. Social score
        df['social_score'] = (df['goout'] + df['freetime']) / 2
        print("✓ Created 'social_score' (average of goout + freetime)")
        
        # ADD THESE 4 NEW FEATURES
        
        # 6. Total support (school OR family support)
        df['total_support'] = ((df['schoolsup'] == 'yes') | (df['famsup'] == 'yes')).astype(int)
        print("✓ Created 'total_support' (has schoolsup OR famsup)")
        
        # 7. Study to failure ratio
        df['study_to_failure_ratio'] = df['studytime'] / (df['failures'] + 1)
        print("✓ Created 'study_to_failure_ratio' (studytime / (failures + 1))")
        
        # 8. High absence flag
        df['high_absence'] = (df['absences'] > 10).astype(int)
        print("✓ Created 'high_absence' (absences > 10)")
        
        # 9. Both parents educated
        df['both_parents_educated'] = ((df['Medu'] >= 3) & (df['Fedu'] >= 3)).astype(int)
        print("✓ Created 'both_parents_educated' (Medu >= 3 AND Fedu >= 3)")

        # --- 5 NEW FEATURES (added to improve model accuracy) ---

        # 10. Academic support score — how many academic support channels active
        df['academic_support_score'] = (
            (df['schoolsup'] == 'yes').astype(int) +
            (df['paid'] == 'yes').astype(int) +
            (df['activities'] == 'yes').astype(int)
        )
        print("✓ Created 'academic_support_score' (schoolsup + paid + activities)")

        # 11. Family quality score — relationship quality + family support
        df['family_quality_score'] = df['famrel'] + (df['famsup'] == 'yes').astype(int)
        print("✓ Created 'family_quality_score' (famrel + famsup)")

        # 12. Health risk flag — poor health (1–2 on 1–5 scale) signals dropout risk
        df['health_risk_flag'] = (df['health'] <= 2).astype(int)
        print("✓ Created 'health_risk_flag' (health <= 2)")

        # 13. Absence risk flag — stricter threshold than high_absence (>10)
        df['absence_risk_flag'] = (df['absences'] > 15).astype(int)
        print("✓ Created 'absence_risk_flag' (absences > 15)")

        # 14. Weekend alcohol flag — high weekend drinking (4–5 on 1–5 scale)
        df['weekend_alcohol_flag'] = (df['Walc'] >= 4).astype(int)
        print("✓ Created 'weekend_alcohol_flag' (Walc >= 4)")

        print("=" * 60)
        print(f"✓ Feature engineering completed successfully!")
        print(f"✓ Total new features created: 14")
        print(f"✓ New dataset shape: {df.shape}")
        
        return df
        
    except KeyError as e:
        print(f"Error: {e}")
        raise
        
    except ValueError as e:
        print(f"Error: {e}")
        raise
        
    except Exception as e:
        print(f"Unexpected error during feature engineering: {e}")
        raise



def split_and_scale_data(X, y):
    """
    Split data into training and testing sets, then scale the features.
    
    This function performs train-test split and applies StandardScaler to normalize
    features, which is essential for many machine learning algorithms.
    
    Parameters:
        X (pd.DataFrame or np.ndarray): Feature matrix
        y (pd.Series or np.ndarray): Target variable (G3 grades)
        
    Returns:
        tuple: (X_train, X_test, y_train, y_test, scaler)
            - X_train: Scaled training features
            - X_test: Scaled testing features
            - y_train: Training target values
            - y_test: Testing target values
            - scaler: Fitted StandardScaler object (for inverse transform if needed)
            
    Raises:
        ValueError: If X or y are empty, or if shapes don't match
        
    Example:
        >>> df = load_and_combine_data()
        >>> X = df.drop(['G3', 'risk_category'], axis=1)
        >>> y = df['G3']
        >>> X_train, X_test, y_train, y_test, scaler = split_and_scale_data(X, y)
        >>> print(f"Training set size: {len(X_train)}, Test set size: {len(X_test)}")
    """
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    
    try:
        # Validate inputs
        if len(X) == 0:
            raise ValueError("Feature matrix X is empty.")
        
        if len(y) == 0:
            raise ValueError("Target variable y is empty.")
        
        if len(X) != len(y):
            raise ValueError(
                f"Shape mismatch: X has {len(X)} samples but y has {len(y)} samples."
            )
        
        print("Splitting and scaling data...")
        print("=" * 60)
        
        # Split data into train and test sets (80-20 split)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=0.2, 
            random_state=42,
            stratify=None  # Can stratify by risk_category if needed
        )
        
        print(f"✓ Data split completed (80-20 split)")
        print(f"  Training samples: {len(X_train)}")
        print(f"  Testing samples: {len(X_test)}")
        
        # Initialize and fit scaler on training data only
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        print(f"✓ Feature scaling completed (StandardScaler)")
        print(f"  Features scaled: {X_train.shape[1]}")
        print(f"  Mean of scaled training data: {X_train_scaled.mean():.6f}")
        print(f"  Std of scaled training data: {X_train_scaled.std():.6f}")
        
        print("=" * 60)
        print(f"✓ Split and scale completed successfully!")
        
        return X_train_scaled, X_test_scaled, y_train, y_test, scaler
        
    except ValueError as e:
        print(f"Error: {e}")
        raise
        
    except Exception as e:
        print(f"Unexpected error during split and scale: {e}")
        raise


def load_processed_data():
    """
    Load preprocessed and ready-to-use data for modeling.
    
    This is a convenience function that combines all preprocessing steps:
    loading data, creating risk categories, and engineering features.
    Returns data ready for model training.
    
    Returns:
        tuple: (X, y, df_processed)
            - X: Feature matrix (all numeric features except G3)
            - y: Target variable (G3 final grades)
            - df_processed: Full processed DataFrame with all features
            
    Raises:
        FileNotFoundError: If the data file cannot be found
        Exception: For any errors during preprocessing
        
    Example:
        >>> X, y, df = load_processed_data()
        >>> print(f"Ready for modeling: {X.shape[0]} samples, {X.shape[1]} features")
        >>> # Can now directly use: X_train, X_test, y_train, y_test, scaler = split_and_scale_data(X, y)
    """
    try:
        print("Loading and preprocessing data...")
        print("=" * 60)
        
        # Step 1: Load data
        print("\n[1/3] Loading combined dataset...")
        df = load_and_combine_data()
        
        # Step 2: Create risk categories
        print("\n[2/3] Creating risk categories...")
        df = create_risk_categories(df)
        
        # Step 3: Engineer features
        print("\n[3/3] Engineering features...")
        df = engineer_features(df)
        
        print("\n" + "=" * 60)
        print("Preparing feature matrix and target variable...")
        print("=" * 60)
        
        # Select only numeric columns for features
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Remove target variables from features
        features_to_exclude = ['G3', 'G1', 'G2']  # Exclude all grade columns except G3 as target
        feature_cols = [col for col in numeric_cols if col not in features_to_exclude]
        
        # Create feature matrix and target
        X = df[feature_cols]
        y = df['G3']
        
        print(f"✓ Feature matrix created: {X.shape}")
        print(f"✓ Target variable created: {y.shape}")
        print(f"✓ Features included: {len(feature_cols)}")
        print(f"\nFeature list:")
        for i, col in enumerate(feature_cols, 1):
            print(f"  {i}. {col}")
        
        print("\n" + "=" * 60)
        print("✓ Data preprocessing pipeline completed successfully!")
        print("=" * 60)
        print(f"Dataset ready for modeling:")
        print(f"  - Total samples: {len(df)}")
        print(f"  - Total features: {X.shape[1]}")
        print(f"  - Target variable: G3 (final grade)")
        print(f"  - Target range: {y.min()}-{y.max()}")
        print(f"  - Target mean: {y.mean():.2f}")
        
        return X, y, df
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise
        
    except Exception as e:
        print(f"Unexpected error during data loading: {e}")
        raise
