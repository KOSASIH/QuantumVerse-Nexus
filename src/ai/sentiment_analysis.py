import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class SentimentAnalysis:
    """A comprehensive sentiment analysis system."""

    def __init__(self, data):
        """
        Initialize the SentimentAnalysis class with data.
        
        :param data: A DataFrame containing the text data for sentiment analysis.
        """
        self.data = data
        self.vectorizer = None
        self.model = None

    def preprocess_text(self):
        """Preprocess the text data."""
        logging.info("Preprocessing text data...")
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')

        lemmatizer = WordNetLemmatizer()
        stop_words = set(stopwords.words('english'))

        self.data['text'] = self.data['text'].apply(lambda x: x.lower())
        self.data['text'] = self.data['text'].apply(word_tokenize)
        self.data['text'] = self.data['text'].apply(lambda x: [lemmatizer.lemmatize(word) for word in x if word not in stop_words])
        self.data['text'] = self.data['text'].apply(lambda x: ' '.join(x))

    def split_data(self):
        """Split the data into training and testing sets."""
        X = self.data['text']
        y = self.data['sentiment']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test

    def build_vectorizer(self):
        """Build a TF-IDF vectorizer."""
        self.vectorizer = TfidfVectorizer(max_features=5000)
        return self.vectorizer

    def train_model(self):
        """Train a sentiment classification model."""
        logging.info("Training the sentiment classification model...")
        X_train, X_test, y_train, y_test = self.split_data()
        vectorizer = self.build_vectorizer()

        X_train_tfidf = vectorizer.fit_transform(X_train)
        X_test_tfidf = vectorizer.transform(X_test)

        self.model = SVC(kernel='linear', C=1)
        self.model.fit(X_train_tfidf, y_train)

        # Evaluate the model
        y_pred = self.model.predict(X_test_tfidf)
        print(classification_report(y_test, y_pred))
        print(confusion_matrix(y_test, y_pred))

    def save_model(self, filename='sentiment_analysis_model.pkl'):
        """Save the trained model to a file."""
        joblib.dump(self.model, filename)
        logging.info(f"Model saved to {filename}")

    def load_model(self, filename='sentiment_analysis_model.pkl'):
        """Load a trained model from a file."""
        self.model = joblib.load(filename)
        logging.info(f"Model loaded from {filename}")

    def predict(self, new_text):
        """Predict the sentiment of new text."""
        if self.model is None:
            raise Exception("Model is not trained or loaded.")
        
        new_text_tfidf = self.vectorizer.transform([new_text])
        prediction = self.model.predict(new_text_tfidf)
        return prediction

    def visualize_results(self):
        """Visualize the sentiment analysis results."""
        logging.info("Visualizing sentiment analysis results...")
        plt.figure(figsize=(10, 8))
        sns.countplot(x='sentiment', data=self.data)
        plt.title("Sentiment Distribution")
        plt.show()

# Example usage
if __name__ == "__main__":
    # Sample data creation for demonstration
    data = {
        'text': ['This is a great product!', 'I love this product.', 'This product is terrible.', 'I hate this product.'],
        'sentiment': [1, 1, 0, 0]  # 1 = Positive, 0 = Negative
    }
    
    df = pd.DataFrame(data)

    sentiment_analysis = SentimentAnalysis(df)
    sentiment_analysis.preprocess_text()
    sentiment_analysis.train_model()
    sentiment_analysis.save_model()

    # Simulate new text for prediction
    new_text = "I'm very satisfied with this product."
    prediction = sentiment_analysis.predict(new_text)
    print(f"Predicted sentiment: {prediction}")

    # Visualize the results
    sentiment_analysis.visualize_results()
