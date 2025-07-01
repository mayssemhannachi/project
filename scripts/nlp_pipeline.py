from langdetect import detect
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pymongo import MongoClient
import sys

def nlp_process(text):
    try:
        lang = detect(text) if text else 'unknown'
    except:
        lang = 'unknown'
    
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(text)
    sentiment = 'positive' if sentiment_scores['compound'] > 0.05 else 'negative' if sentiment_scores['compound'] < -0.05 else 'neutral'
    
    return {
        'language': lang,
        'sentiment': sentiment,
        'sentiment_score': sentiment_scores['compound']
    }

def process_nlp_collection():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['harcelement']
        collection = db['posts']
        
        for doc in collection.find():
            text = doc.get('Text_cleaned', doc['Text'])
            nlp_results = nlp_process(text)
            collection.update_one(
                {'_id': doc['_id']},
                {'$set': nlp_results}
            )
        print("✅ NLP processing completed.")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        client.close()

if __name__ == "__main__":
    process_nlp_collection()