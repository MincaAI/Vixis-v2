import requests
import os
import pandas as pd
from io import BytesIO
import json
from dotenv import load_dotenv
from mongodb import MongoDBClient
import streamlit as st

# Load environment variables from .env file
load_dotenv()

def _get_sharepoint_secrets():
    """Secrets from Streamlit Cloud dashboard or .env. Avoids KeyError if [sharepoint] not set."""
    try:
        return dict(st.secrets.get("sharepoint", {}))
    except Exception:
        return {}


class SharePointClient:
    def __init__(self):
        secrets = _get_sharepoint_secrets()
        self.tenant_id = secrets.get("TENANT_ID", os.getenv("TENANT_ID"))
        self.client_id = secrets.get("CLIENT_ID", os.getenv("CLIENT_ID"))
        self.client_secret = secrets.get("CLIENT_SECRET", os.getenv("CLIENT_SECRET"))
        self.resource_url = secrets.get("RESOURCE", os.getenv("RESOURCE"))
        self._secrets = secrets
        if not self.tenant_id or not self.client_id or not self.client_secret:
            raise ValueError(
                "SharePoint/MongoDB non configurés. Sur Streamlit Cloud : réglages → Secrets → ajouter la section [sharepoint] avec TENANT_ID, CLIENT_ID, CLIENT_SECRET, SITE_URL, DRIVE_ID, FOLDER_ID, MONGO_URL, DB_NAME."
            )
        self.base_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.access_token = self.get_access_token()

    def get_access_token(self):
        body = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'https://graph.microsoft.com/.default'
        }
        
        response = requests.post(self.base_url, headers=self.headers, data=body)
        response.raise_for_status()
        return response.json().get('access_token')

    def get_site_id(self, site_url):
        full_url = f'https://graph.microsoft.com/v1.0/sites/{site_url}'
        response = requests.get(full_url, headers={'Authorization': f'Bearer {self.access_token}'})
        response.raise_for_status()
        return response.json().get('id')

    def get_drive_id(self, site_id):
        drives_url = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives'
        response = requests.get(drives_url, headers={'Authorization': f'Bearer {self.access_token}'})
        response.raise_for_status()
        return [(drive['id'], drive['name']) for drive in response.json().get('value', [])]

    def download_file(self, file_url, file_name):
        response = requests.get(file_url, headers={'Authorization': f'Bearer {self.access_token}'})
        response.raise_for_status()
        if file_name.endswith('Screening Valeurs - VIXIS.xlsx'):
            df = pd.read_excel(BytesIO(response.content))
            self.transform(df)

    def download_folder_contents(self, site_id, drive_id, folder_id):
        folder_url = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/items/{folder_id}/children'
        response = requests.get(folder_url, headers={'Authorization': f'Bearer {self.access_token}'})
        response.raise_for_status()
        for item in response.json().get('value', []):
            if 'folder' in item:
                self.download_folder_contents(site_id, drive_id, item['id'])
            elif 'file' in item:
                file_url = item['@microsoft.graph.downloadUrl']
                if item['name'].endswith('Screening Valeurs - VIXIS.xlsx'):
                    self.download_file(file_url, item['name'])

    def round_numeric_values(x):
        numeric_value = pd.to_numeric(x, errors='coerce')  # Convert to number if possible
        if pd.notna(numeric_value):  # Check if it's a valid number
            return round(numeric_value, 2)  # Round if it's a number
        return x 
    
    def transform(self, df):
        df.columns = df.iloc[0]  # Assign first row as column names
        df = df[1:].reset_index(drop=True)  # Remove first row from data
        if df['CUR_MKT_CAP'].isna().all():
            st.error("All values in CUR_MKT_CAP are null. Please check the file.")
            return
        # Find the index of the "SCORING" column
        if "SCORING" in df.columns:
            scoring_index = df.columns.get_loc("SCORING") + 1  # Keep up to "SCORING" (inclusive)
            df = df.iloc[:, :scoring_index]  # Keep only required columns

        # Convert numeric values to float and round them
        df = df.map(lambda x: round(float(x), 2) if str(x).replace('.', '', 1).isdigit() else x)

        df.columns = df.columns.str.strip()
        # Strip and normalize spaces in all string cells
        df = df.map(lambda x: ' '.join(x.split()) if isinstance(x, str) else x)

        json_data = df.to_dict(orient="records")
        json_output = json.dumps(json_data, indent=4)
        mongo_client = MongoDBClient(mongo_url=self._secrets.get('MONGO_URL', os.getenv('MONGO_URL')), db_name=self._secrets.get('DB_NAME', os.getenv('DB_NAME')))
        mongo_client.update_collection('stock', json_data)


    def load_data(self):
        site_url = self._secrets.get("SITE_URL", os.getenv("SITE_URL"))
        site_id = self.get_site_id(site_url)

        drive_id = self._secrets.get("DRIVE_ID", os.getenv("DRIVE_ID"))
        folder_id = self._secrets.get("FOLDER_ID", os.getenv("FOLDER_ID"))
        self.download_folder_contents(site_id, drive_id, folder_id)

