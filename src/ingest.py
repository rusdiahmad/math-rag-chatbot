import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from dotenv import load_dotenv
from utils import load_local_files, chunk_documents
from pathlib import Path

load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Set OPENAI_API_KEY in env")

PERSIST_DIR = "chroma_db"

def ingest(data_dir="data", persist_dir=PERSIST_DIR):
    docs = load_local_files(data_dir)
    chunked = chunk_documents(docs)
    texts = [c["text"] for c in chunked]
    metadatas = [{"source": c["source"], "chunk_id": c["id"]} for c in chunked]

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-3-small")
    vectordb = Chroma.from_texts(texts, embeddings, metadatas=metadatas, persist_directory=persist_dir)
    vectordb.persist()
    print(f"Ingested {len(texts)} chunks to Chroma at {persist_dir}")

if __name__ == "__main__":
    ingest()
