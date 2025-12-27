import time
import streamlit as st
from openai import OpenAI

# =============================
# OpenAI client
# =============================
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# =============================
# Sayfa ayarı
# =============================
st.set_page_config(
    page_title="Burak GPT",
    layout="centered"
)

# =============================
# CSS
# =============================
st.markdown("""
<style>
.dot {
    width: 14px;
    height: 14px;
    background: black;
    border-radius: 50%;
    animation: pulse 1.2s infinite;
    display: inline-block;
    margin-right: 8px;
}
@keyframes pulse {
    0% { transform: scale(1); opacity: .4; }
    50% { transform: scale(1.6); opacity: 1; }
    100% { transform: scale(1); opacity: .4; }
}
.chat-box {
    background: #f5f5f5;
    padding: 12px;
    border-radius: 10px;
    margin-top: 10px;
}
.user-box {
    background: #e8e8e8;
    padding: 10px;
    border-radius: 10px;
    margin-top: 10px;
    text-align: right;
}
</style>
""", unsafe_allow_html=True)

# =============================
# Başlık
# =============================
st.markdown("<h2>🤖 Burak GPT</h2>", unsafe_allow_html=True)

# =============================
# HAFIZA
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
# Geçmiş mesajlar
# =============================
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

# =============================
# Input
# =============================
user_input = st.text_input(
    "Burak GPT'ye yaz",
    placeholder="Bir şey sor…"
)

# =============================
# Hafızayı metne çevir
# =============================
def hafiza_metni():
    metin = ""
    for m in st.session_state.messages:
        rol = m["role"].upper()
        metin += f"{rol}: {m['content']}\n"
    return metin

# =============================
# OpenAI cevap
# =============================
def burak_gpt_cevap():
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=hafiza_metni()
    )
    return response.output_text.strip()

# =============================
# Yavaş yazma
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
        time.sleep(0.06)

# =============================
# Yeni mesaj
# =============================
if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
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
