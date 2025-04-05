# modules/sentiment.py

from transformers import pipeline

# Load a sentiment model
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
# Alternatively: "cardiffnlp/twitter-roberta-base-emotion" for emotion classification

def analyze_sentiment(text: str) -> dict:
    """
    Returns sentiment analysis for the provided text.
    For large text, consider chunking or speaker segmentation.
    """
    # This example uses the first 512 characters to avoid token length issues
    chunk = text[:512] if len(text) > 512 else text
    result = sentiment_pipeline(chunk)
    # Typically returns a list, e.g. [{'label': '5 stars', 'score': 0.9}]
    return result[0]
