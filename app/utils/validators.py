import re
from app.config import get_settings

ALLOWED_LETTER_TYPES = {
    "Rasmiy murojaat", "So‘rov xati", "Iltimos xati", "Javob xati",
    "Hamkorlik taklifi", "Kafolat xati", "Axborot xati", "Bildirishnoma", "Erkin shakl"
}

def clean_text(value: str | None, *, required: bool = True, max_length: int | None = None) -> str | None:
    if value is None:
        if required: raise ValueError("Matn kiritilmadi")
        return None
    value = value.strip()
    if not value or value == "-":
        if required: raise ValueError("Bu maydon majburiy")
        return None
    limit = max_length or get_settings().max_input_length
    if len(value) > limit: raise ValueError(f"Matn {limit} belgidan oshmasligi kerak")
    return value

def safe_filename(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("._")
    return value[:120] or "document"
