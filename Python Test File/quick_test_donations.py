import urllib.request
import json

print("Testing Donations Feed...")
resp = urllib.request.urlopen('http://127.0.0.1:5000/api/donations')
data = json.loads(resp.read())
print(f'✅ API returned {len(data)} donations')
if data:
    d = data[0]
    print(f'First donation: {d.get("title")} (Status: {d.get("status")})')
    print(f'Location: {d.get("pickup_location")}, Photo: {d.get("photo_filename") is not None}')
