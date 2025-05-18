import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="PixelGenius - AI Image Generator",
    page_icon="🎨",
    layout="centered"
)

# -----------------------------
# Title and Description
# -----------------------------
st.title("🎨 PixelGenius: AI Image Generator")
st.markdown("Generate stunning images using **Hugging Face's Stable Diffusion AI**. Just describe your image!")

# -----------------------------
# Hugging Face API Settings
# -----------------------------
API_TOKEN = "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"  # ✅ Your token inserted here
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"

HEADERS = {
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
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        if response.status_code != 200:
            st.error(f"❌ API Error {response.status_code}: {response.text}")
            return None
        return Image.open(BytesIO(response.content))
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
        return None

# -----------------------------
# User Input
# -----------------------------
with st.form("prompt_form"):
    user_prompt = st.text_input("📝 Enter your image description (prompt):")
    style = st.selectbox("🎨 Choose image style:", ["Realistic", "Cartoon", "3D Art", "Digital Painting"])
    submitted = st.form_submit_button("Generate Image")

# -----------------------------
# Generate & Display Image
# -----------------------------
if submitted:
    if not user_prompt.strip():
        st.warning("⚠️ Please enter a prompt to generate an image.")
    else:
        final_prompt = f"{user_prompt}, {style} style"
        with st.spinner("⏳ Generating your image... please wait..."):
            image = generate_image(final_prompt)
            if image:
                st.image(image, caption=f"🖼️ Style: {style}", use_column_width=True)

                # Download button
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                st.download_button(
                    label="⬇️ Download Image",
                    data=buffered.getvalue(),
                    file_name="pixelgenius_image.png",
                    mime="image/png"
                )

