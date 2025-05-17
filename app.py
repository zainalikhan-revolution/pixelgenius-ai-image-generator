import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="PixelGenius - AI Image Generator", layout="centered")

st.title("🎨 PixelGenius: AI Image Generator")
st.write("Generate stunning images using Hugging Face's Stable Diffusion API.")

# Your Hugging Face API token
API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4"

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

def generate_image(prompt, style="Realistic"):
    # Prepare payload with style if needed (you can customize this)
    data = {
        "inputs": prompt,
        # Add parameters for style customization if API supports it
    }
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code != 200:
        st.error(f"API Error: {response.status_code} - {response.text}")
        return None
    try:
        image_bytes = BytesIO(response.content)
        img = Image.open(image_bytes)
        return img
    except Exception as e:
        st.error(f"Image Processing Error: {e}")
        return None

# User input
prompt = st.text_input("Enter your image description (prompt):")
style = st.selectbox("Choose image style:", ["Realistic", "Cartoon", "3D Art"])

if st.button("Generate Image"):
    if not prompt.strip():
        st.warning("Please enter a prompt to generate an image.")
    else:
        with st.spinner("Generating image..."):
            img = generate_image(prompt, style)
            if img:
                st.image(img, caption=f"Style: {style}", use_column_width=True)
                # Download button
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                st.download_button("Download Image", data=buffered.getvalue(), file_name="pixelgenius_image.png", mime="image/png")

