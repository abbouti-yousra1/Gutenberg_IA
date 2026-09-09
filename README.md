# Gutenberg IA

Pipeline local : URL Gutenberg -> extraction -> analyse OpenAI -> chunks -> embeddings -> ChromaDB -> recherche RAG.

## Installation Windows

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Renseignez `OPENAI_API_KEY` dans `.env`.

## Interface web

```powershell
python -m streamlit run app\streamlit_app.py
```

## Interface terminal

```powershell
python main.py
```

L'URL Gutenberg `https://www.gutenberg.org/ebooks/1342` est préremplie. L'extracteur suit le lien `Plain Text` quand il est disponible, afin de permettre des questions sur le contenu complet du livre.

Les fichiers générés (`extraction.txt`, `document.json`) et la base locale ChromaDB sont ignorés par Git. Ne partagez jamais `.env`.
