import streamlit as st
import time
import requests
from openai import OpenAI
from gradio_client import Client
from PIL import Image
from io import BytesIO

# ================== API ==================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
TAVILY_API_KEY = st.secrets["TAVILY_API_KEY"]

# ================== SAYFA ==================
st.set_page_config(
    page_title="Burak GPT",
    page_icon="🤖",
    layout="centered"
)

# ================== CSS ==================
st.markdown("""
<style>
.chat-container { max-width: 760px; margin: auto; }
.user-msg {
    background:#DCF8C6; padding:12px 16px; border-radius:15px;
    margin:8px 0; text-align:right;
}
.bot-msg {
    background:#F1F0F0; padding:12px 16px; border-radius:15px;
    margin:8px 0;
}
.input-row {
    display:flex; gap:6px; align-items:center;
}
.send-btn button {
    background:black; color:white;
    border-radius:10px; width:42px; height:42px;
}
.mode {
    font-size:13px; color:gray; text-align:center;
}
</style>
""", unsafe_allow_html=True)

# ================== SESSION ==================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "mode" not in st.session_state:
    st.session_state.mode = "chat"

# ================== BAŞLIK ==================
st.markdown("<h2 style='text-align:center;'>🧠 Burak GPT</h2>", unsafe_allow_html=True)
st.markdown(
    f"<p class='mode'>Mod: {st.session_state.mode.upper()}</p>",
    unsafe_allow_html=True
)

# ================== CHAT ==================
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)

    elif msg["role"] == "assistant":
        st.markdown(
            f"<div class='bot-msg'><b>Burak GPT:</b> {msg['content']}</div>",
            unsafe_allow_html=True
        )

    elif msg["role"] == "image":
        st.image(msg["content"], use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ================== FONKSİYONLAR ==================
def tavily_search(query):
    url = "https://api.tavily.com/search"
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "advanced",
        "max_results": 5
    }
    r = requests.post(url, json=payload, timeout=30)
    data = r.json()
    return "\n".join([f"- {i['content']}" for i in data["results"]])


def gpt_text(prompt):
    res = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )
    return res.output_text.strip()


def generate_image_from_space(prompt):
    hf_client = Client("burak12321/burak-gpt-image")
    result = hf_client.predict(
        prompt=prompt,
        api_name="/generate"
    )

    if result and result.get("url"):
        r = requests.get(result["url"])
        img = Image.open(BytesIO(r.content)).convert("RGB")
        return img

    return None

# ================== INPUT ==================
with st.form("chat_form", clear_on_submit=True):
    col1, col2, col3 = st.columns([1,6,1])

    with col1:
        menu = st.selectbox(
            "⋯",
            ["💬 Sohbet", "🔍 Araştırma", "🖼️ Görsel"],
            label_visibility="collapsed"
        )

    with col2:
        user_input = st.text_input(
            "Mesaj",
            placeholder="Burak GPT’ye yaz…",
            label_visibility="collapsed"
        )

    with col3:
        send = st.form_submit_button("➤")

# ================== MOD ==================
if menu == "💬 Sohbet":
    st.session_state.mode = "chat"
elif menu == "🔍 Araştırma":
    st.session_state.mode = "research"
elif menu == "🖼️ Görsel":
    st.session_state.mode = "image"

# ================== GÖNDER ==================
if send and user_input.strip():
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.spinner("Burak GPT düşünüyor..."):
        time.sleep(0.4)

        # CHAT
        if st.session_state.mode == "chat":
            reply = gpt_text(
                f"Samimi, kısa ve emoji kullanarak cevap ver:\n{user_input}"
            )
            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

        # RESEARCH
        elif st.session_state.mode == "research":
            web = tavily_search(user_input)
            reply = gpt_text(
                f"Aşağıdaki internet sonuçlarını kullanarak açıkla:\n{web}"
            )
            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })

        # IMAGE
        elif st.session_state.mode == "image":
            img = generate_image_from_space(user_input)

            if img:
                st.session_state.messages.append({
                    "role": "image",
                    "content": img
                })
            else:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "❌ Görsel üretilemedi. Biraz sonra tekrar dene."
                })

    st.rerun()
