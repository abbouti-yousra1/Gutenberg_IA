import hashlib
import os
from pathlib import Path

import chromadb
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class VectorStore:
    def __init__(self, path: str = "database/chroma") -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "TA_VRAIE_CLE_OPENAI":
            raise ValueError("OPENAI_API_KEY est absente du fichier .env")
        self.openai = OpenAI(api_key=api_key)
        self.embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
        Path(path).mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(name="documents")

    def create_embeddings(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        response = self.openai.embeddings.create(model=self.embedding_model, input=texts)
        return [item.embedding for item in response.data]

    def add_chunks(self, chunks: list[str], source: str, source_type: str = "web") -> None:
        if not chunks:
            return
        embeddings = self.create_embeddings(chunks)
        source_hash = hashlib.sha256(source.encode("utf-8")).hexdigest()[:16]
        ids = [f"{source_type}_{source_hash}_{index}" for index in range(len(chunks))]
        metadatas = [{"source": source, "source_type": source_type, "chunk": index} for index in range(len(chunks))]
        self.collection.upsert(ids=ids, documents=chunks, embeddings=embeddings, metadatas=metadatas)

    def search(self, question: str, n_results: int = 5) -> dict:
        embedding = self.create_embeddings([question])[0]
        return self.collection.query(query_embeddings=[embedding], n_results=n_results)

    def count(self) -> int:
        return self.collection.count()
