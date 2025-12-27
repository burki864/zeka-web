import streamlit as st
import requests
from io import BytesIO
from datetime import datetime

# ------------------ AYARLAR ------------------
st.set_page_config(
    page_title="Burak GPT",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Burak GPT")
st.caption("Yazı • Araştırma • Görsel")

# ------------------ SESSION ------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "mode" not in st.session_state:
    st.session_state.mode = "chat"

# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.subheader("Mod Seç")
    mode = st.radio(
        "Ne yapmak istiyorsun?",
        ["Sohbet", "Araştırma", "Görsel Oluştur"],
        label_visibility="collapsed"
    )

    if mode == "Sohbet":
        st.session_state.mode = "chat"
    elif mode == "Araştırma":
        st.session_state.mode = "research"
    else:
        st.session_state.mode = "image"

# ------------------ FONKSİYON ------------------
def generate_image(prompt):
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
    headers = {
        "Authorization": f"Bearer {st.secrets['HF_TOKEN']}"
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": prompt},
        timeout=60
    )

    if response.status_code != 200:
        return None

    return response.content

# ------------------ CHAT GEÇMİŞİ ------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])

    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])

    elif msg["role"] == "image":
        st.image(msg["content"], use_container_width=True)

        st.download_button(
            label="⬇️ Görseli indir",
            data=msg["content"],
            file_name=f"burak_gpt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            mime="image/png"
        )

# ------------------ INPUT ------------------
user_input = st.chat_input("Bir şey yaz...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # -------- SOHBET --------
    if st.session_state.mode == "chat":
        reply = f"🤖 Bunu düşündüm:\n\n{user_input}"
        st.session_state.messages.append({
            "role": "assistant",
            "content": reply
        })

    # -------- ARAŞTIRMA --------
    elif st.session_state.mode == "research":
        reply = (
            "🔎 Araştırma modu aktif.\n\n"
            f"Başlık: {user_input}\n\n"
            "Bu konu hakkında detaylı bir özet hazırlanabilir."
        )
        st.session_state.messages.append({
            "role": "assistant",
            "content": reply
        })

    # -------- GÖRSEL --------
    elif st.session_state.mode == "image":
        with st.spinner("🎨 Görsel oluşturuluyor..."):
            image_bytes = generate_image(user_input)

        if image_bytes:
            st.session_state.messages.append({
                "role": "image",
                "content": image_bytes
            })
        else:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "❌ Görsel üretilemedi. Biraz sonra tekrar dene."
            })

    st.rerun()
