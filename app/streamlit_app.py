import streamlit as st

from app.ai_parser import AIParser
from app.chunker import split_text
from app.extractor import extract_page
from app.parser import save_json
from app.rag import RAG
from app.vectorstore import VectorStore

st.set_page_config(page_title="Gutenberg IA", page_icon="📚", layout="wide")


@st.cache_resource
def get_vectorstore():
    return VectorStore()


@st.cache_resource
def get_rag(_vectorstore):
    return RAG(_vectorstore)


st.title("📚 L'IA DE YOUSRA")
st.caption("Extraction, analyse, recherche sémantique et réponses sourcées")

try:
    vectorstore = get_vectorstore()
    rag = get_rag(vectorstore)
except ValueError as error:
    st.error(str(error))
    st.info("Copiez .env.example vers .env, puis renseignez OPENAI_API_KEY.")
    st.stop()

with st.sidebar:
    st.header("Configuration")
    st.success("Application locale")
    st.metric("Chunks dans la base", vectorstore.count())

url = st.text_input("URL du document", "https://www.gutenberg.org/ebooks/1342")
if st.button("Ajouter le document", type="primary"):
    if not url.strip():
        st.warning("Veuillez entrer une URL.")
    else:
        with st.status("Traitement du document...", expanded=True) as status:
            try:
                text = extract_page(url)
                st.write(f"{len(text):,} caractères extraits")
                with open("extraction.txt", "w", encoding="utf-8") as file:
                    file.write(text)
                document = AIParser().parse(text, url)
                save_json(document)
                chunks = split_text(text)
                st.write(f"{len(chunks)} chunks créés")
                vectorstore.add_chunks(chunks, url)
                st.session_state["last_document"] = document
                status.update(label="Document ajouté avec succès", state="complete")
            except Exception as error:
                status.update(label="Erreur", state="error")
                st.error(str(error))

if "last_document" in st.session_state:
    st.subheader("Dernier document")
    st.json(st.session_state["last_document"])

st.divider()
st.subheader("Poser une question")
question = st.text_area("Votre question", placeholder="Qui est Elizabeth Bennet ?")
if st.button("Rechercher"):
    if not question.strip():
        st.warning("Veuillez écrire une question.")
    elif vectorstore.count() == 0:
        st.warning("Ajoutez d'abord un document.")
    else:
        with st.spinner("Recherche et génération de la réponse..."):
            try:
                result = rag.ask(question)
                st.markdown("### Réponse")
                st.write(result["answer"])
                st.markdown("### Sources")
                for source in result["sources"]:
                    st.markdown(f"- {source}")
            except Exception as error:
                st.error(str(error))
