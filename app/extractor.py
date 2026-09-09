from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


USER_AGENT = "GutenbergIA/1.0 (+https://www.gutenberg.org/)"


def _download(url: str) -> tuple[str, str]:
    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=30,
    )
    response.raise_for_status()
    return response.text, response.url


def _find_full_text_url(html: str, base_url: str) -> str | None:
    soup = BeautifulSoup(html, "html.parser")
    for link in soup.select("a[href]"):
        label = link.get_text(" ", strip=True).lower()
        href = link.get("href", "")
        if "plain text" in label or "text (utf-8)" in label:
            return urljoin(base_url, href)
    return None


def extract_page(url: str, follow_full_text: bool = True) -> str:
    """Download a Gutenberg page and optionally its linked full-text edition."""
    html, final_url = _download(url)
    text_url = _find_full_text_url(html, final_url) if follow_full_text else None
    if text_url:
        try:
            html, final_url = _download(text_url)
        except requests.RequestException:
            pass

    soup = BeautifulSoup(html, "html.parser")
    for element in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        element.decompose()

    lines = []
    for line in soup.get_text(separator="\n", strip=True).splitlines():
        normalized = " ".join(line.split())
        if normalized:
            lines.append(normalized)
    return "\n".join(lines)
