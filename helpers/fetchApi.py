# Function to fetch data from API
import requests

def fetch_attachment_data(api_url, files):
    try:
        response = requests.post(api_url, files=files)
        response.raise_for_status()  # Ensure response is valid (200 OK)
        original_data = response.json()

        transformed_data = [
            {
                "name": item["name"],
                "mime": item["mimeType"],
                "data": item["content"],
                "type": "file:full"
            }
            for item in original_data
        ]

        return transformed_data
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def fetch_data(api_url, payload):
    try:
        response = requests.post(api_url, json=payload)
        data = response.json().get('text', "No response received.")
        return data
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"