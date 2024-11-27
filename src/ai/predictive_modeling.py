import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class PredictiveModeling:
    """A comprehensive predictive modeling system."""

    def __init__(self, data):
        """
        Initialize the PredictiveModeling class with data.
        
        :param data: A DataFrame containing the data to analyze.
        """
        self.data = data
        self.model = None
        self.scaler = None

    def preprocess_data(self):
        """Preprocess the data for modeling."""
        logging.info("Preprocessing data...")
        self.data.fillna(0, inplace=True)
        self.data['target'] = self.data['target'].astype(int)  # Ensure target is integer

    def split_data(self):
        """Split the data into training and testing sets."""
        X = self.data.drop(columns=['target'])
        y = self.data['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test

    def build_pipeline(self):
        """Build a machine learning pipeline."""
        self.scaler = StandardScaler()
        model = RandomForestClassifier(random_state=42)
        pipeline = Pipeline([
            ('scaler', self.scaler),
            ('classifier', model)
        ])
        return pipeline

    def train_model(self):
        """Train the predictive model."""
        logging.info("Training the predictive model...")
        X_train, X_test, y_train, y_test = self.split_data()
        pipeline = self.build_pipeline()

        # Hyperparameter tuning
        param_grid = {
            'classifier__n_estimators': [50, 100, 200],
            'classifier__max_depth': [None, 10, 20, 30]
        }
        grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy')
        grid_search.fit(X_train, y_train)

        self.model = grid_search.best_estimator_

        # Evaluate the model
        y_pred = self.model.predict(X_test)
        print(classification_report(y_test, y_pred))
        print(confusion_matrix(y_test, y_pred))

    def save_model(self, filename='predictive_model.pkl'):
        """Save the trained model to a file."""
        joblib.dump(self.model, filename)
        logging.info(f"Model saved to {filename}")

    def load_model(self, filename='predictive_model.pkl'):
        """Load a trained model from a file."""
        self.model = joblib.load(filename)
        logging.info(f"Model loaded from {filename}")

    def predict(self, new_data):
        """Predict outcomes on new data."""
        if self.model is None:
            raise Exception("Model is not trained or loaded.")
        
        new_data_scaled = self.scaler.transform(new_data)
        predictions = self.model.predict(new_data_scaled)
        return predictions

# Example usage
if __name__ == "__main__":
    # Sample data creation for demonstration
    data = {
        'feature1': np.random.rand(100),
        'feature2': np.random.rand(100),
        'feature3': np.random.rand(100),
        'target': np.random.choice([0, 1], 100, p=[0.7, 0.3])  # 70% class 0, 30% class 1
    }
    
    df = pd.DataFrame(data)

    predictive_modeling = PredictiveModeling(df)
    predictive_modeling.preprocess_data()
    predictive_modeling.train_model()
    predictive_modeling.save_model()

    # Simulate new data for prediction
    new_data = pd.DataFrame({
        'feature1': [0.5, 0.8],
        'feature2': [0.2, 0.9],
        'feature3': [0.3, 0.4]
    })

    predictions = predictive_modeling.predict(new_data)
    print(f"Predictions for new data: {predictions}")
