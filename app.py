# -----------------------------------------------
# PixelGenius - Full Updated Version (Phase 2, 3, and 4)
# -----------------------------------------------

import streamlit as st
import requests
from PIL import Image, ImageEnhance
from io import BytesIO
import zipfile
import base64

# -----------------------------
# Config and Branding
# -----------------------------
st.set_page_config(
    page_title="PixelGenius - AI Image Generator",
    page_icon="🎨",
    layout="wide"
)

# -----------------------------
# Branding - Logo and Title
# -----------------------------
st.image("assets/logo.png", width=150)
st.title("🎨 PixelGenius: AI Image Generator")
st.markdown("Generate high-quality images using **Stable Diffusion XL** with filters, download options, and history.")

# -----------------------------
# Hugging Face API Setup
# -----------------------------
API_TOKEN = st.secrets["HF_API_TOKEN"]
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

# -----------------------------
# Utilities
# -----------------------------
def generate_image(prompt):
    payload = {"inputs": prompt, "options": {"wait_for_model": True}}
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        st.error(f"API Error {response.status_code}: {response.text}")
        return None

def apply_filters(img, brightness, contrast, sharpness):
    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = ImageEnhance.Sharpness(img).enhance(sharpness)
    return img

def get_image_download_link(img_list):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for idx, img in enumerate(img_list):
            img_buffer = BytesIO()
            img.save(img_buffer, format="PNG")
            zip_file.writestr(f"image_{idx+1}.png", img_buffer.getvalue())
    zip_buffer.seek(0)
    b64 = base64.b64encode(zip_buffer.read()).decode()
    href = f'<a href="data:application/zip;base64,{b64}" download="pixelgenius_images.zip">⬇️ Download All Images (ZIP)</a>'
    return href

# -----------------------------
# Sidebar UI
# -----------------------------
st.sidebar.header("🛠️ Generator Settings")

prompt = st.sidebar.text_input("Enter your image description:")
style = st.sidebar.selectbox("Choose style:", ["Realistic", "Anime", "Sketch", "Cyberpunk"])
num_images = st.sidebar.slider("Number of images:", 1, 4, 1)

st.sidebar.markdown("### 🎛️ Filters")
brightness = st.sidebar.slider("Brightness", 0.5, 2.0, 1.0)
contrast = st.sidebar.slider("Contrast", 0.5, 2.0, 1.0)
sharpness = st.sidebar.slider("Sharpness", 0.5, 2.0, 1.0)

generate = st.sidebar.button("🎨 Generate")

# -----------------------------
# Main UI
# -----------------------------
if generate:
    if not prompt:
        st.warning("❗ Please enter a prompt.")
    else:
        images = []
        with st.spinner("🚀 Generating images..."):
            for _ in range(num_images):
                image = generate_image(f"{style} style - {prompt}")
                if image:
                    filtered_image = apply_filters(image, brightness, contrast, sharpness)
                    images.append(filtered_image)

        for img in images:
            st.image(img, use_column_width=True)

        st.markdown(get_image_download_link(images), unsafe_allow_html=True)




