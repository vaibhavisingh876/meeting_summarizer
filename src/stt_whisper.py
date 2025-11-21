import whisper

# Load model once
model = whisper.load_model("small")  # change to "base"/"medium" if needed

def transcribe_audio(audio_path: str) -> str:
    """
    Offline Whisper transcription for meeting audio.
    Returns transcript as string.
    """
    print("[INFO] Converting speech to text...")
    result = model.transcribe(audio_path)
    text = result.get("text", "")
    if not text.strip():
        return "No speech detected."
    return text
