Data Science Technical Test - Mayssem Hannachi
Overview
This project processes a Kaggle cyberbullying dataset (8,452 rows) through a pipeline involving MongoDB storage, text preprocessing, NLP analysis, Elasticsearch indexing, and Kibana visualization. The dataset is processed in five stages, with corresponding test units to ensure functionality.
Project Structure
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

Prerequisites

Python: 3.9 or later (via Anaconda cyberbullying_env)
MongoDB: Community edition (brew install mongodb-community)
Elasticsearch: 8.8.0 (brew install elastic/tap/elasticsearch-full)
Kibana: 8.8.0 (brew install elastic/tap/kibana-full)
Docker: For containerized execution

Setup
1. Create a Conda Environment
conda create -n cyberbullying_env python=3.9 -y

2. Activate the Environment
conda activate cyberbullying_env

3. Install Dependencies
pip install -r requirements.txt

4. Download Required NLTK Data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('punkt_tab')"

5. Start Services

MongoDB:
brew services start mongodb-community

Or, if port 27017 is in use, specify a custom path and port:
mongod --dbpath /data/db --port 27017  # Use 27018 if 27017 is occupied


Elasticsearch:
elasticsearch


Kibana:
kibana



Execution
Run each stage sequentially from the project root directory.
Stage 1: Load CSV to MongoDB
python scripts/scraper.py --csv "dataset/dataset.csv"

Verify:
mongosh --port 27017
use harcelement
db.posts.find().limit(5)

Stage 2: Text Preprocessing
python scripts/preprocessing.py

Verify:
mongosh --port 27017
use harcelement
db.posts.find({}, {Text: 1, Text_cleaned: 1}).limit(5)

Stage 3: NLP Processing
python scripts/nlp_pipeline.py

Verify:
mongosh --port 27017
use harcelement
db.posts.find().limit(5)

Stage 4: Elasticsearch Indexing
python scripts/es_ingest.py

Verify:
curl -X GET "http://localhost:9200/harcelement_posts/_search?pretty"

Stage 5: Kibana Visualization

View screenshots and video demo in the screenshots/ folder.

Running Test Units
Test units validate the functionality of each script. Ensure MongoDB is running before testing:
brew services start mongodb-community

Install pytest
pip install pytest

Run All Tests
PYTHONPATH=. pytest tests/ -v

Individual Test Units
Stage 1: Test scraper.py
PYTHONPATH=. pytest tests/test_scraper.py -v

Tests:

test_load_and_store_data_tmp: Verifies loading a temporary CSV (2 rows) into MongoDB.
test_load_and_store_data_real: Verifies loading the full dataset (8,452 rows) into MongoDB.
Requirement: dataset/dataset.csv must exist.



Stage 2: Test preprocessing.py
PYTHONPATH=. pytest tests/test_preprocessing.py -v

Tests:

test_preprocess_text: Verifies text cleaning (e.g., removing HTML, URLs, special characters).

Stage 3: Test nlp_pipeline.py
PYTHONPATH=. pytest tests/test_nlp_pipeline.py -v

Tests:

test_nlp_process: Verifies language detection and sentiment analysis.

Running the Project with Docker
Build and Start All Services
docker-compose up --build

Run Each Pipeline Step
docker-compose run app python scripts/scraper.py --csv dataset/dataset.csv
docker-compose run app python scripts/preprocessing.py
docker-compose run app python scripts/nlp_pipeline.py
docker-compose run app python scripts/es_ingest.py

Access Kibana

Open http://localhost:5601 in your browser.
Create an index pattern for harcelement_posts*.
Build visualizations and dashboards.

Stop All Services
Press Ctrl+C in the terminal running docker-compose up, then:
docker-compose down

Troubleshooting

File Not Found: Ensure the CSV is located at dataset/dataset.csv.
MongoDB Errors: Verify MongoDB is running on port 27017 (or 27018 if configured). Update the MongoClient port in scripts if needed.
Column Mismatch: Ensure scraper.py maps CSV columns (Text, Types, Label) correctly.

Notes

Dataset: Contains 8,452 rows with columns Text, Types, Label.
MongoDB Port: Default is 27017; use 27018 if 27017 is in use.
Screenshots: Stored in screenshots/ for Kibana visualizations.
Docker: Use docker-compose.yml for containerized execution.
When running in Docker Compose, the app connects to MongoDB and Elasticsearch using service names (mongodb, elasticsearch) as hostnames, not localhost.
