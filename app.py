
import streamlit as st
import base64

st.set_page_config(page_title="AI Voiceover Translator", layout="centered")
st.title("🌍 AI Translation App with Voiceover")

# Load and encode voiceover.mp3
audio_file = "voiceover.mp3"
with open(audio_file, "rb") as f:
    b64 = base64.b64encode(f.read()).decode()

# HTML + JS Autoplay workaround
st.markdown(
    f'''
    <audio id="bg-audio" autoplay hidden>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    <script>
    document.addEventListener("DOMContentLoaded", function() {{
        const audio = document.getElementById("bg-audio");
        setTimeout(() => {{
            var clickEvent = new MouseEvent("click", {{
                view: window,
                bubbles: true,
                cancelable: true
            }});
            document.body.dispatchEvent(clickEvent);
            audio.play().catch(e => console.log("Autoplay blocked", e));
        }}, 1000);
    }});
    </script>
    ''',
    unsafe_allow_html=True
)

st.markdown("Enter text below and experience AI-powered translation with voice narration!")
text = st.text_area("Enter English Text")
lang = st.selectbox("Choose Language", ["Hindi", "Spanish", "Japanese"])
if st.button("Translate"):
    st.success(f"✅ Translated to {lang} (simulation only).")
