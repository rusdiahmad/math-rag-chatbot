import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from prompts import SYSTEM_PROMPT, QA_PROMPT
from pathlib import Path

load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Set OPENAI_API_KEY in env")
PERSIST_DIR = "chroma_db"

app = FastAPI(title="Math RAG Chatbot - Bangun Datar & Bangun Ruang")

class Query(BaseModel):
    question: str
    top_k: int = 4

@app.on_event("startup")
def startup():
    global vectordb, retriever, qa_chain
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-3-small")
    vectordb = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)
    retriever = vectordb.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.0, model="gpt-4o-mini")
    prompt = PromptTemplate(template=QA_PROMPT, input_variables=["system_prompt","context","question"])
    qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True, chain_type_kwargs={"prompt": prompt})

@app.post("/query")
def query(q: Query):
    res = qa_chain({"query": q.question})
    answer = res.get("result") or res.get("output_text") or str(res)
    sources = [d.metadata for d in res.get("source_documents", [])]
    return {"answer": answer, "sources": sources}

@app.post("/add_doc")
def add_doc(path: str):
    p = Path(path)
    if not p.exists():
        return {"status": "error", "msg": f"{path} not found"}
    text = p.read_text(encoding="utf-8")
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model="text-embedding-3-small")
    vectordb.add_documents([{"page_content": text}], embedding=embeddings, metadatas=[{"source": str(p)}])
    vectordb.persist()
    return {"status": "ok", "msg": f"added {path}"}
