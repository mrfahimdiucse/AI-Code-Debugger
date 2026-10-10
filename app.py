import streamlit as st
from google import genai
import os
from dotenv import load_dotenv
load_dotenv()
from PIL import Image
from api_calling import note_generator, audio_generator  # audio_generator ইমপোর্ট করা হলো
from gtts import gTTS

api_key = os.environ.get("GEMINI_API_KEY")

# Sidebar Content
with st.sidebar:
    st.header("AI Code Debugger!")
    images = st.file_uploader("Upload the photos of your note", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
    
    # converting pil image
    pil_images = []
    for img in images:
        pil_img = Image.open(img)
        pil_images.append(pil_img)

    if images:
        col = st.columns(len(images))
        for i, img in enumerate(images):
            with col[i]:
                st.image(img)
                
    selected_lang = st.selectbox("Choose Language", ("C", "C++", "Python", "Java"), index=None)
    selected_opt = st.selectbox("Option Bar", ("Hints", "Solution With Code"), index=None)
    clicked = st.button("Debug Code", type="primary")

st.title("⚡ AI Code Inspector Dashboard", anchor=False)
st.divider()

if clicked:
    if len(images) > 3: 
        st.error("Upload At most 3 Images!")
    elif not images:
        st.error("Upload At least 1 image!")
    elif not selected_lang:
        st.error("Please Select language!")
    elif not selected_opt:
        st.error("Please Select an Option!")
    else:
        if images and selected_opt and selected_lang:
            with st.container(border=True):
                # error explanation 
                st.subheader("Error Explanation")
                with st.spinner("AI is working for you..."):
                    response = note_generator(pil_images, selected_lang, selected_opt)
                    st.markdown(response)
            # audio generator container
            with st.container(border=True):
                st.subheader("Audio Explanation")
                with st.spinner("AI is generating audio..."):
                    cleaned_notes = response.replace("#", "").replace("*", "").replace("_", "").replace("'", "")
                    audio_buffer = audio_generator(cleaned_notes)
                    st.audio(audio_buffer, format="audio/mp3")