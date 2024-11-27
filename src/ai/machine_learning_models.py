import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
import joblib

class MachineLearningModels:
    def __init__(self):
        self.models = {
            'random_forest': RandomForestClassifier(),
            'logistic_regression': LogisticRegression(),
            'svm': SVC(probability=True)
        }
        self.scaler = StandardScaler()
        self.imputer = SimpleImputer(strategy='mean')

    def preprocess_data(self, data):
        """Preprocess the input data by handling missing values and scaling."""
        # Impute missing values
        data_imputed = self.imputer.fit_transform(data)
        # Scale features
        data_scaled = self.scaler.fit_transform(data_imputed)
        return data_scaled

    def train_model(self, model_name, X_train, y_train):
        """Train a specified machine learning model."""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} is not defined.")
        
        model = self.models[model_name]
        model.fit(X_train, y_train)
        return model

    def evaluate_model(self, model, X_test, y_test):
        """Evaluate the trained model on the test set."""
        predictions = model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        report = classification_report(y_test, predictions)
        return accuracy, report

    def save_model(self, model, model_name):
        """Save the trained model to a file."""
        joblib.dump(model, f"{model_name}.joblib")

    def load_model(self, model_name):
        """Load a trained model from a file."""
        return joblib.load(f"{model_name}.joblib")

    def detect_anomalies(self, data):
        """Detect anomalies in the data using Isolation Forest and Local Outlier Factor."""
        isolation_forest = IsolationForest(contamination=0.1)
        lof = LocalOutlierFactor(n_neighbors=20)

        # Fit Isolation Forest
        isolation_forest.fit(data)
        isolation_predictions = isolation_forest.predict(data)

        # Fit Local Outlier Factor
        lof_predictions = lof.fit_predict(data)

        return isolation_predictions, lof_predictions

# Example usage
if __name__ == "__main__":
    # Sample data generation
    # In practice, you would load your dataset here
    data = pd.DataFrame({
        'feature1': np.random.rand(100),
        'feature2': np.random.rand(100),
        'label': np.random.randint(0, 2, size=100)
    })

    X = data[['feature1', 'feature2']]
    y = data['label']

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    ml_models = MachineLearningModels()

    # Preprocess the data
    X_train_processed = ml_models.preprocess_data(X_train)
    X_test_processed = ml_models.preprocess_data(X_test)

    # Train a model
    trained_model = ml_models.train_model('random_forest', X_train_processed, y_train)

    # Evaluate the model
    accuracy, report = ml_models.evaluate_model(trained_model, X_test_processed, y_test)
    print("Accuracy:", accuracy)
    print("Classification Report:\n", report)

    # Save the model
    ml_models.save_model(trained_model, 'random_forest_model')

    # Load the model
    loaded_model = ml_models.load_model('random_forest_model')

    # Detect anomalies
    anomalies = ml_models.detect_anomalies(X)
    print("Anomaly Detection Results (Isolation Forest):", anomalies[0])
    print("Anomaly Detection Results (Local Outlier Factor):", anomalies[1])
