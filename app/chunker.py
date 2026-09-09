def split_text(text: str, chunk_size: int = 1200, overlap: int = 200) -> list[str]:
    """Split text into overlapping character-based chunks."""
    if not text:
        return []
    if chunk_size <= 0:
        raise ValueError("chunk_size doit etre positif")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap doit etre compris entre 0 et chunk_size - 1")

    chunks = []
    step = chunk_size - overlap
    for start in range(0, len(text), step):
        chunk = text[start:start + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
        if start + chunk_size >= len(text):
            break
    return chunks
