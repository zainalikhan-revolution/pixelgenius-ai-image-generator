import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# --- Page Configuration ---
st.set_page_config(page_title="PixelGenius", page_icon="🎨", layout="centered")
st.title("🎨 PixelGenius: AI Image Generator")
st.markdown("Generate images using **Hugging Face Stable Diffusion XL**.")

# --- Hugging Face API Settings ---
API_TOKEN = st.secrets["HF_API_TOKEN"]
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# --- Generate Image Function ---
def generate_image(prompt):
    payload = {
        "inputs": prompt,
        "options": {"wait_for_model": True}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        st.error(f"❌ API Error {response.status_code}: {response.text}")
        return None
    try:
        return Image.open(BytesIO(response.content))
    except Exception as e:
        st.error(f"⚠️ Error reading image: {e}")
        return None

# --- User Prompt Form ---
with st.form("prompt_form"):
    prompt = st.text_input("📝 Enter your image description (prompt):")
    style = st.selectbox("🎨 Choose image style:", ["Realistic", "Cartoon", "3D Art"])
    submitted = st.form_submit_button("Generate Image")

if submitted:
    if not prompt.strip():
        st.warning("⚠️ Please enter a prompt.")
    else:
        final_prompt = f"{prompt}, {style} style"
        with st.spinner("⏳ Generating image..."):
            image = generate_image(final_prompt)
            if image:
                st.image(image, caption=f"🖼️ Style: {style}", use_column_width=True)
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                st.download_button(
                    label="⬇️ Download Image",
                    data=buffered.getvalue(),
                    file_name="pixelgenius_image.png",
                    mime="image/png"
                )
