
import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError

load_dotenv()
# SDK apne aap GEMINI_API_KEY (ya GOOGLE_API_KEY) .env se utha leta hai
# Client initialization
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    client = None

def generate_meeting_minutes(transcript: str) -> dict:
    """
    Call Gemini API for abstractive meeting summary using the google-genai SDK.
    """
    if not client:
        return {"title": "Error", "summary": "Gemini Client not initialized.", "decisions": [], "action_items": [], "attendees": []}

    if not transcript.strip():
        return {"title": "Error", "summary": "No transcript available.", "decisions": [], "action_items": [], "attendees": []}

    # Prompt structure
    system_instruction = (
        "You are a professional meeting summarization assistant. "
        "Analyze the following transcript and return the results as a single, "
        "well-formed JSON object. The keys must be 'title', 'summary', 'attendees' (array of strings), "
        "'decisions' (array of strings), and 'action_items' (array of objects with 'task', 'owner', and 'due' keys)."
    )
    
    config = types.GenerateContentConfig(
        temperature=0.1,
        system_instruction=system_instruction,
        response_mime_type="application/json"
    )

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Meeting Transcript to Summarize:\n\n{transcript}",
            config=config,
        )
        
        # Parse the JSON string from the response
        try:
            minutes_dict = json.loads(response.text)
            minutes_dict["_transcript"] = transcript 
            return minutes_dict
        except json.JSONDecodeError:
            return {"title": "Error", "summary": f"Gemini API returned unparsable JSON: {response.text}", "decisions": [], "action_items": [], "attendees": [], "_transcript": transcript}
            
    except APIError as e:
        return {"title": "Error", "summary": f"Gemini API Error: {str(e)}", "decisions": [], "action_items": [], "attendees": [], "_transcript": transcript}
    except Exception as e:
        return {"title": "Error", "summary": f"An unexpected error occurred: {str(e)}", "decisions": [], "action_items": [], "attendees": [], "_transcript": transcript}