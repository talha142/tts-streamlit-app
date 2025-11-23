# app.py
import streamlit as st
from synthesize import synthesize_with_coqui
import os
from io import BytesIO

st.set_page_config(page_title="Open TTS Streamlit", layout="centered")

st.title("Open-source Long-form Text → Speech (Coqui/OpenTTS)")
st.markdown("Paste text, choose voice/model, and click *Synthesize*. For 15–20 minutes audio, large texts will be chunked and concatenated automatically.")

text = st.text_area("Input text (you can paste long text, e.g., 15–20 min of narration):", height=300)
model_name = st.text_input("Coqui model name (leave blank for default)", value="")
if st.button("Synthesize"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Synthesizing (may take time on first run; model will download)..."):
            out_wav = "final_output.wav"
            try:
                path = synthesize_with_coqui(text, model_name=model_name or None, out_path=out_wav)
                st.success("Done — audio ready.")
                # play audio
                audio_bytes = open(path, "rb").read()
                st.audio(audio_bytes, format="audio/wav")
                st.download_button("Download WAV", data=audio_bytes, file_name="tts_output.wav", mime="audio/wav")
            except Exception as e:
                st.error(f"Synthesis failed: {e}")
                st.exception(e)
