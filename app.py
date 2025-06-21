# -----------------------------------------------
# PixelGenius - Phase 4+ Enhanced Version (Replicate)
# -----------------------------------------------

import streamlit as st
import replicate
from PIL import Image, ImageEnhance
from io import BytesIO
import zipfile
import base64
import requests

# -----------------------------
# Config and Branding
# -----------------------------
st.set_page_config(
    page_title="PixelGenius - AI Image Generator",
    page_icon="🎨",
    layout="wide"
)

# -----------------------------
# Logo and Description
# -----------------------------
st.image("assets/logo.png", width=140)
st.title("🎨 PixelGenius: AI Image Generator")
st.caption("Create high-quality images using Stable Diffusion XL with real-time filters, style previews, and multi-image generation.")

st.divider()

# -----------------------------
# Replicate API Setup
# -----------------------------
REPLICATE_TOKEN = st.secrets["REPLICATE_API_TOKEN"]
client = replicate.Client(api_token=REPLICATE_TOKEN)

# -----------------------------
# Utility Functions
# -----------------------------
def generate_image(prompt):
    try:
        output = client.run(
            "stability-ai/stable-diffusion-xl",  # ✅ Fixed model name
            input={
                "prompt": prompt,
                "width": 1024,
                "height": 1024
            }
        )
        response = requests.get(output[0])
        return Image.open(BytesIO(response.content))
    except Exception as e:
        st.error(f"Image generation failed: {e}")
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
# Sidebar Settings
# -----------------------------
st.sidebar.header("🧠 Generator Controls")
style = st.sidebar.selectbox("🎨 Choose Style", ["Realistic", "Anime", "Sketch", "Cyberpunk"])
num_images = st.sidebar.slider("🖼️ Number of Images", 1, 4, 1)

st.sidebar.markdown("### 🎛️ Filters")
brightness = st.sidebar.slider("Brightness", 0.5, 2.0, 1.0)
contrast = st.sidebar.slider("Contrast", 0.5, 2.0, 1.0)
sharpness = st.sidebar.slider("Sharpness", 0.5, 2.0, 1.0)

# -----------------------------
# Main Prompt + UI
# -----------------------------
st.markdown("### ✏️ Enter your prompt")
prompt = st.text_input("For example: *A futuristic city at sunset, in anime style*")

if prompt:
    if st.button("🚀 Generate Images"):
        st.info(f"Generating {num_images} image(s) with **{style}** style...")
        images = []
        history = st.session_state.get("prompt_history", [])
        history.append(prompt)
        st.session_state.prompt_history = history

        with st.spinner("Generating..."):
            for _ in range(num_images):
                styled_prompt = f"{style} style - {prompt}"
                img = generate_image(styled_prompt)
                if img:
                    filtered_img = apply_filters(img, brightness, contrast, sharpness)
                    images.append(filtered_img)

        st.success("✅ Done!")

        # ✅ Prevent crash if no images
        if images:
            cols = st.columns(len(images))
            for i, img in enumerate(images):
                with cols[i]:
                    st.image(img, caption=f"Image {i+1}", use_column_width="always")
            st.markdown(get_image_download_link(images), unsafe_allow_html=True)
        else:
            st.warning("⚠️ No images were generated. Please check your API credits or try again with a different prompt.")

        st.divider()
        st.markdown("### 🕘 Prompt History")
        for i, p in enumerate(reversed(history[-5:]), 1):
            st.markdown(f"{i}. _{p}_")

else:
    st.info("👈 Enter a prompt above to start generating images.")








