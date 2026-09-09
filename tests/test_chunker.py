from app.chunker import split_text


def test_split_text_returns_overlapping_chunks():
    chunks = split_text("a" * 2500, chunk_size=1200, overlap=200)
    assert len(chunks) == 3
    assert chunks[0][-200:] == chunks[1][:200]


def test_split_text_empty_input():
    assert split_text("") == []
