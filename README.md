# Math RAG Chatbot - Bangun Datar & Bangun Ruang

**Isi proyek ini**:
- data/: konten materi matematika dasar (bangun datar & bangun ruang) dalam file .md
- src/: kode ingestion, API, util
- tests/: script sederhana

**Cara pakai**:
1. Copy .env.example -> .env, isi OPENAI_API_KEY
2. buat virtualenv, aktifkan, lalu:
   pip install -r requirements.txt
3. Ingest data:
   cd math-rag-chatbot
   python src/ingest.py
4. Jalankan API:
   uvicorn src.app:app --reload --port 8000
5. Tes query:
   curl -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d '{"question":"Hitung luas persegi dengan sisi 5"}'

**Catatan**:
- Pastikan OPENAI_API_KEY punya akses model yang ditentukan (ganti model jika perlu).
- Untuk menambah dokumen, gunakan endpoint /add_doc atau tambahkan file di data/ dan re-ingest.
