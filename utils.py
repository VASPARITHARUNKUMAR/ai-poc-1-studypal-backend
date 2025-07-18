import hashlib
from nltk.tokenize import sent_tokenize
from datetime import datetime

def file_hash(file_bytes):
    return hashlib.md5(file_bytes).hexdigest()

def chunk_text_semantic(text, max_length=500):
    sentences = sent_tokenize(text)
    chunks, chunk = [], ""
    for sentence in sentences:
        if len(chunk) + len(sentence) < max_length:
            chunk += " " + sentence
        else:
            chunks.append(chunk.strip())
            chunk = sentence
    if chunk:
        chunks.append(chunk.strip())
    return chunks

def log_event(event: str):
    with open("usage.log", "a") as log:
        log.write(f"{datetime.now()} - {event}\n")
