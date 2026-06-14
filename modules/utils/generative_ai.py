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

DEFAULT_MODEL = "gemini-3.5-flash"

# Model Quotas (Free Tier Defaults)
MODEL_QUOTAS = {
    "gemini-3.5-flash": {"RPM": 10, "RPD": 1500},
    "gemini-2.0-flash": {"RPM": 15, "RPD": 1500},
    "gemini-1.5-flash": {"RPM": 15, "RPD": 1500},
}


def initialise_quotas():
    """Initialize quota tracking in session state if not present."""
    if 'quota_usage' not in st.session_state:
        st.session_state.quota_usage = {
            model: {"RPM_left": info["RPM"], "RPD_left": info["RPD"], "last_reset": st.session_state.get('start_time', 0)}
            for model, info in MODEL_QUOTAS.items()
        }


def update_quota(model_name: str):
    """Decrement quota for the selected model."""
    initialise_quotas()
    if model_name in st.session_state.quota_usage:
        # We can't easily track RPM perfectly without background threads, 
        # but we can decrement RPD and provide a warning.
        st.session_state.quota_usage[model_name]["RPD_left"] -= 1
        # Also decrement RPM_left for the current session interaction
        if st.session_state.quota_usage[model_name]["RPM_left"] > 0:
             st.session_state.quota_usage[model_name]["RPM_left"] -= 1


def get_cache_filename(prompt_text: str, images_data: list[bytes] = None, model_name: str = DEFAULT_MODEL):
    """Generate a unique filename for caching based on prompt, multiple images, and model name."""
    hash_input = f"{prompt_text}_{model_name}".encode()
    if images_data:
        for img_data in images_data:
            hash_input += img_data  # Include all images bytes in hash

    prompt_hash = hashlib.md5(hash_input).hexdigest()
    return os.path.join(CACHE_DIR, f"{prompt_hash}.json")


def load_cache(prompt_text: str, images_data: list[bytes] = None, model_name: str = DEFAULT_MODEL):
    """Load cached response if available."""
    cache_file = get_cache_filename(prompt_text, images_data, model_name)
    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_cache(prompt_text: str, response_text: str, images_data: list[bytes] = None, model_name: str = DEFAULT_MODEL):
    """Save response in cache."""
    cache_file = get_cache_filename(prompt_text, images_data, model_name)
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump({"response": response_text}, f, indent=4, ensure_ascii=False)


def encode_image(image: Image.Image) -> bytes:
    """Convert an image to base64-encoded bytes."""
    with io.BytesIO() as buffer:
        image.save(buffer, format="PNG")
        return buffer.getvalue()


def generate_response(prompt_text: str, images: list[Image.Image] | Image.Image = None, model_name: str = None):
    """Generate AI response using Gemini with optional multiple image input and model selection."""
    initialise_quotas()
    
    # Use default model if not provided
    if not model_name:
        model_name = DEFAULT_MODEL

    if images is None:
        images_list = []
    elif isinstance(images, list):
        images_list = images
    else:
        images_list = [images]

    # Encode images if available
    images_data = [encode_image(img) for img in images_list] if images_list else None

    # Modify prompt if images are included
    full_prompt = prompt_text
    if images_list:
        full_prompt += f"\n\n(Note: This prompt includes {len(images_list)} image(s) for reference.)"

    # Check cache before calling API
    cached_response = load_cache(full_prompt, images_data, model_name)
    if cached_response:
        return cached_response["response"]

    try:
        # Prepare input content
        parts = [{"text": prompt_text}]

        # If images are provided, append them
        if images_data:
            for img_data in images_data:
                parts.append({
                    "inline_data": {
                        "mime_type": "image/png",
                        "data": base64.b64encode(img_data).decode(),
                    }
                })

        # Call Gemini API
        response = client.models.generate_content(
                model=model_name, contents=[{"role": "user", "parts": parts}]
            )

        # Extract response text
        response_text = response.text

        # Update local quota tracking on success
        update_quota(model_name)

        # Cache the response
        save_cache(full_prompt, response_text, images_data, model_name)

        return response_text

    except Exception as e:
        return f"Error: {str(e)}"