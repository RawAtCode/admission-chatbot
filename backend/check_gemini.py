
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

models = [
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
]

for model_name in models:
    print(f"\nTesting: {model_name}")

    try:
        response = client.models.generate_content(
            model=model_name,
            contents="Reply with exactly: API test successful."
        )

        print("SUCCESS:", response.text)

    except Exception as error:
        print("FAILED:", str(error))
