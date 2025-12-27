import streamlit as st
from gradio_client import Client
from PIL import Image
from io import BytesIO
import requests
import time

# =========================
# SAYFA AYARLARI
# =========================
st.set_page_config(
    page_title="🧠 Burak GPT",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Burak GPT")
st.caption("Yazı • Sohbet • Araştırma • Görsel")

# =========================
# SESSION STATE
# =========================
if "chat" not in st.session_state:
    st.session_state.chat = []

# =========================
# GÖRSEL ÜRETME FONKSİYONU
# =========================
def generate_image(prompt):
    try:
        client = Client("burak12321/burak-gpt-image")
        result = client.predict(prompt=prompt, api_name="/generate")

        if isinstance(result, list):
            result = result[0]

        if isinstance(result, dict) and result.get("url"):
            r = requests.get(result["url"], timeout=60)
            img = Image.open(BytesIO(r.content)).convert("RGB")
            return img
        return None
    except:
        return None

# =========================
# CHAT / YAZI CEVAP MOTORU
# =========================
def generate_text(prompt, mode):
    time.sleep(1.2)  # düşünüyormuş hissi 😄

    if mode == "Sohbet":
        return f"🧠 Burak GPT: {prompt} hakkında konuşalım. Bana biraz daha detay ver."

    if mode == "Araştırma":
        return (
            f"🔍 **Araştırma Sonucu:**\n\n"
            f"'{prompt}' konusu hakkında genel bilgiler:\n\n"
            f"- Tanımı ve temel özellikleri\n"
            f"- Avantajları ve kullanım alanları\n"
            f"- Güncel örnekler\n\n"
            f"İstersen daha derine inebilirim."
        )

    return f"✍️ **Metin:**\n\n{prompt} üzerine özgün bir yazı hazırlandı."

# =========================
# MOD SEÇİMİ
# =========================
mode = st.radio(
    "Ne yapmak istiyorsun?",
    ["Sohbet", "Yazı", "Araştırma", "Görsel"],
    horizontal=True
)

user_input = st.text_input(
    "Bir şey yaz...",
    placeholder="örnek: istanbul manzarası, yapay zeka nedir, bana bir hikaye yaz"
)

# =========================
# GÖNDER BUTONU
# =========================
if st.button("🚀 Gönder") and user_input.strip():

    if mode == "Görsel":
        with st.spinner("🎨 Görsel oluşturuluyor..."):
            img = generate_image(user_input)

        if img:
            st.image(img, use_container_width=True)

            buf = BytesIO()
            img.save(buf, format="PNG")
            st.download_button(
                "⬇️ Görseli İndir",
                buf.getvalue(),
                file_name="burak_gpt.png",
                mime="image/png"
            )
        else:
            st.error("❌ Görsel üretilemedi, biraz sonra tekrar dene.")

    else:
        with st.spinner("🧠 Burak GPT düşünüyor..."):
            answer = generate_text(user_input, mode)

        st.session_state.chat.append(("Sen", user_input))
        st.session_state.chat.append(("Burak GPT", answer))

# =========================
# CHAT GEÇMİŞİ
# =========================
if st.session_state.chat:
    st.markdown("---")
    for who, msg in st.session_state.chat:
        if who == "Sen":
            st.markdown(f"**🧑 {who}:** {msg}")
        else:
            st.markdown(f"**🧠 {who}:** {msg}")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("🧠 Burak GPT • Hepsi tek yerde")
