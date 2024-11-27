import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

class AnomalyDetection:
    def __init__(self, contamination=0.1):
        self.contamination = contamination
        self.isolation_forest = IsolationForest(contamination=self.contamination, random_state=42)
        self.local_outlier_factor = LocalOutlierFactor(n_neighbors=20, contamination=self.contamination)
        self.scaler = StandardScaler()

    def fit_isolation_forest(self, data):
        """Fit the Isolation Forest model to the data."""
        data_scaled = self.scaler.fit_transform(data)
        self.isolation_forest.fit(data_scaled)

    def fit_local_outlier_factor(self, data):
        """Fit the Local Outlier Factor model to the data."""
        data_scaled = self.scaler.fit_transform(data)
        self.local_outlier_factor.fit(data_scaled)

    def predict_isolation_forest(self, data):
        """Predict anomalies using the Isolation Forest model."""
        data_scaled = self.scaler.transform(data)
        predictions = self.isolation_forest.predict(data_scaled)
        return predictions

    def predict_local_outlier_factor(self, data):
        """Predict anomalies using the Local Outlier Factor model."""
        data_scaled = self.scaler.transform(data)
        predictions = self.local_outlier_factor.fit_predict(data_scaled)
        return predictions

    def visualize_results(self, data, predictions, model_name):
        """Visualize the results of the anomaly detection."""
        plt.figure(figsize=(10, 6))
        plt.title(f'Anomaly Detection using {model_name}')
        plt.scatter(data.iloc[:, 0], data.iloc[:, 1], c=predictions, cmap='coolwarm', edgecolor='k', s=50)
        plt.xlabel('Feature 1')
        plt.ylabel('Feature 2')
        plt.colorbar(label='Anomaly Score')
        plt.show()

# Example usage
if __name__ == "__main__":
    # Generate sample data
    # In practice, you would load your dataset here
    np.random.seed(42)
    normal_data = np.random.normal(loc=0, scale=1, size=(200, 2))
    anomaly_data = np.random.uniform(low=-4, high=4, size=(20, 2))
    data = np.vstack((normal_data, anomaly_data))
    df = pd.DataFrame(data, columns=['Feature 1', 'Feature 2'])

    anomaly_detector = AnomalyDetection(contamination=0.1)

    # Fit models
    anomaly_detector.fit_isolation_forest(df)
    anomaly_detector.fit_local_outlier_factor(df)

    # Predict anomalies
    isolation_forest_predictions = anomaly_detector.predict_isolation_forest(df)
    local_outlier_factor_predictions = anomaly_detector.predict_local_outlier_factor(df)

    # Convert predictions to binary (1 for normal, -1 for anomaly)
    isolation_forest_predictions = np.where(isolation_forest_predictions == -1, 1, 0)
    local_outlier_factor_predictions = np.where(local_outlier_factor_predictions == -1, 1, 0)

    # Visualize results
    anomaly_detector.visualize_results(df, isolation_forest_predictions, "Isolation Forest")
    anomaly_detector.visualize_results(df, local_outlier_factor_predictions, "Local Outlier Factor")
