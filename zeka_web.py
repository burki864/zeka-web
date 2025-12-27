import streamlit as st
import time
import random

# ---------------- SAYFA AYARLARI ----------------
st.set_page_config(
    page_title="Burak GPT",
    page_icon="🤖",
    layout="centered"
)

# ---------------- CSS TASARIM ----------------
st.markdown("""
<style>
.chat-container {
    max-width: 750px;
    margin: auto;
}
.user-msg {
    background-color: #DCF8C6;
    padding: 12px 16px;
    border-radius: 15px;
    margin: 8px 0;
    text-align: right;
    font-size: 16px;
}
.bot-msg {
    background-color: #F1F0F0;
    padding: 12px 16px;
    border-radius: 15px;
    margin: 8px 0;
    text-align: left;
    font-size: 16px;
}
.bot-name {
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# ---------------- BAŞLIK ----------------
st.markdown("<h2 style='text-align:center;'>🤖 Burak GPT</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>Senin dijital kardeşin</p>", unsafe_allow_html=True)

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# ---------------- MESAJLARI GÖSTER ----------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(
            f"<div class='bot-msg'><span class='bot-name'>Burak GPT:</span> {msg['content']}</div>",
            unsafe_allow_html=True
        )

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- EMOJİ HAVUZU ----------------
emoji_list = ["😎", "🔥", "🤖", "✨", "🚀", "😉", "💡"]

def burak_gpt_response(user_text):
    emoji = random.choice(emoji_list)
    return f"{emoji} {user_text.capitalize()} hakkında düşündüm… Sana net ve kısa anlatayım."

# ---------------- INPUT + BUTON ----------------
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "Mesajın",
        placeholder="Burak GPT’ye yaz…",
        key="input_text"
    )
    send_button = st.form_submit_button("Gönder 🚀")

# ---------------- MESAJ GÖNDERME ----------------
if send_button and user_input.strip():
    # Kullanıcı mesajı
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Yazıyor efekti
    with st.spinner("Burak GPT düşünüyor..."):
        time.sleep(0.8)

    # Bot cevabı
    bot_reply = burak_gpt_response(user_input)
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    st.rerun()
