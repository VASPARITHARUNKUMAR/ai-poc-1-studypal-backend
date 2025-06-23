import requests

def ask_ollama(query: str, context: str = "") -> str:
    payload = {"model": "deepseek-r1:1.5b", "prompt": context + "\n\n" + query}
    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=20)
        return response.json().get("response", "❌ No response")
    except Exception as e:
        return f"❌ Error from Ollama: {e}"
