import streamlit as st
from gradio_client import Client
from PIL import Image
from io import BytesIO
import requests

# =====================
# PAGE
# =====================
st.set_page_config(
    page_title="Burak GPT",
    page_icon="🧠",
    layout="centered"
)

st.markdown("## 🧠 Burak GPT")
st.caption("Yazı · Araştırma · Görsel")

# =====================
# STATE
# =====================
if "history" not in st.session_state:
    st.session_state.history = []

# =====================
# IMAGE SERVICE
# =====================
def generate_image(prompt: str):
    try:
        client = Client("burak12321/burak-gpt-image")
        result = client.predict(prompt=prompt, api_name="/generate")

        if isinstance(result, list):
            result = result[0]

        if result and result.get("url"):
            r = requests.get(result["url"], timeout=45)
            return Image.open(BytesIO(r.content)).convert("RGB")
    except:
        pass
    return None

# =====================
# TEXT SERVICE
# =====================
def generate_text(prompt, mode):
    if mode == "Yazı":
        return f"{prompt}\n\nBu konu üzerine sade, anlaşılır ve özgün bir metin hazırlandı."

    if mode == "Araştırma":
        return (
            f"{prompt}\n\n"
            f"- Tanım\n"
            f"- Kullanım alanları\n"
            f"- Avantajlar\n"
            f"- Güncel örnekler"
        )

    return f"{prompt} üzerine konuşabiliriz. Detaylandırmak ister misin?"

# =====================
# UI
# =====================
mode = st.selectbox(
    "Mod",
    ["Sohbet", "Yazı", "Araştırma", "Görsel"]
)

prompt = st.text_input(
    "Girdi",
    placeholder="örn: istanbul manzarası"
)

send = st.button("Gönder")

# =====================
# ACTION
# =====================
if send and prompt:

    if mode == "Görsel":
        with st.spinner("Görsel oluşturuluyor..."):
            img = generate_image(prompt)

        if img:
            st.image(img, use_container_width=True)

            buffer = BytesIO()
            img.save(buffer, format="PNG")

            st.download_button(
                "İndir",
                buffer.getvalue(),
                "burak-gpt.png",
                "image/png"
            )
        else:
            st.warning("Görsel üretilemedi.")

    else:
        with st.spinner("Yanıt hazırlanıyor..."):
            answer = generate_text(prompt, mode)

        st.session_state.history.append((prompt, answer))

# =====================
# HISTORY
# =====================
for q, a in reversed(st.session_state.history[-5:]):
    st.markdown(f"**Sen:** {q}")
    st.markdown(f"**Burak GPT:** {a}")
    st.divider()
