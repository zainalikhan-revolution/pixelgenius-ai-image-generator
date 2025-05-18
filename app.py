import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import base64

st.set_page_config(page_title="PixelGenius - AI Image Generator", page_icon="🎨", layout="centered")

st.title("🎨 PixelGenius: AI Image Generator")
st.markdown("Generate stunning realistic images using Hugging Face's Stable Diffusion XL model.")

API_TOKEN = st.secrets["HF_API_TOKEN"]
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def generate_image(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "width": 1024,
            "height": 1024,
            "num_inference_steps": 50
        }
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        st.error(f"API Error {response.status_code}: {response.text}")
        return None
    # The response is a JSON with an array of base64 images
    data = response.json()
    if "images" in data:
        img_data = data["images"][0]
        img_bytes = base64.b64decode(img_data.split(",",1)[1])  # Remove data:image/png;base64,
        img = Image.open(BytesIO(img_bytes))
        return img
    else:
        st.error("No images returned by API.")
        return None

prompt = st.text_input("Enter your image description (prompt):")
if st.button("Generate Image"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Generating image..."):
            img = generate_image(prompt)
            if img:
                st.image(img, caption="Generated Image", use_column_width=True)
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                st.download_button(
                    label="Download Image",
                    data=buffered.getvalue(),
                    file_name="pixelgenius_image.png",
                    mime="image/png"
                )


