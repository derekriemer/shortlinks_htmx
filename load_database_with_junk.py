import requests

API_URL = "http://localhost:8000/api/add"

for link_number in range(30, 50):
    params = {
        "name": f"link_{link_number}",
        "url": f"https://example.com/link_{link_number}"
    }
    response = requests.post(API_URL, params=params)
    print(f"Added link_{link_number}: {response.status_code}")
    print(response.json())
