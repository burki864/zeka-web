import streamlit as st

st.title("🤖 Benim Yapay Zekam")
st.write("Her gün biraz daha gelişiyorum.")

# Hafıza
if "gecmis" not in st.session_state:
    st.session_state.gecmis = []

mesaj = st.text_input("Sen:")

if mesaj:
    mesaj_kucuk = mesaj.lower()

    if "merhaba" in mesaj_kucuk:
        cevap = "Merhaba! Seni görmek güzel 😄"
    elif "nasılsın" in mesaj_kucuk:
        cevap = "İyiyim. Konuştukça güçleniyorum."
    elif "adın ne" in mesaj_kucuk:
        cevap = "Henüz bir adım yok. İsim koymak ister misin?"
    else:
        cevap = "Bunu henüz bilmiyorum ama aklıma not aldım 🧠"

    st.session_state.gecmis.append(("Sen", mesaj))
    st.session_state.gecmis.append(("AI", cevap))

for kim, yazi in st.session_state.gecmis:
    if kim == "Sen":
        st.write(f"🧑 **Sen:** {yazi}")
    else:
        st.write(f"🤖 **AI:** {yazi}")
