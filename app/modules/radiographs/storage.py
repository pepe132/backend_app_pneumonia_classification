import os
from pathlib import Path
from uuid import uuid4

from app.core.config import RADIOGRAPH_UPLOAD_DIR


EXTENSIONS_BY_CONTENT_TYPE = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
}


def save_radiograph(image_bytes: bytes, content_type: str) -> str:
    extension = EXTENSIONS_BY_CONTENT_TYPE[content_type]
    upload_dir = Path(RADIOGRAPH_UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)

    destination = upload_dir / f"{uuid4()}{extension}"
    temporary = destination.with_suffix(f"{destination.suffix}.tmp")

    temporary.write_bytes(image_bytes)
    os.replace(temporary, destination)
    return str(destination)


def delete_radiograph(file_path: str) -> None:
    try:
        Path(file_path).unlink(missing_ok=True)
    except OSError:
        pass
