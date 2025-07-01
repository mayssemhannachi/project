import pytest
import pandas as pd
from scripts.scraper import load_and_store_data
from pymongo import MongoClient

def test_load_and_store_data_tmp(tmp_path):
    # Test with temporary CSV
    csv_file = tmp_path / "test.csv"
    df = pd.DataFrame({
        'Text': ['Hello world', 'Test message'],
        'Types': ['positive', 'negative'],
        'Label': ['0', '1']
    })
    df.to_csv(csv_file, index=False)
    
    # Run function
    load_and_store_data(str(csv_file))
    
    # Verify in MongoDB
    client = MongoClient('mongodb://localhost:27017/')  
    db = client['harcelement']
    collection = db['posts']
    assert collection.count_documents({}) == 2
    doc = collection.find_one()
    assert all(key in doc for key in ['Text', 'Types', 'Label', 'Id_post'])
    client.close()

def test_load_and_store_data_real():
    # Test with real CSV
    csv_path = 'dataset/dataset.csv' 
    try:
        df = pd.read_csv(csv_path)
        expected_count = len(df)  
        load_and_store_data(csv_path)
        
        # Verify in MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['harcelement']
        collection = db['posts']
        assert collection.count_documents({}) == expected_count
        doc = collection.find_one()
        assert all(key in doc for key in ['Text', 'Types', 'Label', 'Id_post'])
        client.close()
    except FileNotFoundError:
        pytest.skip("Real CSV file not found, skipping test")