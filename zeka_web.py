import streamlit as st
import requests
from openai import OpenAI
from gradio_client import Client
from PIL import Image
from io import BytesIO

# ======================
# PAGE
# ======================
st.set_page_config(
    page_title="Burak GPT",
    page_icon="🧠",
    layout="centered"
)

st.markdown("## 🧠 Burak GPT")
st.caption("Yazı • Araştırma • Görsel")

# ======================
# CLIENTS
# ======================
openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
image_client = Client("burak12321/burak-gpt-image")

# ======================
# SESSION
# ======================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ======================
# AI FUNCTIONS
# ======================
def gpt_response(prompt, mode):
    system_prompt = {
        "Sohbet": "Samimi, zeki, özgüvenli konuş. Az ama etkili emoji kullan 😎🚀",
        "Yazı": "Profesyonel, net, düzgün paragraflar yaz.",
        "Araştırma": "Ciddi, maddeli, öğretici anlat."
    }

    res = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt.get(mode, "")},
            {"role": "user", "content": prompt}
        ]
    )
    return res.choices[0].message.content


def generate_image(prompt):
    try:
        result = image_client.predict(
            prompt=prompt,
            api_name="/generate"
        )

        if isinstance(result, list):
            result = result[0]

        if result and result.get("url"):
            r = requests.get(result["url"], timeout=60)
            img = Image.open(BytesIO(r.content)).convert("RGB")
            return img
    except:
        pass

    return None

# ======================
# UI
# ======================
mode = st.selectbox(
    "Mod",
    ["Sohbet", "Yazı", "Araştırma", "Görsel"]
)

user_input = st.text_input(
    "Mesaj",
    placeholder="Burak GPT’ye yaz…"
)

send = st.button("Gönder")

# ======================
# ACTION
# ======================
if send and user_input:

    st.session_state.messages.append(("Sen", user_input))

    if mode == "Görsel":
        with st.spinner("🎨 Görsel oluşturuluyor..."):
            img = generate_image(user_input)

        if img:
            st.image(img, use_container_width=True)

            buf = BytesIO()
            img.save(buf, format="PNG")

            st.download_button(
                "⬇️ Görseli indir",
                buf.getvalue(),
                "burak-gpt.png",
                "image/png"
            )
        else:
            st.error("❌ Görsel üretilemedi.")

    else:
        with st.spinner("🧠 Burak GPT düşünüyor..."):
            reply = gpt_response(user_input, mode)

        st.session_state.messages.append(("Burak GPT", reply))

# ======================
# CHAT HISTORY
# ======================
st.divider()

for role, msg in st.session_state.messages[-10:]:
    if role == "Sen":
        st.markdown(f"**🧍 {role}:** {msg}")
    else:
        st.markdown(f"**🤖 {role}:** {msg}")
