from elasticsearch import Elasticsearch
from pymongo import MongoClient
from datetime import datetime, timedelta
import random
import sys

def ingest_to_elasticsearch():
    client = None
    try:
        es = Elasticsearch(['http://localhost:9201'])
        if not es.ping():
            raise Exception("Elasticsearch not reachable")
        
        client = MongoClient('mongodb://localhost:27017/')
        db = client['harcelement']
        collection = db['posts']
        
        # Create index with proper mapping for Kibana
        if not es.indices.exists(index='harcelement_posts'):
            mapping = {
                "mappings": {
                    "properties": {
                        "titre": {
                            "type": "text",
                            "fields": {
                                "keyword": {"type": "keyword", "ignore_above": 256}
                            }
                        },
                        "contenu": {
                            "type": "text",
                            "fields": {
                                "keyword": {"type": "keyword", "ignore_above": 256}
                            }
                        },
                        "auteur": {"type": "keyword"},
                        "date": {"type": "date"},
                        "URL": {"type": "keyword"},
                        "langue": {"type": "keyword"},
                        "sentiment": {"type": "keyword"},
                        "score": {"type": "float"},
                        "source": {"type": "keyword"},
                        "Type": {"type": "keyword"},
                        "Label": {"type": "keyword"},
                        "Text": {"type": "text"},
                        "Id_post": {"type": "keyword"}
                    }
                }
            }
            es.indices.create(index='harcelement_posts', body=mapping)
        
        # Simulate sources and dates
        sources = ['twitter', 'facebook', 'instagram', 'reddit', 'youtube']
        base_date = datetime.now() - timedelta(days=30)  # Start 30 days ago
        
        for i, doc in enumerate(collection.find()):
            # Simulate varied dates for temporal analysis
            random_days = random.randint(0, 30)
            random_hours = random.randint(0, 23)
            random_minutes = random.randint(0, 59)
            simulated_date = base_date + timedelta(days=random_days, hours=random_hours, minutes=random_minutes)
            
            # Simulate random source
            simulated_source = random.choice(sources)
            
            es_doc = {
                'titre': doc['Text'][:50] + '...' if len(doc['Text']) > 50 else doc['Text'],
                'contenu': doc['Text'],
                'auteur': 'unknown',
                'date': simulated_date.isoformat(),
                'URL': '',
                'langue': doc.get('language', 'unknown'),
                'sentiment': doc.get('sentiment', 'unknown'),
                'score': doc.get('sentiment_score', 0.0),
                'source': simulated_source,
                'Type': doc['Types'],
                'Label': doc['Label'],
                'Text': doc['Text'],
                'Id_post': str(doc['Id_post'])
            }
            es.index(index='harcelement_posts', body=es_doc)
        
        print("✅ Data indexed in Elasticsearch with simulated dates and sources.")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        if client is not None:
            client.close()

if __name__ == "__main__":
    ingest_to_elasticsearch()