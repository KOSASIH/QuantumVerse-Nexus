import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class RiskManagement:
    """A comprehensive risk management system."""

    def __init__(self, data):
        """
        Initialize the RiskManagement class with data.
        
        :param data: A DataFrame containing the transaction or portfolio data to analyze.
        """
        self.data = data
        self.model = None
        self.scaler = None

    def preprocess_data(self):
        """Preprocess the data for modeling."""
        logging.info("Preprocessing data...")
        self.data.fillna(0, inplace=True)
        self.data['transaction_amount'] = self.data['transaction_amount'].astype(float)
        self.data['risk_level'] = self.data['risk_level'].astype(int)

    def calculate_risk_score(self):
        """Calculate a risk score based on transaction data."""
        logging.info("Calculating risk scores...")
        self.data['risk_score'] = (self.data['transaction_amount'] / self.data['transaction_amount'].max()) * 100
        self.data['risk_level'] = np.where(self.data['risk_score'] > 75, 1, 0)  # 1 = High Risk, 0 = Low Risk

    def train_model(self):
        """Train a Random Forest model for risk classification."""
        logging.info("Training the risk classification model...")
        X = self.data.drop(columns=['risk_level'])
        y = self.data['risk_level']

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Create a pipeline with scaling and model
        self.scaler = StandardScaler()
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

        # Fit the model
        self.model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = self.model.predict(X_test)
        print(classification_report(y_test, y_pred))
        print(confusion_matrix(y_test, y_pred))

    def save_model(self, filename='risk_management_model.pkl'):
        """Save the trained model to a file."""
        joblib.dump(self.model, filename)
        logging.info(f"Model saved to {filename}")

    def load_model(self, filename='risk_management_model.pkl'):
        """Load a trained model from a file."""
        self.model = joblib.load(filename)
        logging.info(f"Model loaded from {filename}")

    def predict_risk(self, new_data):
        """Predict risk on new transaction data."""
        if self.model is None:
            raise Exception("Model is not trained or loaded.")
        
        new_data_scaled = self.scaler.transform(new_data)
        predictions = self.model.predict(new_data_scaled)
        return predictions

    def generate_risk_report(self):
        """Generate a comprehensive risk report."""
        logging.info("Generating risk report...")
        high_risk_count = self.data[self.data['risk_level'] == 1].shape[0]
        low_risk_count = self.data[self.data['risk_level'] == 0].shape[0]
        
        report = {
            'Total Transactions': self.data.shape[0],
            'High Risk Transactions': high_risk_count,
            'Low Risk Transactions': low_risk_count,
            'High Risk Percentage': (high_risk_count / self.data.shape[0]) * 100
        }
        
        print("=== Risk Management Report ===")
        for key, value in report.items():
            print(f"{key}: {value}")
        print("==============================")

# Example usage
if __name__ == "__main__":
    # Sample data creation for demonstration
    data = {
        'transaction_id': range(1, 101),
        'user_id': np.random.randint(1, 20, 100),
        'transaction_amount': np.random.uniform(1, 1000, 100),
        'risk_level': np.random.choice([0, 1], 100, p=[0.8, 0.2])  # 80% low risk, 20% high risk
    }
    
    df = pd.DataFrame(data)

    risk_management = RiskManagement(df)
    risk_management.preprocess_data()
    risk_management.calculate_risk_score()
    risk_management.train_model()
    risk_management.save_model()

    # Simulate new transactions for prediction
    new_transactions = pd.DataFrame({
        'user_id': [21, 22],
        'transaction_amount': [500, 1500]  # One is likely to be high risk
    })

    predictions = risk_management.predict_risk(new_transactions)
    print(f"Predictions for new transactions: {predictions}")

    # Generate a risk report
    risk_management.generate_risk_report()
