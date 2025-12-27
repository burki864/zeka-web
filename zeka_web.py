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
</style>
""", unsafe_allow_html=True)

# Başlık
st.markdown("<h2>👤 Ben</h2>", unsafe_allow_html=True)

# Input
user_input = st.text_input("Bana yaz", placeholder="Bir şey sor…")

# Cevap fonksiyonu
def ben_cevap_ver(metin):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
Senin adın Ben.
Kısa, net, samimi konuş.
Türkçe cevap ver.

Kullanıcı: {metin}
"""
    )
    return response.output_text

# Çalışma
if user_input:
    with st.spinner("Ben düşünüyor…"):
        time.sleep(1)
        cevap = ben_cevap_ver(user_input)

    st.markdown(f"""
    <div class="chat-box">
        <span class="dot"></span>
        <strong>Ben:</strong> {cevap}
    </div>
    """, unsafe_allow_html=True)
