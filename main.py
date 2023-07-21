from flask import Flask, render_template
import requests
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

app = Flask(__name__)

ENDPOINT = 'https://newsapi.org/v2/top-headlines'
API_KEY = 'your key'

# Create an instance of the SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

@app.route('/')
def get_news():
    params = {
        'country': 'in',
        'apiKey': API_KEY
    }

    response = requests.get(ENDPOINT, params=params)
    news_data = response.json()

    articles = news_data['articles']

    readable_news = []

    for article in articles:
        title = article['title']
        description = article['description']
        source = article['source']['name']
        url = article['url']
        image_url = article['urlToImage']

        if not image_url:
            continue

        # Perform sentiment analysis on the description
        scores = sid.polarity_scores(description)
        sentiment_score = scores['compound']

        if sentiment_score >= 0.05:
            sentiment = 'Positive'
        elif sentiment_score <= -0.05:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'

        news_item = {
            'title': title,
            'description': description,
            'source': source,
            'url': url,
            'image_url': image_url,
            'sentiment': sentiment
        }

        readable_news.append(news_item)

    return render_template('news.html', items=readable_news)

if __name__ == '__main__':
    app.run(debug=True)
