# Data Science Technical Test - Mayssem Hannachi

## Overview
This project processes a Kaggle cyberbullying dataset (8,452 rows) through a pipeline involving MongoDB storage, text preprocessing, NLP analysis, Elasticsearch indexing, and Kibana visualization. The dataset is processed in five stages, with corresponding test units to ensure functionality.

## Project Structure
```
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
```

## Prerequisites
- Python 3.9 or later (via Anaconda `cyberbullying_env`)
- MongoDB Community Edition (`brew install mongodb-community`)
- Elasticsearch 8.8.0 (`brew install elastic/tap/elasticsearch-full`)
- Kibana 8.8.0 (`brew install elastic/tap/kibana-full`)
- Docker (for containerized execution)

## Setup

### 1. Create a Conda Environment
```bash
conda create -n cyberbullying_env python=3.9 -y
```

### 2. Activate the Environment
```bash
conda activate cyberbullying_env
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Download Required NLTK Data
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

### 5. Start Services
- **MongoDB:**
  ```bash
  brew services start mongodb-community
  ```
  Or, if port 27017 is in use:
  ```bash
  mongod --dbpath /data/db --port 27017  # Use 27018 if 27017 is occupied
  ```
- **Elasticsearch:**
  ```bash
  elasticsearch
  ```
- **Kibana:**
  ```bash
  kibana
  ```

---

## Execution
Run each stage sequentially from the project root directory.

### Stage 1: Load CSV to MongoDB
```bash
python scripts/scraper.py --csv dataset/dataset.csv
```
**Verify:**
```bash
mongosh --port 27017
use harcelement
db.posts.find().limit(5)
```

### Stage 2: Text Preprocessing
```bash
python scripts/preprocessing.py
```
**Verify:**
```bash
mongosh --port 27017
use harcelement
db.posts.find({}, {Text: 1, Text_cleaned: 1}).limit(5)
```

### Stage 3: NLP Processing
```bash
python scripts/nlp_pipeline.py
```
**Verify:**
```bash
mongosh --port 27017
use harcelement
db.posts.find().limit(5)
```

### Stage 4: Elasticsearch Indexing
```bash
python scripts/es_ingest.py
```
**Verify:**
```bash
curl -X GET "http://localhost:9200/harcelement_posts/_search?pretty"
```

### Stage 5: Kibana Visualization
- View screenshots and video demo in the `screenshots/` folder.
- Access Kibana at [http://localhost:5601](http://localhost:5601)
- Create an index pattern for `harcelement_posts*` and build your visualizations and dashboards.

---

## Running Test Units
Test units validate the functionality of each script. Ensure MongoDB is running before testing:
```bash
brew services start mongodb-community
```

### Install pytest
```bash
pip install pytest
```

### Run All Tests
```bash
PYTHONPATH=. pytest tests/ -v
```

### Individual Test Units

#### Stage 1: Test scraper.py
```bash
PYTHONPATH=. pytest tests/test_scraper.py -v
```
- **test_load_and_store_data_tmp:** Verifies loading a temporary CSV (2 rows) into MongoDB.
- **test_load_and_store_data_real:** Verifies loading the full dataset (8,452 rows) into MongoDB. (Requirement: `dataset/dataset.csv` must exist)

#### Stage 2: Test preprocessing.py
```bash
PYTHONPATH=. pytest tests/test_preprocessing.py -v
```
- **test_preprocess_text:** Verifies text cleaning (e.g., removing HTML, URLs, special characters).

#### Stage 3: Test nlp_pipeline.py
```bash
PYTHONPATH=. pytest tests/test_nlp_pipeline.py -v
```
- **test_nlp_process:** Verifies language detection and sentiment analysis.

---

## Running the Project with Docker

### Build and Start All Services
```bash
docker-compose up --build
```

### Run Each Pipeline Step
```bash
docker-compose run app python scripts/scraper.py --csv dataset/dataset.csv
docker-compose run app python scripts/preprocessing.py
docker-compose run app python scripts/nlp_pipeline.py
docker-compose run app python scripts/es_ingest.py
```

### Access Kibana
- Open [http://localhost:5601](http://localhost:5601) in your browser.
- Create an index pattern for `harcelement_posts*`.
- Build visualizations and dashboards.

### Stop All Services
Press `Ctrl+C` in the terminal running `docker-compose up`, then:
```bash
docker-compose down
```

---

## Troubleshooting
- **File Not Found:** Ensure the CSV is located at `dataset/dataset.csv`.
- **MongoDB Errors:** Verify MongoDB is running on port 27017 (or 27018 if configured). Update the MongoClient port in scripts if needed.
- **Column Mismatch:** Ensure `scraper.py` maps CSV columns (`Text`, `Types`, `Label`) correctly.

---

## Notes
- **Dataset:** Contains 8,452 rows with columns `Text`, `Types`, `Label`.
- **MongoDB Port:** Default is 27017; use 27018 if 27017 is in use.
- **Screenshots:** Stored in `screenshots/` for Kibana visualizations.
- **Docker:** Use `docker-compose.yml` for containerized execution.
- **Docker Compose Networking:** When running in Docker Compose, the app connects to MongoDB and Elasticsearch using service names (`mongodb`, `elasticsearch`) as hostnames, not `localhost`.
