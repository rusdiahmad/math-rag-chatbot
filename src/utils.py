from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_local_files(data_dir="data"):
    data_dir = Path(data_dir)
    docs = []
    for p in sorted(data_dir.glob("*.md")):
        text = p.read_text(encoding="utf-8")
        docs.append({"path": str(p), "content": text})
    return docs

def chunk_documents(docs, chunk_size=800, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunked = []
    for d in docs:
        pieces = splitter.split_text(d["content"])
        for i, p in enumerate(pieces):
            chunked.append({"id": f"{Path(d['path']).stem}_{i}", "text": p, "source": d["path"]})
    return chunked
