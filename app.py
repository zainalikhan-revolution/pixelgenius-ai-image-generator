import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# -----------------------------
# App Configuration
# -----------------------------
st.set_page_config(
    page_title="PixelGenius Pro - AI Image Generator",
    page_icon="🎨",
    layout="wide"
)

# -----------------------------
# Sidebar UI
# -----------------------------
st.sidebar.title("🎨 PixelGenius Pro")
st.sidebar.markdown("Create beautiful AI-generated images with your own style!")

user_prompt = st.sidebar.text_input("📝 Enter your image prompt:")
style = st.sidebar.selectbox("🎨 Choose a style", ["Realistic", "3D Art", "Cartoon", "Digital Painting"])
generate_button = st.sidebar.button("🚀 Generate Image")

# -----------------------------
# API Settings
# -----------------------------
API_TOKEN = st.secrets["HF_API_TOKEN"]
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# -----------------------------
# Image Generation Function
# -----------------------------
def generate_image(prompt):
    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True}
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code != 200:
            st.error(f"❌ API Error {response.status_code}: {response.text}")
            return None
        return Image.open(BytesIO(response.content))
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
        return None

# -----------------------------
# Main Area
# -----------------------------
st.markdown(
    """
    <h1 style='text-align: center; color: #FF4B4B;'>🖼️ PixelGenius Pro</h1>
    <p style='text-align: center;'>Generate AI art from text using Hugging Face’s Stable Diffusion model.</p>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Generate & Display Image
# -----------------------------
if generate_button:
    if not user_prompt.strip():
        st.warning("⚠️ Please enter a prompt.")
    else:
        final_prompt = f"{user_prompt}, {style} style"
        with st.spinner("🎨 Generating your masterpiece..."):
            image = generate_image(final_prompt)
            if image:
                st.image(image, caption=f"🖼️ Style: {style}", use_column_width=True)

                # Download button
                buffer = BytesIO()
                image.save(buffer, format="PNG")
                st.download_button(
                    label="⬇️ Download Image",
                    data=buffer.getvalue(),
                    file_name="pixelgenius_image.png",
                    mime="image/png"
                )


