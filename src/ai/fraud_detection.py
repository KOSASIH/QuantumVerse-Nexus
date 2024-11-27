import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class FraudDetection:
    """A comprehensive fraud detection system."""

    def __init__(self, data):
        """
        Initialize the FraudDetection class with data.
        
        :param data: A DataFrame containing the transaction data to analyze.
        """
        self.data = data
        self.model = None
        self.scaler = None

    def preprocess_data(self):
        """Preprocess the data for modeling."""
        # Example preprocessing steps
        self.data.fillna(0, inplace=True)
        self.data['transaction_amount'] = self.data['transaction_amount'].astype(float)
        self.data['is_fraud'] = self.data['is_fraud'].astype(int)

    def detect_anomalies(self):
        """Use Isolation Forest to detect anomalies in the data."""
        logging.info("Detecting anomalies using Isolation Forest...")
        isolation_forest = IsolationForest(contamination=0.05)
        self.data['anomaly'] = isolation_forest.fit_predict(self.data[['transaction_amount']])
        anomalies = self.data[self.data['anomaly'] == -1]
        logging.info(f"Detected {len(anomalies)} anomalies.")
        return anomalies

    def train_model(self):
        """Train a Random Forest model for fraud detection."""
        logging.info("Training the fraud detection model...")
        X = self.data.drop(columns=['is_fraud', 'anomaly'])
        y = self.data['is_fraud']

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Create a pipeline with scaling and model
        self.scaler = StandardScaler()
        self.model = Pipeline([
            ('scaler', self.scaler),
            ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
        ])

        # Fit the model
        self.model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = self.model.predict(X_test)
        print(classification_report(y_test, y_pred))
        print(confusion_matrix(y_test, y_pred))

    def save_model(self, filename='fraud_detection_model.pkl'):
        """Save the trained model to a file."""
        joblib.dump(self.model, filename)
        logging.info(f"Model saved to {filename}")

    def load_model(self, filename='fraud_detection_model.pkl'):
        """Load a trained model from a file."""
        self.model = joblib.load(filename)
        logging.info(f"Model loaded from {filename}")

    def predict(self, new_data):
        """Predict fraud on new transaction data."""
        if self.model is None:
            raise Exception("Model is not trained or loaded.")
        
        new_data_scaled = self.scaler.transform(new_data)
        predictions = self.model.predict(new_data_scaled)
        return predictions

    def real_time_monitoring(self, new_transactions):
        """Monitor new transactions in real-time for fraud detection."""
        logging.info("Monitoring new transactions for fraud...")
        anomalies = self.detect_anomalies()
        predictions = self.predict(new_transactions)
        return anomalies, predictions

# Example usage
if __name__ == "__main__":
    # Sample data creation for demonstration
    data = {
        'transaction_id': range(1, 101),
        'user_id': np.random.randint(1, 20, 100),
        'transaction_amount': np.random.uniform(1, 1000, 100),
        'is_fraud': np.random.choice([0, 1], 100, p=[0.9, 0.1])
    }
    
    df = pd.DataFrame(data)

    fraud_detection = FraudDetection(df)
    fraud_detection.preprocess_data()
    fraud_detection.detect_anomalies()
    fraud_detection.train_model()
    fraud_detection.save_model()

    # Simulate new transactions for prediction
    new_transactions = pd.DataFrame({
        'user_id': [21, 22],
        'transaction_amount': [500, 1500]  # One is likely to be fraudulent
    })

    predictions = fraud_detection.predict(new_transactions)
    print(f"Predictions for new transactions: {predictions}")
