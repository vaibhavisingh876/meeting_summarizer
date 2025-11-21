# utils.py
import re

def clean_transcript(text: str) -> str:
    """
    Basic cleaning of transcript:
    - Remove filler words
    - Remove repeated/garbled sentences
    """
    filler_words = ["um", "uh", "so carried", "please", "yeah", "I see", "of course", "you know"]
    pattern = r"\b(" + "|".join(map(re.escape, filler_words)) + r")\b"
    cleaned = re.sub(pattern, "", text, flags=re.IGNORECASE)
    # Remove extra spaces & newlines
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()
