# utils/sentiment_analysis.py
from textblob import TextBlob

def analyze_sentiment(text: str) -> str:
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"

def add_sentiment_to_news(news: list[dict]) -> list[dict]:
    for item in news:
        content = f"{item['title']}. {item['description']}"
        item["sentiment"] = analyze_sentiment(content)
    return news
