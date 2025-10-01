# train_model.py
# Project Aura: v0.5 (The Brain)
# This script reads the logged data, trains a model, and evaluates its accuracy.

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

LOG_FILE = 'aura_log.csv'

def train_aura_model():
    """
    Loads data, trains a RandomForest model, and saves it.
    """
    print("--- Starting Model Training ---")

    # 1. Load the Data
    try:
        df = pd.read_csv(LOG_FILE)
    except FileNotFoundError:
        print(f"Error: Log file not found at '{LOG_FILE}'.")
        print("Please run the app_watcher.py script to collect some data first.")
        return

    if len(df) < 20:
        print(f"Not enough data to train. Found {len(df)} entries, need at least 20.")
        return

    print(f"Loaded {len(df)} data entries.")

    # 2. Prepare the Data (Feature Engineering)
    # Convert app names into numerical features using one-hot encoding
    features = pd.get_dummies(df[['app_name', 'key_presses', 'mouse_clicks']], columns=['app_name'])
    labels = df['label']

    # 3. Split Data into Training and Testing Sets
    # 80% for training, 20% for testing
    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.2, random_state=42, stratify=labels
    )
    print(f"Data split: {len(X_train)} training samples, {len(X_test)} testing samples.")

    # 4. Train the Model
    print("Training the RandomForestClassifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 5. Evaluate the Model
    print("Evaluating model performance...")
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"✅ Model Accuracy: {accuracy * 100:.2f}%")

    # 6. Save the Model and Columns for later use
    model_filename = 'aura_model.joblib'
    columns_filename = 'model_columns.joblib'
    joblib.dump(model, model_filename)
    joblib.dump(features.columns.tolist(), columns_filename)
    print(f"✅ Model saved as '{model_filename}'")
    print(f"✅ Model columns saved as '{columns_filename}'")
    
    print("--- Training Complete ---")

if __name__ == '__main__':
    train_aura_model()
