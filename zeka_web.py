import streamlit as st
import time

st.set_page_config(page_title="Ben", layout="centered")

# CSS
st.markdown("""
<style>
.dot {
    width: 18px;
    height: 18px;
    background: black;
    border-radius: 50%;
    animation: pulse 1.4s infinite;
    display: inline-block;
    margin-right: 10px;
}
@keyframes pulse {
    0% { transform: scale(1); opacity: .4; }
    50% { transform: scale(1.6); opacity: 1; }
    100% { transform: scale(1); opacity: .4; }
}
.header {
    font-size: 36px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 10px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
  <div class="dot"></div>
  Ben
</div>
""", unsafe_allow_html=True)

st.write("")  
st.write("")  

# Session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat geçmişi
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# INPUT (ÖNEMLİ KISIM)
prompt = st.chat_input("Bana yaz…")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Ben düşünüyorum…"):
            time.sleep(1.2)
        cevap = f"Bunu düşündüm: {prompt}"
        st.write(cevap)

    st.session_state.messages.append({"role": "assistant", "content": cevap})
