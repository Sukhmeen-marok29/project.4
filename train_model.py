import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

def load_and_clean_data(filepath):
    """
    Loads the Excel dataset file cleanly using the openpyxl engine.
    """
    print(f"Reading dataset rows from '{filepath}'...")
    df = pd.read_excel(filepath, engine='openpyxl')
    
    # Standardizing column names (removing accidental spaces and converting to lowercase)
    df.columns = [col.strip().lower() for col in df.columns]
    
    # Identify the target variable column based on dataset layout
    target_col = 'production'
    if target_col not in df.columns:
        if 'quantity' in df.columns:
            target_col = 'quantity'
        else:
            target_col = df.columns[-1]
        
    df = df.dropna(subset=[target_col])
    
    # Handle missing values safely
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].fillna('Unknown')
        else:
            df[col] = df[col].fillna(df[col].median())
            
    return df, target_col

def build_pipeline(categorical_features, numerical_features):
    """
    Creates a machine learning pipeline structure using OneHotEncoder and Random Forest.
    """
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
        ])
    
    model_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1))
    ])
    
    return model_pipeline

def main():
    # Use the newly extracted excel file path
    data_path = "crop_production.xlsx"
    
    try:
        df, target_column = load_and_clean_data(data_path)
        print(f"Target column detected successfully: '{target_column}'")
        
        # Match feature requirements parameters
        categorical_cols = ['crop', 'variety', 'state', 'season', 'recommended zone']
        numerical_cols = ['cost'] 
        
        # Verify columns exist in the file layout
        categorical_cols = [c for c in categorical_cols if c in df.columns]
        numerical_cols = [n for n in numerical_cols if n in df.columns]
        
        X = df[categorical_cols + numerical_cols]
        y = df[target_column]
        
        # Save unique dropdown options for Streamlit selection boxes
        ui_dropdown_options = {}
        for col in categorical_cols:
            ui_dropdown_options[col] = sorted(df[col].unique().tolist())
            
        with open('dropdown_options.pkl', 'wb') as f:
            pickle.dump(ui_dropdown_options, f)
        
        # Split data split frames
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        print("Training Random Forest Regressor Model (This may take a brief moment)...")
        pipeline = build_pipeline(categorical_cols, numerical_cols)
        pipeline.fit(X_train, y_train)
        
        # Evaluate model metrics
        y_pred = pipeline.predict(X_test)
        print("\n--- Model Evaluation Metrics ---")
        print(f"R2 Score (Accuracy): {r2_score(y_test, y_pred):.4f}")
        print(f"Mean Absolute Error: {mean_absolute_error(y_test, y_pred):.2f}")
        
        print("\nSaving trained model pipeline to 'crop_model.pkl'...")
        with open('crop_model.pkl', 'wb') as f:
            pickle.dump(pipeline, f)
        print("✨ Model files generated and saved successfully!")
        
    except Exception as e:
        print(f"❌ Error running training pipeline: {e}")

if __name__ == "__main__":
    main()