import streamlit as st
import requests
from io import BytesIO
from PIL import Image
from openai import OpenAI
from gradio_client import Client

# ======================
# PAGE
# ======================
st.set_page_config(
    page_title="Burak GPT",
    page_icon="🧠",
    layout="centered"
)

st.markdown("""
<style>
body { background-color:#0f0f10; color:#f5f5f7; }
.block-container { max-width:720px; }
.chat-bubble {
    padding:14px 18px;
    border-radius:16px;
    margin:10px 0;
    line-height:1.5;
}
.user { background:#1f1f22; text-align:right; }
.bot { background:#161617; }
.mode { font-size:12px; opacity:.6; text-align:center; }
button { border-radius:10px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("## 🧠 Burak GPT")
st.markdown("<div class='mode'>Think less. Build more.</div>", unsafe_allow_html=True)

# ======================
# CLIENTS
# ======================
openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
image_client = Client("burak12321/burak-gpt-image")

# ======================
# SESSION
# ======================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ======================
# FUNCTIONS
# ======================
def burak_gpt(prompt, mode):
    styles = {
        "Sohbet": "Kısa, zeki, kendinden emin konuş. Emoji dozunda 😎",
        "Yazı": "Profesyonel, sade, akıcı yaz.",
        "Araştırma": "Maddeli, net, öğretici anlat."
    }

    response = openai_client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role":"system","content":styles.get(mode,"")},
            {"role":"user","content":prompt}
        ]
    )
    return response.output_text.strip()

def generate_image(prompt):
    try:
        result = image_client.predict(prompt=prompt, api_name="/generate")
        if isinstance(result, list):
            result = result[0]
        if result and result.get("url"):
            img_data = requests.get(result["url"], timeout=60).content
            return Image.open(BytesIO(img_data))
    except:
        return None

# ======================
# UI
# ======================
mode = st.selectbox("Mod", ["Sohbet", "Yazı", "Araştırma", "Görsel"])

user_input = st.text_input("Mesaj", placeholder="Burak GPT’ye yaz…")

send = st.button("Gönder")

# ======================
# ACTION
# ======================
if send and user_input:
    st.session_state.messages.append(("user", user_input))

    if mode == "Görsel":
        with st.spinner("🎨 Görsel oluşturuluyor..."):
            img = generate_image(user_input)

        if img:
            st.image(img, use_container_width=True)
            buf = BytesIO()
            img.save(buf, format="PNG")
            st.download_button("⬇️ İndir", buf.getvalue(), "burak-gpt.png", "image/png")
        else:
            st.error("Görsel üretilemedi.")

    else:
        with st.spinner("🧠 Burak GPT düşünüyor..."):
            reply = burak_gpt(user_input, mode)
        st.session_state.messages.append(("bot", reply))

# ======================
# CHAT
# ======================
st.divider()
for role, msg in st.session_state.messages[-12:]:
    css = "user" if role == "user" else "bot"
    st.markdown(f"<div class='chat-bubble {css}'>{msg}</div>", unsafe_allow_html=True)
