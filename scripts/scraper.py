import pandas as pd
from pymongo import MongoClient
from bson.objectid import ObjectId
import argparse
import sys
import os

def load_and_store_data(csv_path):
    client = None
    try:
        # Load CSV
        df = pd.read_csv(csv_path)
        print(f"Loaded {len(df)} rows from {csv_path}")
        
        # Verify required columns 
        expected_columns = ['Text', 'Types', 'Label']
        if not all(col in df.columns for col in expected_columns):
            print(f"Warning: Expected columns {expected_columns}, found {list(df.columns)}")
        
        # Clean data
        df['Types'] = df['Types'].fillna("Unknown").str.strip()
        df['Label'] = df['Label'].astype(str).str.replace(" ", "").str.strip()
        df['Text'] = df['Text'].astype(str).str.strip()
        
        # Create Id_post
        df['Id_post'] = [str(ObjectId()) for _ in range(len(df))]
        
        # Select required columns
        columns_to_keep = ['Text', 'Types', 'Label', 'Id_post']
        df = df[columns_to_keep]
        
        # Connect to MongoDB
        mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
        client = MongoClient(mongo_uri) 
        db = client['harcelement']
        collection = db['posts']
        
        # Clear existing collection 
        collection.drop()
        
        # Insert data
        documents = df.to_dict(orient='records')
        result = collection.insert_many(documents)
        print(f"✅ Inserted {len(result.inserted_ids)} documents into MongoDB.")
        
    except FileNotFoundError:
        print(f"Error: File {csv_path} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        if client is not None:
            client.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load and store CSV data in MongoDB")
    parser.add_argument('--csv', type=str, required=True, help='Path to CSV file')
    args = parser.parse_args()
    
    load_and_store_data(args.csv)