import streamlit as st
import requests
from openai import OpenAI
from PIL import Image
from io import BytesIO

# ======================
# CONFIG
# ======================
st.set_page_config(
    page_title="🧠 Burak GPT",
    layout="centered",
    initial_sidebar_state="collapsed"
)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
HF_SPACE = st.secrets["HF_SPACE_URL"]

# ======================
# STYLE
# ======================
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top, #1e1e2f, #0e0e16);
    color: #ffffff;
}
.chat-box {
    background: rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 14px;
    margin-bottom: 10px;
}
.user {
    text-align: right;
    color: #9ae6ff;
}
.bot {
    text-align: left;
    color: #ffffff;
}
.input-bar {
    display: flex;
    gap: 8px;
}
</style>
""", unsafe_allow_html=True)

# ======================
# HEADER
# ======================
st.markdown("## 🧠 **Burak GPT**")
st.caption("Yazı • Araştırma • Görsel")

# ======================
# MODE SELECT (3 DOTS)
# ======================
mode = st.selectbox(
    "⠇",
    ["Sohbet", "Araştırma", "Görsel"],
    label_visibility="collapsed"
)

# ======================
# SESSION
# ======================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ======================
# CHAT HISTORY
# ======================
for role, msg in st.session_state.messages:
    cls = "user" if role == "user" else "bot"
    st.markdown(f"<div class='chat-box {cls}'>{msg}</div>", unsafe_allow_html=True)

# ======================
# INPUT
# ======================
col1, col2 = st.columns([8,1])
with col1:
    user_input = st.text_input(
        "Ne soracaksın?",
        placeholder="İstanbul manzarası, araştırma yap, sohbet edelim...",
        label_visibility="collapsed"
    )
with col2:
    send = st.button("➤")

# ======================
# FUNCTIONS
# ======================
def burak_gpt(prompt, mode):
    system = {
        "Sohbet": "Samimi, zeki, emoji kullanan bir yapay zekasın.",
        "Araştırma": "Maddeli, net, öğretici cevaplar ver."
    }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system.get(mode, "")},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


def generate_image(prompt):
    r = requests.post(
        HF_SPACE + "/predict",
        json={"data":[prompt]},
        timeout=120
    )
    if r.status_code == 200:
        url = r.json()["data"][0]
        img = requests.get(url).content
        return img
    return None

# ======================
# ACTION
# ======================
if send and user_input:
    st.session_state.messages.append(("user", user_input))

    with st.spinner("🧠 Burak GPT düşünüyor..."):
        if mode == "Görsel":
            img_bytes = generate_image(user_input)
            if img_bytes:
                image = Image.open(BytesIO(img_bytes))
                st.image(image, use_container_width=True)
                st.download_button(
                    "⬇ Görseli indir",
                    img_bytes,
                    file_name="burak_gpt.png",
                    mime="image/png"
                )
                st.session_state.messages.append(("bot", "🖼 Görsel hazır."))
            else:
                st.session_state.messages.append(("bot", "❌ Görsel üretilemedi."))
        else:
            reply = burak_gpt(user_input, mode)
            st.session_state.messages.append(("bot", reply))

    st.rerun()
