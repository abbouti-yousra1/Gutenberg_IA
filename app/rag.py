import os

from dotenv import load_dotenv
from openai import OpenAI

from app.vectorstore import VectorStore

load_dotenv()


class RAG:
    def __init__(self, vectorstore: VectorStore | None = None) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "TA_VRAIE_CLE_OPENAI":
            raise ValueError("OPENAI_API_KEY est absente du fichier .env")
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_CHAT_MODEL", "gpt-5")
        self.vectorstore = vectorstore or VectorStore()

    def ask(self, question: str, n_results: int = 5) -> dict:
        results = self.vectorstore.search(question, n_results)
        documents = (results.get("documents") or [[]])[0]
        metadatas = (results.get("metadatas") or [[]])[0]
        if not documents:
            return {"answer": "Je ne trouve aucune information dans les sources.", "sources": []}

        context = "\n\n".join(
            f"SOURCE {index + 1}\nURL: {metadata.get('source', 'inconnue')}\nCONTENU:\n{document}"
            for index, (document, metadata) in enumerate(zip(documents, metadatas))
        )
        prompt = f"""Reponds en francais uniquement a partir du CONTEXTE.
N'invente rien. Si la reponse n'est pas presente, dis-le clairement.
Cite les URL utilisees a la fin.

CONTEXTE:
{context}

QUESTION:
{question}
"""
        response = self.client.responses.create(model=self.model, input=prompt)
        sources = list(dict.fromkeys(metadata.get("source") for metadata in metadatas if metadata.get("source")))
        return {"answer": response.output_text.strip(), "sources": sources}
