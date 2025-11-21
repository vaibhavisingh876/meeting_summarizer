import os
from dotenv import load_dotenv
from stt_whisper import transcribe_audio
from summarizer_gpt import generate_meeting_minutes
from markdown_exporter import minutes_to_markdown

load_dotenv()  # load .env file for API keys

print("=== Meeting Summarizer ===")
audio_path = input("Enter your audio file path (mp3, wav, m4a, webm, mp4 etc.):\n> ").strip()

print("\n[STEP 1] Transcribing audio... please wait...")
transcript = transcribe_audio(audio_path)

print("\n[STEP 2] Generating meeting minutes via Gemini API...")  # or OpenAI if you change
minutes = generate_meeting_minutes(transcript)

print("\n[STEP 3] Saving meeting minutes as Markdown...")
try:
    md_path = minutes_to_markdown(minutes)
    print(f"\n✅ Meeting minutes saved as Markdown: {md_path}")
except Exception as e:
    print(f"\n❌ Failed to save markdown: {e}")

print("\n===== MEETING MINUTES =====\n")
print(minutes)
