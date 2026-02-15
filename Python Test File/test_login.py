import requests
import json

url = "http://127.0.0.1:5000/api/ngo/login"
payload = {
    "email": "test@test.com",
    "password": "testpass123"
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
