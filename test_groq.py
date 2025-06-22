import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"

def test_groq():
    try:
        print("⏳ Sending request to Groq...")
        response = openai.ChatCompletion.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is Artificial Intelligence?"}
            ],
            temperature=0.5,
            timeout=10  # seconds
        )
        print("✅ Response from Groq:")
        print(response.choices[0].message["content"].strip())
    except Exception as e:
        print(f"❌ Error calling Groq: {e}")

if __name__ == "__main__":
    test_groq()
