import streamlit as st
from gradio_client import Client
from PIL import Image
from io import BytesIO
import requests

# =========================
# SAYFA AYARLARI
# =========================
st.set_page_config(
    page_title="🧠 Burak GPT – Görsel Üretici",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Burak GPT – Görsel Üretici")
st.caption("Stable Diffusion + Hugging Face Space")

# =========================
# GÖRSEL ÜRETEN FONKSİYON
# =========================
def generate_image_from_space(prompt):
    try:
        client = Client("burak12321/burak-gpt-image")

        result = client.predict(
            prompt=prompt,
            api_name="/generate"
        )

        # HF bazen liste döndürür
        if isinstance(result, list) and len(result) > 0:
            result = result[0]

        if isinstance(result, dict) and result.get("url"):
            response = requests.get(result["url"], timeout=60)
            image = Image.open(BytesIO(response.content)).convert("RGB")
            return image

        return None

    except Exception as e:
        st.error(f"Hata oluştu: {e}")
        return None

# =========================
# ARAYÜZ
# =========================
prompt = st.text_input(
    "Ne çizilsin?",
    placeholder="örnek: istanbul manzarası, sinematik, gece"
)

col1, col2 = st.columns(2)

with col1:
    generate_btn = st.button("🎨 Görsel Üret")

with col2:
    clear_btn = st.button("🧹 Temizle")

if clear_btn:
    st.experimental_rerun()

# =========================
# ÜRETİM
# =========================
if generate_btn and prompt.strip():
    with st.spinner("🧠 Burak GPT düşünüyor..."):
        img = generate_image_from_space(prompt)

    if img:
        st.success("✅ Görsel üretildi")
        st.image(img, use_container_width=True)

        # İNDİRME BUTONU
        buf = BytesIO()
        img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        st.download_button(
            label="⬇️ Görseli İndir",
            data=byte_im,
            file_name="burak_gpt.png",
            mime="image/png"
        )
    else:
        st.error("❌ Görsel üretilemedi. Biraz sonra tekrar dene.")

elif generate_btn:
    st.warning("✏️ Önce bir şey yaz kral")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("🧠 Burak GPT • Yazı • Araştırma • Görsel")
