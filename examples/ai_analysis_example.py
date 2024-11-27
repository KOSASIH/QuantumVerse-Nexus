# ai_analysis_example.py
from src.ai.analytics import Analytics
from src.ai.sentiment_analysis import SentimentAnalysis

def perform_ai_analysis():
    """Example of using AI analytics to analyze transaction patterns and market sentiment."""
    
    # Example transaction data (replace with actual transaction data)
    transaction_data = [
        {'amount': 100, 'timestamp': '2023-10-01T12:00:00Z'},
        {'amount': 200, 'timestamp': '2023-10-01T12:05:00Z'},
        {'amount': 150, 'timestamp': '2023-10-01T12:10:00Z'},
        {'amount': 300, 'timestamp': '2023-10-01T12:15:00Z'},
    ]

    # Perform analytics on transaction patterns
    analytics = Analytics()
    transaction_summary = analytics.analyze_transaction_patterns(transaction_data)
    print("Transaction Summary:")
    print(transaction_summary)

    # Example social media data for sentiment analysis (replace with actual data)
    social_media_data = [
        "I love using this blockchain!",
        "The transaction fees are too high.",
        "Great project with a bright future!",
        "I'm not sure about the security."
    ]

    # Perform sentiment analysis
    sentiment_analysis = SentimentAnalysis()
    sentiment_results = sentiment_analysis.analyze_sentiment(social_media_data)
    print("Sentiment Analysis Results:")
    print(sentiment_results)

if __name__ == "__main__":
    perform_ai_analysis()
