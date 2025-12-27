import time
import streamlit as st
from openai import OpenAI

# OpenAI client
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# Sayfa ayarı
st.set_page_config(page_title="Ben", layout="centered")

# CSS
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

# Başlık
st.markdown("<h2>👤 Ben</h2>", unsafe_allow_html=True)

# 🧠 HAFIZA
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "Senin adın Ben. Samimi, net ve kısa cevap ver. Türkçe konuş."
        }
    ]

# Geçmişi göster
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="user-box">
            {msg["content"]}
        </div>
        """, unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f"""
        <div class="chat-box">
            <strong>Ben:</strong> {msg["content"]}
        </div>
        """, unsafe_allow_html=True)

# Input
user_input = st.text_input("Bana yaz", placeholder="Bir şey sor…")

def ben_cevap_ver():
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=st.session_state.messages
    )
    return response.output_text

# Yeni mesaj
if user_input:
    # Kullanıcı mesajı kaydet
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.spinner("Ben düşünüyor…"):
        time.sleep(1)
        cevap = ben_cevap_ver()

    # Ben cevabı kaydet
    st.session_state.messages.append({
        "role": "assistant",
        "content": cevap
    })

    st.rerun()
