import os
import json
import urllib.request
import urllib.error

API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = "gemini-3.8-flash"

if not API_KEY:
    print("API KEY MISSING!")
    exit()

url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

data = {
    "contents": [{
        "parts": [{
            "text": "Tum DOST ho, ek friendly personal AI assistant. Hindi mein jawab do. Apna introduction do."
        }]
    }]
}

req = urllib.request.Request(
    url,
    data=json.dumps(data).encode(),
    headers={"Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req, timeout=60) as response:
        result = json.loads(response.read())
        answer = result["candidates"][0]["content"]["parts"][0]["text"]
        print("\nDOST:", answer)

except Exception as e:
    print("Connection error:", e)
