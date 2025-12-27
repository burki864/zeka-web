import time
import streamlit as st
from openai import OpenAI

# =============================
# OpenAI Client
# =============================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# =============================
# Sayfa Ayarı
# =============================
st.set_page_config(
    page_title="Burak GPT",
    page_icon="🤖",
    layout="centered"
)

# =============================
# CSS (Profesyonel UI)
# =============================
st.markdown("""
<style>
body {
    background-color: #fafafa;
}
.chat-container {
    max-width: 720px;
    margin: auto;
}
.chat-box {
    background: #ffffff;
    padding: 14px;
    border-radius: 14px;
    margin-top: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
}
.user-box {
    background: #dcf8c6;
    padding: 12px;
    border-radius: 14px;
    margin-top: 10px;
    text-align: right;
}
.dot {
    width: 12px;
    height: 12px;
    background: #333;
    border-radius: 50%;
    animation: pulse 1.2s infinite;
    display: inline-block;
    margin-right: 6px;
}
@keyframes pulse {
    0% { transform: scale(1); opacity: .4; }
    50% { transform: scale(1.5); opacity: 1; }
    100% { transform: scale(1); opacity: .4; }
}
.send-btn button {
    width: 100%;
    border-radius: 12px;
    height: 42px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# =============================
# Başlık
# =============================
st.markdown("<h2 style='text-align:center;'>🤖 Burak GPT</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>Samimi • Hızlı • Akıllı</p>", unsafe_allow_html=True)

# =============================
# Hafıza
# =============================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "Senin adın Burak GPT. "
                "Samimi, kısa ve insan gibi cevap ver. "
                "Bazen düşündüğünü belli et. "
                "Türkçe konuş."
            )
        }
    ]

# =============================
# Mesajları Göster
# =============================
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"<div class='user-box'>{msg['content']}</div>",
            unsafe_allow_html=True
        )
    elif msg["role"] == "assistant":
        st.markdown(
            f"<div class='chat-box'><strong>Burak GPT:</strong> {msg['content']}</div>",
            unsafe_allow_html=True
        )

st.markdown("</div>", unsafe_allow_html=True)

# =============================
# Input + Buton
# =============================
with st.container():
    user_input = st.text_area(
        "Mesajın",
        placeholder="Burak GPT’ye bir şey yaz…",
        height=80
    )

    send = st.button("📨 Gönder", key="send", use_container_width=True)

# =============================
# Hafızayı Metne Çevir
# =============================
def hafiza_metni():
    metin = ""
    for m in st.session_state.messages:
        metin += f"{m['role'].upper()}: {m['content']}\n"
    return metin

# =============================
# OpenAI Cevap
# =============================
def burak_gpt_cevap():
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=hafiza_metni()
    )
    return response.output_text.strip()

# =============================
# Yavaş Yazma
# =============================
def yavas_yaz(text):
    alan = st.empty()
    yazilan = ""
    for kelime in text.split():
        yazilan += kelime + " "
        alan.markdown(
            f"<div class='chat-box'><strong>Burak GPT:</strong> {yazilan}</div>",
            unsafe_allow_html=True
        )
        time.sleep(0.05)

# =============================
# Gönderme Mantığı
# =============================
if send and user_input.strip():
    st.session_state.messages.append({
        "role": "user",
        "content": user_input.strip()
    })

    thinking = st.empty()
    thinking.markdown(
        "<div class='dot'></div> Burak GPT düşünüyor...",
        unsafe_allow_html=True
    )

    cevap = burak_gpt_cevap()

    thinking.empty()
    yavas_yaz(cevap)

    st.session_state.messages.append({
        "role": "assistant",
        "content": cevap
    })

    st.rerun()
