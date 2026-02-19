from pymongo import MongoClient
import certifi
import json
import os
import streamlit as st
import time

class MongoDBClient:
    def __init__(self, mongo_url, db_name):
        """
        Initialize the MongoDB client.
        
        Parameters:
        - mongo_url (str): MongoDB Atlas connection string
        - db_name (str): Database name
        """
        self.client = MongoClient(mongo_url,tlsCAFile=certifi.where())
        self.db = self.client[db_name]

    def update_collection(self, collection_name, new_data):
        """
        Deletes all existing records and inserts new data into the specified collection.

        Parameters:
        - collection_name (str): Name of the MongoDB collection
        - new_data (list of dicts): Transformed JSON data to insert
        """
        try:
            collection = self.db[collection_name]

            # Delete all existing records
            collection.delete_many({})

            # Insert new data
            if new_data:
                collection.insert_many(new_data)
                print(f"Successfully updated collection: {collection_name}")
                time.sleep(2)
                st.success("Data successfully updated in MongoDB")

        except Exception as e:
            print(f"An error occurred: {e}")


