# 📊 Data Science Technical Test – Mayssem Hannachi

## 🗂 Overview

This project processes a Kaggle **cyberbullying dataset (8,452 rows)** through a pipeline involving:

- **MongoDB** for storage  
- **Text preprocessing**  
- **NLP analysis**  
- **Elasticsearch** for indexing  
- **Kibana** for visualization

Each processing stage includes corresponding unit tests to ensure reliability and modularity.

---

## 📁 Project Structure

project/
├── scripts/
│   ├── scraper.py              # Load data to MongoDB
│   ├── preprocessing.py        # Clean and normalize text
│   ├── nlp_pipeline.py         # Sentiment analysis & language detection
│   ├── es_ingest.py            # Elasticsearch ingestion
├── tests/
│   ├── test_scraper.py
│   ├── test_preprocessing.py
│   ├── test_nlp_pipeline.py
├── dataset/
│   └── dataset.csv             # Original dataset
├── screenshots/                # Kibana visualization screenshots
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md

---

## ⚙️ Prerequisites

- Python 3.9+ (recommended: via Conda)
- MongoDB (e.g., `brew install mongodb-community`)
- Elasticsearch 8.8.0 (`brew install elastic/tap/elasticsearch-full`)
- Kibana 8.8.0 (`brew install elastic/tap/kibana-full`)
- Docker & Docker Compose

---

## 🧪 Setup

### 1. Create & Activate Conda Environment
```bash
conda create -n cyberbullying_env python=3.9 -y
conda activate cyberbullying_env

2. Install Python Dependencies

pip install -r requirements.txt

3. Download NLTK Data

python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('punkt_tab')"


⸻

▶️ Execution (Manual Mode)

Run from project root:

🔹 Stage 1: Load CSV to MongoDB

python scripts/scraper.py --csv "dataset/dataset.csv"

Verify in MongoDB:

mongosh --port 27017
use harcelement
db.posts.find().limit(5)


⸻

🔹 Stage 2: Text Preprocessing

python scripts/preprocessing.py

Verify:

db.posts.find({}, {Text: 1, Text_cleaned: 1}).limit(5)


⸻

🔹 Stage 3: NLP Pipeline

python scripts/nlp_pipeline.py


⸻

🔹 Stage 4: Elasticsearch Indexing

python scripts/es_ingest.py

Verify:

curl -X GET "http://localhost:9200/harcelement_posts/_search?pretty"


⸻

🔹 Stage 5: Kibana Visualization
	•	Access Kibana: http://localhost:5601
	•	Create index pattern: harcelement_posts*
	•	View sample dashboards in screenshots/

⸻

🧪 Run Unit Tests

Setup

pip install pytest

Run All Tests

PYTHONPATH=. pytest tests/ -v


⸻

Individual Test Scripts

✅ Test scraper.py

PYTHONPATH=. pytest tests/test_scraper.py -v

	•	test_load_and_store_data_tmp: Test with 2-row temp file
	•	test_load_and_store_data_real: Test with full dataset (8,452 rows)

Ensure dataset/dataset.csv exists

⸻

✅ Test preprocessing.py

PYTHONPATH=. pytest tests/test_preprocessing.py -v

	•	test_preprocess_text: Verifies HTML, URL, and special char removal

⸻

✅ Test nlp_pipeline.py

PYTHONPATH=. pytest tests/test_nlp_pipeline.py -v

	•	test_nlp_process: Language detection + Sentiment analysis

⸻

🐳 Docker-Based Execution

Build and Start All Services

docker-compose up --build

Run Pipeline Steps

docker-compose run app python scripts/scraper.py --csv dataset/dataset.csv
docker-compose run app python scripts/preprocessing.py
docker-compose run app python scripts/nlp_pipeline.py
docker-compose run app python scripts/es_ingest.py

Access Kibana Dashboard
	•	http://localhost:5601
	•	Create index: harcelement_posts*

Stop All Services

docker-compose down


⸻

🛠 Troubleshooting

Issue	Solution
File Not Found	Ensure CSV is at dataset/dataset.csv
MongoDB connection issues	Check Mongo is running on 27017 (or change script to 27018)
Column mismatch in CSV	Verify columns: Text, Types, Label
Docker Mongo/ES access	Use container service names mongodb, elasticsearch instead of localhost


⸻

📌 Notes
	•	Dataset: 8,452 rows, columns: Text, Types, Label
	•	MongoDB default port: 27017 (use 27018 if needed)
	•	Screenshots: See screenshots/ folder
	•	Docker-friendly: All services defined in docker-compose.yml
