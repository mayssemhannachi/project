# Data Science Technical Test - Mayssem Hannachi
## Overview
This project processes a Kaggle cyberbullying dataset (8,452 rows) through a pipeline involving MongoDB storage, text preprocessing, NLP analysis, Elasticsearch indexing, and Kibana visualization. The dataset is processed in five étapes, with corresponding test units to ensure functionality.
## Project Structure
project/
├── scripts/
│   ├── scraper.py
│   ├── preprocessing.py
│   ├── nlp_pipeline.py
│   ├── es_ingest.py
├── tests/
│   ├── test_scraper.py
│   ├── test_preprocessing.py
│   ├── test_nlp_pipeline.py
├── dataset/
│   └── dataset.csv
├── screenshots/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md

## Prerequisites

Python: 3.9 or later (via Anaconda cyberbullying_env)
MongoDB: Community edition (brew install mongodb-community)
Elasticsearch: 8.8.0 (brew install elastic/tap/elasticsearch-full)
Kibana: 8.8.0 (brew install elastic/tap/kibana-full)
Docker: For containerized execution

## Setup

### Create a new conda environment (Python 3.9+)
conda create -n cyberbullying_env python=3.9 -y

### Activate the environment
conda activate cyberbullying_env

### Install dependencies from requirements.txt
pip install -r requirements.txt

### Download required NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('punkt_tab')"


## Start services:

MongoDB:brew services start mongodb-community
# Or: mongod --dbpath /data/db --port 27017  # Use 27018 if 27017 is in use


Elasticsearch:elasticsearch


Kibana:kibana




Docker (optional):
docker-compose up -d



## Execution
Run each étape sequentially from the project root directory:

### Étape 1: Load CSV to MongoDB:
python scripts/scraper.py --csv "dataset/dataset.csv"


#### Verify:
mongosh --port 27017
use harcelement
db.posts.find().limit(5)


### Étape 2: Text Preprocessing:
python scripts/preprocessing.py

#### Verify:
mongosh --port 27017
use harcelement
db.posts.find({}, {Text: 1, Text_cleaned: 1}).limit(5)


Étape 3: NLP Processing:
python scripts/nlp_pipeline.py

Verify:
mongosh --port 27017
use harcelement
db.posts.find().limit(5)


Étape 4: Elasticsearch Indexing:
python scripts/es_ingest.py

Verify:
curl -X GET "http://localhost:9200/harcelement_posts/_search?pretty"


Étape 5: Kibana Visualization:

Access: http://localhost:5601
Create index pattern: Stack Management > Index Patterns > Create for harcelement_posts
Create visualizations:
Pie Chart: language
Pie Chart: sentiment
Histogram: sentiment_score
Data Table: Sort by sentiment_score (ascending)


Create dashboard: Add visualizations, include filters for language, sentiment_score, Type
Save screenshots to screenshots/



## Running Test Units
Test units validate the functionality of each script. Ensure MongoDB is running (brew services start mongodb-community) before testing.

### Install pytest:
pip install pytest


### Run all tests:
pytest tests/ -v


### Individual test units:

#### Étape 1: Test scraper.py:
PYTHONPATH=. pytest tests/test_scraper.py -v

######Tests:
test_load_and_store_data_tmp: Verifies loading a temporary CSV (2 rows) into MongoDB.
test_load_and_store_data_real: Verifies loading the full dataset (8,452 rows) into MongoDB.Requirements: dataset/dataset.csv must exist.


#### Étape 2: Test preprocessing.py:
PYTHONPATH=. pytest tests/test_preprocessing.py -v


##### Tests:
test_preprocess_text: Verifies text cleaning (e.g., removing HTML, URLs, special characters).


#### Étape 3: Test nlp_pipeline.py:
PYTHONPATH=. pytest tests/test_nlp_pipeline.py -v

##### Tests:
test_nlp_process: Verifies language detection and sentiment analysis.




## Troubleshooting:

File Not Found: Ensure the CSV is at dataset/Approach to Social Media Cyberbullying and Harassment Detection Using Advanced Machine Learning.csv.
MongoDB Errors: Verify MongoDB is running on port 27017 (or 27018 if configured). Update MongoClient port in scripts if needed.
Column Mismatch: Ensure scraper.py maps CSV columns (Text, Types, Label) correctly.



Exports
Export data for submission:
mongoexport --db harcelement --collection posts --out posts.json
curl -X GET "http://localhost:9200/harcelement_posts/_search?pretty" > es_export.json

Notes

Dataset: Contains 8,452 rows with columns Text, Types, Label.
MongoDB Port: Default is 27017; use 27018 if 27017 is in use.
Screenshots: Stored in screenshots/ for Kibana visualizations.
Docker: Use docker-compose.yml for containerized execution.
