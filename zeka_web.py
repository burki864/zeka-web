import streamlit as st
import time
import random

st.set_page_config(page_title="Ben", page_icon="⚫")

# CSS – nabız atan siyah nokta
st.markdown("""
<style>
.thinking-dot {
  width: 14px;
  height: 14px;
  background-color: black;
  border-radius: 50%;
  animation: pulse 1.2s infinite ease-in-out;
  margin: 10px 0;
}

@keyframes pulse {
  0% { transform: scale(0.7); opacity: 0.5; }
  50% { transform: scale(1.2); opacity: 1; }
  100% { transform: scale(0.7); opacity: 0.5; }
}
</style>
""", unsafe_allow_html=True)

st.title("⚫ Ben")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları göster
for role, content in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(content)

# Kullanıcı girişi
prompt = st.chat_input("Bana yaz...")

if prompt:
    # Kullanıcı mesajı
    st.session_state.messages.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # Ben düşünüyorum efekti
    with st.chat_message("assistant"):
        dot = st.empty()
        text = st.empty()

        thinking_texts = [
            "🧠 Bir bakıyorum...",
            "🤔 Düşünüyorum...",
            "🔍 Araştırıyorum...",
            "⏳ Bir saniye..."
        ]

        dot.markdown('<div class="thinking-dot"></div>', unsafe_allow_html=True)
        text.markdown(random.choice(thinking_texts))

        time.sleep(random.uniform(1.5, 2.5))

        dot.empty()
        text.empty()

        # Demo cevap (buraya AI bağlanır)
        response = f"Tamam, anladım. **{prompt}** hakkında konuşabiliriz."

        st.markdown(response)
        st.session_state.messages.append(("assistant", response))
