import json
import os
import hashlib
import base64
from google import genai
from google.genai.types import Content, Part  # Importing correct types
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import io

# Load environment variables
load_dotenv()

# Define cache directory
CACHE_DIR = "modules/cache"

# Ensure the cache directory exists
os.makedirs(CACHE_DIR, exist_ok=True)

# Initialize the Gemini API client once
GENAI_API_KEY = os.getenv("GEMINI_API_KEY", "")
client = genai.Client(api_key=GENAI_API_KEY)


def get_cache_filename(prompt_text: str, image_data: bytes = None):
    """Generate a unique filename for caching based on prompt and image."""
    hash_input = prompt_text.encode()
    if image_data:
        hash_input += image_data  # Include image bytes in hash if available

    prompt_hash = hashlib.md5(hash_input).hexdigest()
    return os.path.join(CACHE_DIR, f"{prompt_hash}.json")


def load_cache(prompt_text: str, image_data: bytes = None):
    """Load cached response if available."""
    cache_file = get_cache_filename(prompt_text, image_data)
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_cache(prompt_text: str, response_text: str, image_data: bytes = None):
    """Save response in cache."""
    cache_file = get_cache_filename(prompt_text, image_data)
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump({"response": response_text}, f, indent=4, ensure_ascii=False)


def encode_image(image: Image.Image) -> bytes:
    """Convert an image to base64-encoded bytes."""
    with io.BytesIO() as buffer:
        image.save(buffer, format="PNG")
        return buffer.getvalue()


def generate_response(prompt_text: str, image: Image.Image = None):
    """Generate AI response using Gemini with optional image input."""

    # Encode image if available
    image_data = encode_image(image) if image else None

    # Modify prompt if an image is included
    full_prompt = prompt_text
    if image:
        full_prompt += "\n\n(Note: This prompt includes an image for reference.)"

    # Check cache before calling API
    cached_response = load_cache(full_prompt, image_data)
    if cached_response:
        return cached_response["response"]

    try:
        # Prepare input content
        parts = [{"text": prompt_text}]

        # If an image is provided, append it
        if image_data:
            parts.append({
                "inline_data": {
                    "mime_type": "image/png",
                    "data": base64.b64encode(image_data).decode(),
                }
            })

        # Call Gemini API
        response = client.models.generate_content(
                model="gemini-2.0-flash", contents=[{"role": "user", "parts": parts}]
            )

        # Extract response text
        response_text = response.text

        # Cache the response
        save_cache(prompt_text, response_text, image_data)

        return response_text

    except Exception as e:
        return f"Error: {str(e)}"