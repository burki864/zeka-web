import streamlit as st
from openai import OpenAI
from gradio_client import Client
from PIL import Image

# =====================
# PAGE
# =====================
st.set_page_config(
    page_title="🧠 Burak GPT",
    page_icon="🧠",
    layout="centered"
)

# =====================
# CLIENTS
# =====================
openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
hf_client = Client(st.secrets["HF_SPACE_NAME"])

# =====================
# STYLE
# =====================
st.markdown("""
<style>
body {
    background: linear-gradient(180deg, #0f0f1a, #090912);
    color: white;
}
.chat {
    padding: 14px;
    border-radius: 12px;
    margin-bottom: 10px;
    background: rgba(255,255,255,0.06);
}
.user { color: #8fd3ff; text-align: right; }
.bot { color: #ffffff; }
</style>
""", unsafe_allow_html=True)

# =====================
# HEADER
# =====================
st.markdown("## 🧠 Burak GPT")
st.caption("Yazı • Araştırma • Görsel")

# =====================
# MODE
# =====================
mode = st.selectbox("⠇", ["Sohbet", "Araştırma", "Görsel"], label_visibility="collapsed")

# =====================
# SESSION
# =====================
if "chat" not in st.session_state:
    st.session_state.chat = []

# =====================
# SHOW CHAT
# =====================
for role, msg in st.session_state.chat:
    cls = "user" if role == "user" else "bot"
    st.markdown(f"<div class='chat {cls}'>{msg}</div>", unsafe_allow_html=True)

# =====================
# INPUT
# =====================
col1, col2 = st.columns([8,1])
with col1:
    prompt = st.text_input("", placeholder="Bir şey yaz...", label_visibility="collapsed")
with col2:
    send = st.button("➤")

# =====================
# GPT
# =====================
def ask_gpt(text, mode):
    system = {
        "Sohbet": "Samimi, zeki, emoji kullanan bir asistansın.",
        "Araştırma": "Maddeli, net ve öğretici cevap ver."
    }
    res = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system.get(mode, "")},
            {"role": "user", "content": text}
        ]
    )
    return res.choices[0].message.content

# =====================
# IMAGE
# =====================
def generate_image(prompt):
    result = hf_client.predict(prompt=prompt, api_name="/generate")
    return result["path"]

# =====================
# ACTION
# =====================
if send and prompt:
    st.session_state.chat.append(("user", prompt))

    with st.spinner("🧠 Burak GPT düşünüyor..."):
        if mode == "Görsel":
            try:
                img_path = generate_image(prompt)
                img = Image.open(img_path)
                st.image(img, use_container_width=True)
                with open(img_path, "rb") as f:
                    st.download_button("⬇ Görseli indir", f, "burak_gpt.png")
                st.session_state.chat.append(("bot", "🖼 Görsel hazır."))
            except Exception as e:
                st.session_state.chat.append(("bot", "❌ Görsel üretilemedi."))

        else:
            reply = ask_gpt(prompt, mode)
            st.session_state.chat.append(("bot", reply))

    st.rerun()
