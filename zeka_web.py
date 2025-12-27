import streamlit as st
from openai import OpenAI

# ---------- PAGE ----------
st.set_page_config(
    page_title="BurakGPT",
    page_icon="🧠",
    layout="wide"
)

# ---------- STYLE ----------
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #1b1f2a, #0e1117);
    color: #ffffff;
}
.block-container {
    padding-top: 2rem;
}
.chat-box {
    background: #161b22;
    border-radius: 16px;
    padding: 20px;
    min-height: 400px;
}
.msg-user {
    text-align: right;
    color: #4fd1c5;
    margin-bottom: 10px;
}
.msg-ai {
    text-align: left;
    color: #e5e7eb;
    margin-bottom: 16px;
}
input {
    background-color: #0e1117 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- API ----------
if "OPENAI_API_KEY" not in st.secrets:
    st.error("OPENAI_API_KEY secrets içinde bulunamadı.")
    st.stop()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------- STATE ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- LAYOUT ----------
left, center, right = st.columns([1, 6, 1])

with left:
    st.markdown("### ⋯")
    st.caption("🔍 Araştırma")
    st.caption("🖼 Görsel")
    st.caption("💬 Sohbet")

with center:
    st.markdown("## 🧠 BurakGPT")
    chat = st.container()
    with chat:
        st.markdown('<div class="chat-box">', unsafe_allow_html=True)
        for role, content in st.session_state.messages:
            if role == "user":
                st.markdown(f'<div class="msg-user">{content}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="msg-ai">{content}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown(" ")

# ---------- INPUT ----------
user_input = st.text_input("Mesajını yaz", placeholder="BurakGPT’ye sor…", label_visibility="collapsed")

if st.button("Gönder ➤", use_container_width=True):
    if user_input.strip():
        st.session_state.messages.append(("user", user_input))

        with st.spinner("Düşünüyorum…"):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Profesyonel, net ve yardımcı bir yapay zekasın."},
                    *[
                        {"role": r, "content": c}
                        for r, c in st.session_state.messages
                    ]
                ]
            )

        ai_text = response.choices[0].message.content
        st.session_state.messages.append(("ai", ai_text))
        st.rerun()
