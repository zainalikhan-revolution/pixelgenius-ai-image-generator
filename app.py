# -----------------------------------------------
# PixelGenius - Full Updated Version (Phase 2, 3, and 4)
# -----------------------------------------------

import streamlit as st
import requests
from PIL import Image, ImageEnhance
from io import BytesIO
import zipfile
import base64
import os

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
style = st.sidebar.selectbox("Choose style:", ["Realistic", "3D Art", "Cartoon", "Digital Painting"])
num_images = st.sidebar.selectbox("Number of images:", [1, 2, 3, 4])
generate_button = st.sidebar.button("Generate")

st.sidebar.markdown("---")
st.sidebar.header("🎛️ Filters")
brightness = st.sidebar.slider("Brightness", 0.5, 2.0, 1.0)
contrast = st.sidebar.slider("Contrast", 0.5, 2.0, 1.0)
sharpness = st.sidebar.slider("Sharpness", 0.5, 2.0, 1.0)

# -----------------------------
# Image Generation and Display
# -----------------------------
if generate_button:
    if not prompt:
        st.warning("Please enter a prompt first.")
    else:
        final_prompt = f"{prompt}, {style} style"
        st.subheader("🖼️ Generated Images")
        with st.spinner("Generating images..."):
            columns = st.columns(num_images)
            session_images = []
            for i in range(num_images):
                img = generate_image(final_prompt)
                if img:
                    filtered_img = apply_filters(img, brightness, contrast, sharpness)
                    columns[i].image(filtered_img, use_column_width=True, caption=f"Image {i+1}")
                    session_images.append(filtered_img)

            if session_images:
                st.markdown(get_image_download_link(session_images), unsafe_allow_html=True)
                st.session_state["history"] = session_images

# -----------------------------
# Image History (Session)
# -----------------------------
if "history" in st.session_state:
    st.markdown("---")
    st.subheader("🕘 Image History")
    cols = st.columns(len(st.session_state["history"]))
    for idx, img in enumerate(st.session_state["history"]):
        cols[idx].image(img, caption=f"Previous Image {idx+1}", use_column_width=True)


