"""Streamlit demo application."""

import streamlit as st

from src.inference import predict

st.set_page_config(page_title="Lyric Emotion Timeline", page_icon="🎵")
st.title("Lyric Emotion Timeline")
st.write("Поставете текст, за да получите прогнозирани емоции.")

lyrics = st.text_area("Текст на песента", height=220)
model_name = st.text_input("Модел", value="xlm-roberta-base")

if st.button("Анализирай"):
    if not lyrics.strip():
        st.warning("Моля, въведете текст.")
    else:
        with st.spinner("Анализирам..."):
            st.json(predict(lyrics, model_name))
