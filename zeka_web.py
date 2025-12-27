import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Benim Yapay Zekam", page_icon="🤖")
st.title("🤖 Benim Yapay Zekam")
st.write("Her gün biraz daha gelişiyorum.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"🧑 **Sen:** {msg['content']}")
    else:
        st.markdown(f"🤖 **AI:** {msg['content']}")

user_input = st.text_input("Sen:")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )

    ai_reply = response.choices[0].message.content

    st.session_state.messages.append(
        {"role": "assistant", "content": ai_reply}
    )

    st.rerun()

