import streamlit as st
from gradio_client import Client

# ================== SAYFA ==================
st.set_page_config(
    page_title="Burak GPT",
    page_icon="🧠",
    layout="centered"
)

# ================== CSS ==================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
}
.chat {
    max-width:750px;
    margin:auto;
}
.user {
    background:#1e90ff;
    color:white;
    padding:12px 16px;
    border-radius:16px;
    margin:8px 0;
    text-align:right;
}
.bot {
    background:#f2f2f2;
    padding:12px 16px;
    border-radius:16px;
    margin:8px 0;
}
.control {
    display:flex;
    gap:6px;
}
.send button {
    background:black !important;
    color:white !important;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# ================== STATE ==================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "mode" not in st.session_state:
    st.session_state.mode = "Sohbet"

# ================== BAŞLIK ==================
st.markdown("<h2 style='text-align:center;color:white;'>🧠 Burak GPT</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;color:#ddd;'>Mod: {st.session_state.mode}</p>", unsafe_allow_html=True)

# ================== CHAT ==================
st.markdown("<div class='chat'>", unsafe_allow_html=True)
for r, c in st.session_state.messages:
    if r == "user":
        st.markdown(f"<div class='user'>{c}</div>", unsafe_allow_html=True)
    elif r == "bot":
        st.markdown(f"<div class='bot'><b>Burak GPT:</b> {c}</div>", unsafe_allow_html=True)
    elif r == "image":
        st.image(c)
st.markdown("</div>", unsafe_allow_html=True)

# ================== INPUT ==================
with st.form("chat", clear_on_submit=True):
    c1, c2, c3 = st.columns([1,6,1])

    with c1:
        mode = st.selectbox(
            "⋯",
            ["Sohbet", "Araştırma", "Görsel"],
            label_visibility="collapsed"
        )

    with c2:
        text = st.text_input(
            "",
            placeholder="Burak GPT’ye yaz…",
            label_visibility="collapsed"
        )

    with c3:
        send = st.form_submit_button("➤")

st.session_state.mode = mode

# ================== HF GÖRSEL ==================
def generate_image(prompt):
    client = Client("burak12321/burak-gpt-image")
    result = client.predict(prompt=prompt, api_name="/generate")
    return result["url"]

# ================== GÖNDER ==================
if send and text.strip():
    st.session_state.messages.append(("user", text))

    if mode == "Görsel":
        with st.spinner("🎨 Görsel üretiliyor..."):
            try:
                img = generate_image(text)
                st.session_state.messages.append(("image", img))
            except:
                st.session_state.messages.append(("bot", "❌ Görsel üretilemedi."))

    else:
        # geçici metin cevap
        st.session_state.messages.append((
            "bot",
            "✨ Sistem hazır. Yapay zeka motoru bir sonraki adımda aktif edilecek."
        ))

    st.rerun()
