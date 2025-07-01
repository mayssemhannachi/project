FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install pandas
RUN pip install nltk 
RUN pip install pymongo
RUN pip install beautifulsoup4
RUN pip install langdetect
RUN pip install vaderSentiment
RUN pip install elasticsearch
RUN pip install pytest

# List all installed packages for debugging
RUN pip list

# Download NLTK data
RUN pip show nltk
RUN python -m nltk.downloader punkt stopwords wordnet

COPY . .

# Default command (can be overridden)
ENTRYPOINT ["python"]
CMD ["scripts/scraper.py", "--csv", "dataset/dataset.csv"]