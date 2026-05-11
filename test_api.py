import requests

# This is your local Django endpoint
url = "http://127.0.0.1:8000/api/chat/"

# Testing the refund query in Lagos flex style
data = {
    "query": "I wan refund but I no get receipt, wetin I go do?"
}

print("--- Sending Query to NovaPay Backend ---")
try:
    response = requests.post(url, json=data, timeout=20)
    print(f"Status Code: {response.status_code}")
    print(f"Nova-Pilot Response: {response.json().get('response')}")
except Exception as e:
    print(f"Wahala: {e}")