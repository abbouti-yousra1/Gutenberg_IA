import json
from pathlib import Path
from typing import Any


def save_json(data: dict[str, Any], filename: str = "document.json") -> None:
    Path(filename).write_text(
        json.dumps(data, ensure_ascii=False, indent=4),
        encoding="utf-8",
    )


def print_document(data: dict[str, Any]) -> None:
    print("\n" + "=" * 70)
    print("DOCUMENT STRUCTURE")
    print("=" * 70)
    print(json.dumps(data, ensure_ascii=False, indent=4))
    print("=" * 70)
