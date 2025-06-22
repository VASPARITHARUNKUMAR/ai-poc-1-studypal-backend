import os
import openai
from dotenv import load_dotenv

load_dotenv()

# Print API key for debugging
print(f"✅ GROQ API Key: {os.getenv('GROQ_API_KEY')}")
openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"

def ask_groq(prompt: str) -> str:
    print(f"⏳ Asking Groq: {prompt}")
    try:
        response = openai.ChatCompletion.create(
            model="llama3-8b-8192",  # fastest Groq model
            messages=[
                {"role": "system", "content": "You are a helpful study assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            timeout=10
        )
        print("✅ Got response from Groq.")
        return response.choices[0].message["content"].strip()
    except Exception as e:
        print(f"❌ Groq API Error: {e}")
        return f"⚠️ Error: {str(e)}"
