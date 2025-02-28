import requests

url = "http://127.0.0.1:11434/api/generate"
payload = {
    "model": "mistral",
    "prompt": "whats is AI?",
    "stream": False
}

response = requests.post(url, json=payload)

print(response.json()["response"])
