# random_forest.py - Trains a Random Forest Classifier on the Aura Log Data

import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# --- CONFIGURATION ---
LOG_FILE = 'aura_log.csv'
MODEL_FILE = 'random_forest_model.joblib' # Name of the file the model will be saved to
TARGET_COLUMN = 'user_state'

# Feature columns MUST match the order and names used in aura_platform_core.py's logs
FEATURE_COLUMNS = [
    'active_app',
    'key_count',
    'mouse_distance',
    'calendar_state' # The powerful new "sense" feature!
]

# Define the features by type for the ColumnTransformer
categorical_features = ['active_app', 'calendar_state']
numerical_features = ['key_count', 'mouse_distance']

# --- PREPROCESSING PIPELINE ---
# This pipeline ensures all data is transformed correctly before hitting the model
preprocessor = ColumnTransformer(
    transformers=[
        # 1. Scale numerical features (important for general good practice)
        ('num', StandardScaler(), numerical_features),
        # 2. One-Hot Encode categorical features (required for Random Forest to use text data)
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ],
    remainder='passthrough' # Keep any other columns (though we use all defined features)
)


def train_random_forest():
    """Loads data, trains the Random Forest model, evaluates, and saves it."""
    
    if not os.path.exists(LOG_FILE):
        print(f"❌ Error: Log file not found at {LOG_FILE}. Please run aura_platform_core.py to collect data first.")
        return

    # 1. Load Data
    try:
        df = pd.read_csv(LOG_FILE)
    except pd.errors.EmptyDataError:
        print(f"❌ Error: Log file {LOG_FILE} is empty. Collect some data!")
        return
        
    # Ensure necessary features are present
    if not all(col in df.columns for col in FEATURE_COLUMNS + [TARGET_COLUMN]):
        print("❌ Error: Log file is missing required columns. Check if the headers match.")
        print(f"Expected: {FEATURE_COLUMNS + [TARGET_COLUMN]}")
        return

    # Remove the timestamp for simplicity
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]
    
    # Drop any rows where the target state is missing (e.g., if logging was interrupted)
    X = X.dropna(subset=[TARGET_COLUMN])
    y = y.dropna()

    # 2. Split Data
    # Stratify=y ensures the training and test sets have the same proportion of focused/distracted states
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training on {len(X_train)} samples, testing on {len(X_test)}.")

    # 3. Define the Full Pipeline
    rf_classifier = RandomForestClassifier(
        n_estimators=150,       # Slightly more trees for better accuracy
        max_depth=12,           # Controls the complexity of individual trees
        random_state=42,
        class_weight='balanced' # Handles situations where one state is much more frequent
    )

    full_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', rf_classifier)
    ])

    # 4. Train the Model
    print("🌳 Starting Random Forest training...")
    full_pipeline.fit(X_train, y_train)
    print("Training complete.")

    # 5. Evaluate Performance
    y_pred = full_pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print("\n--- Model Evaluation ---")
    print(f"Model Accuracy on Test Set: **{accuracy:.4f}**")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # 6. Save the Model
    joblib.dump(full_pipeline, MODEL_FILE)
    print(f"✅ Trained model saved to **{MODEL_FILE}**. The core platform can now use it.")


if __name__ == "__main__":
    train_random_forest()
