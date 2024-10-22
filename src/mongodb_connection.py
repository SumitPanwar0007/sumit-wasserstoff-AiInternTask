# src/mongodb_connection.py

import os
import logging
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection string with credentials
connection_string = os.getenv("MONGO_URL")

# Setting up logging for error tracking
logging.basicConfig(filename='pdf_processing_errors.log', level=logging.INFO)

class MongoDBClient:
    def __init__(self):
        # Connect to the MongoDB client
        self.client = MongoClient(connection_string)
        self.db = self.client["pdf_database"]
        self.collection = self.db["pdf_documents"]

        # Check MongoDB connection
        try:
            self.client.admin.command('ping')
            logging.info("MongoDB connection successful!")
        except Exception as e:
            logging.error(f"Error connecting to MongoDB: {str(e)}")
            exit(1)

    def store_metadata(self, pdf_name, folder_path):
        """Store initial metadata about the PDF file in MongoDB."""
        pdf_path = os.path.join(folder_path, pdf_name)
        try:
            file_stats = os.stat(pdf_path)
            pdf_metadata = {
                "pdf_name": pdf_name,
                "file_size": file_stats.st_size,
                "upload_date": datetime.now(),
                "status": "pending",
                "summary": None,
                "keywords": None
            }
            result = self.collection.insert_one(pdf_metadata)
            logging.info(f"Successfully stored metadata for {pdf_name} in MongoDB with ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            logging.error(f"Error storing metadata for {pdf_name}: {str(e)}")
            return None

    def update_with_summary_and_keywords(self, pdf_id, summary, keywords):
        """Update MongoDB document with the summary and keywords."""
        try:
            self.collection.update_one(
                {"_id": pdf_id},
                {"$set": {
                    "summary": summary,
                    "keywords": keywords,
                    "status": "processed"
                }}
            )
            logging.info(f"Successfully updated MongoDB document with ID: {pdf_id}")
        except Exception as e:
            logging.error(f"Error updating MongoDB for document ID {pdf_id}: {str(e)}")
