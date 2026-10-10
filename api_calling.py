import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
import io
from gtts import gTTS

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=api_key)

def note_generator(images, language, option):
    prompt = f"""You are an expert AI Code Debugger. Analyze the provided code image carefully. 
    Programming Language: {language}
    Selected Option/Focus: {option}
    
    1. Identify all syntax, logic, or runtime errors visible in the code.
    2. Provide a clear, structured bug report explaining what went wrong and why.
    3. Output the fully corrected, clean code in proper Markdown code blocks with appropriate syntax highlighting.
    Keep the explanation concise and developer-friendly."""
    
    response = client.models.generate_content(
        model="gemini-3-flash-preview", 
        contents=[images, prompt]
    )
    return response.text

def audio_generator(text):
    speech = gTTS(text, lang="en", slow=False)
    audio_buffer = io.BytesIO()
    speech.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer