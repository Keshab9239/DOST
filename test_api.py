import os
import json
import urllib.request
import urllib.error

key = os.getenv("GEMINI_API_KEY")

if not key:
    print("API KEY MISSING")
    raise SystemExit

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent"

data = {
    "contents": [{
        "parts": [{
            "text": "Namaste DOST! Hindi mein apna introduction do."
        }]
    }]
}

req = urllib.request.Request(
    url,
    data=json.dumps(data).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "x-goog-api-key": key
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req, timeout=120) as response:
        result = json.loads(response.read())
        print("\nDOST:", result["candidates"][0]["content"]["parts"][0]["text"])

except urllib.error.HTTPError as e:
    print("HTTP ERROR:", e.code)
    print(e.read().decode())

except Exception as e:
    print("ERROR:", str(e))
