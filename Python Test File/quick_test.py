import requests

print("Testing donation endpoint...")
url = "http://localhost:5000/api/donations"
data = {
    "title": "Test Donation",
    "description": "Testing email",
    "quantity": "10",
    "pickup_info": "Test location",
    "donor_id": 1,
    "donor_email": "test@example.com"
}

try:
    r = requests.post(url, json=data)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.json()}")
except Exception as e:
    print(f"Error: {e}")
