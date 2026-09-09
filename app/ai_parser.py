import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

SCHEMA = {
    "titre": None,
    "auteur": None,
    "date_publication_oeuvre": None,
    "date_release_source": None,
    "langue": None,
    "categorie": None,
    "ebook_id": None,
    "prix": None,
    "devise": None,
    "description": None,
    "localisation": None,
    "vendeur": None,
    "caracteristiques": [],
    "source": None,
    "url": None,
}


class AIParser:
    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "TA_VRAIE_CLE_OPENAI":
            raise ValueError("OPENAI_API_KEY est absente du fichier .env")
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_CHAT_MODEL", "gpt-5")

    def parse(self, text: str, url: str | None = None) -> dict[str, Any]:
        prompt = f"""Analyse le texte fourni et retourne uniquement un objet JSON valide.
N'invente aucune information. Utilise null si un champ est absent. Le champ url doit
etre exactement l'URL fournie.

Structure exacte:
{json.dumps(SCHEMA, ensure_ascii=False, indent=2)}

URL: {url}
TEXTE:
{text[:20000]}
"""
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )
        result = response.output_text.strip().removeprefix("```json").removesuffix("```").strip()
        try:
            data = json.loads(result)
        except json.JSONDecodeError as error:
            raise ValueError("L'IA n'a pas retourne un JSON valide.") from error
        data["url"] = url
        return data
