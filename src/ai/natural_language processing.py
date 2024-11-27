import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from transformers import pipeline
import spacy

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

class NaturalLanguageProcessing:
    def __init__(self):
        # Initialize sentiment analyzer
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        # Load pre-trained transformer model for named entity recognition
        self.ner_model = pipeline("ner", aggregation_strategy="simple")
        # Load spaCy model for advanced NLP tasks
        self.nlp = spacy.load("en_core_web_sm")

    def analyze_sentiment(self, text):
        """Analyze the sentiment of the given text."""
        scores = self.sentiment_analyzer.polarity_scores(text)
        return scores

    def tokenize_text(self, text):
        """Tokenize the input text into words."""
        tokens = word_tokenize(text)
        return tokens

    def remove_stopwords(self, tokens):
        """Remove stopwords from the tokenized words."""
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
        return filtered_tokens

    def named_entity_recognition(self, text):
        """Perform named entity recognition on the input text."""
        entities = self.ner_model(text)
        return entities

    def extract_keywords(self, text):
        """Extract keywords from the text using spaCy."""
        doc = self.nlp(text)
        keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
        return keywords

    def summarize_text(self, text):
        """Summarize the input text using a transformer model."""
        summarizer = pipeline("summarization")
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']

    def chat_response(self, user_input):
        """Generate a response based on user input using a conversational model."""
        chatbot = pipeline("conversational")
        response = chatbot(user_input)
        return response

# Example usage
if __name__ == "__main__":
    nlp_processor = NaturalLanguageProcessing()
    
    sample_text = "The QuantumVerse project is revolutionizing the blockchain space with its innovative features."
    
    sentiment = nlp_processor.analyze_sentiment(sample_text)
    tokens = nlp_processor.tokenize_text(sample_text)
    filtered_tokens = nlp_processor.remove_stopwords(tokens)
    entities = nlp_processor.named_entity_recognition(sample_text)
    keywords = nlp_processor.extract_keywords(sample_text)
    summary = nlp_processor.summarize_text(sample_text)
    response = nlp_processor.chat_response("What do you think about QuantumVerse?")

    print("Sentiment Analysis:", sentiment)
    print("Tokens:", tokens)
    print("Filtered Tokens:", filtered_tokens)
    print("Named Entities:", entities)
    print("Keywords:", keywords)
    print("Summary:", summary)
    print("Chatbot Response:", response)
