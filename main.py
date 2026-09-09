from pathlib import Path

from app.ai_parser import AIParser
from app.chunker import split_text
from app.extractor import extract_page
from app.parser import print_document, save_json
from app.rag import RAG
from app.vectorstore import VectorStore


def add_url(vectorstore: VectorStore) -> None:
    url = input("\nURL a ajouter : ").strip()
    if not url:
        print("URL vide.")
        return
    try:
        text = extract_page(url)
        Path("extraction.txt").write_text(text, encoding="utf-8")
        document = AIParser().parse(text, url)
        print_document(document)
        save_json(document)
        chunks = split_text(text)
        vectorstore.add_chunks(chunks, url)
        print(f"Document ajoute : {len(chunks)} chunks.")
    except Exception as error:
        print(f"Erreur : {error}")


def main() -> None:
    try:
        vectorstore = VectorStore()
        rag = RAG(vectorstore)
    except ValueError as error:
        print(f"Configuration incomplete : {error}")
        print("Copiez .env.example vers .env et renseignez OPENAI_API_KEY.")
        return

    while True:
        print("\n" + "=" * 60)
        print("MON MINI NOTEBOOKLM")
        print("=" * 60)
        print("1. Ajouter une URL")
        print("2. Poser une question")
        print("3. Voir les statistiques")
        print("4. Quitter")
        choice = input("\nVotre choix : ").strip()
        if choice == "1":
            add_url(vectorstore)
        elif choice == "2":
            question = input("\nVotre question : ").strip()
            if question:
                try:
                    result = rag.ask(question)
                    print("\n" + result["answer"])
                    print("\nSources:")
                    print("\n".join(f"- {source}" for source in result["sources"]))
                except Exception as error:
                    print(f"Erreur RAG : {error}")
        elif choice == "3":
            print(f"Chunks dans la base : {vectorstore.count()}")
        elif choice == "4":
            print("Au revoir !")
            break
        else:
            print("Choix incorrect.")


if __name__ == "__main__":
    main()
