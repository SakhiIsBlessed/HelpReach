import requests
import json

# Test if photos are in donations
response = requests.get('http://127.0.0.1:5000/api/donations')
donations = response.json()

print(f"Total donations: {len(donations)}")
print("\nRecent 3 donations:")
for d in donations[:3]:
    print(f"  ID: {d.get('id')}")
    print(f"  Title: {d.get('title')}")
    print(f"  Photo: {d.get('photo_filename')}")
    print()
