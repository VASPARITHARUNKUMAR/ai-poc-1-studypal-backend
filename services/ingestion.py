import tempfile
from services.embeddings import generate_embeddings

async def ingest_and_embed(semester, subject, files):
    embeddings_info = []
    for file in files:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(await file.read())
            tmp.flush()
            embs = generate_embeddings(tmp.name)
            embeddings_info.append({"file": file.filename, "embeddings": embs})
    return embeddings_info
