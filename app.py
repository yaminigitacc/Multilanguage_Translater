
import streamlit as st
import base64
from mtranslate import translate
import pandas as pd 
import os
from gtts import gTTS

df = pd.read_csv("language.csv")

df.dropna(inplace=True)
lang = df['name'].to_list()
langlist = tuple(lang)
langcode = df['iso'].to_list()


# create dict of language and 2letter code for it
lang_array = {lang[i]: langcode[i] for i in range(len(langcode))}

# create a layout

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
st.markdown(
    """
    <style>
    /* Main app background */
    [data-testid="stAppViewContainer"] {
        background-image: url("https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1400&q=80");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Optional: Make sidebar slightly transparent */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.7);
    }

    /* Optional: Make text areas readable with white background */
    .stTextArea textarea {
        background-color: #ffffff;
        color: black;
    }

    /* Optional: Add a bit of rounding and shadow to text boxes */
    .stTextArea textarea, .stTextInput input {
        border-radius: 10px;
        box-shadow: 1px 1px 5px rgba(0,0,0,0.1);
    }

    /* Remove header background */
    [data-testid="stHeader"] {
        background: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

input_text = st.text_area('Hi Please enter a text to translate',height = 100)


choice = st.sidebar.radio('Select Language',langlist)


speech_langs = {
    "af": "Afrikaans",
    "ar": "Arabic",
    "bg": "Bulgarian",
    "bn": "Bengali",
    "bs": "Bosnian",
    "ca": "Catalan",
    "cs": "Czech",
    "cy": "Welsh",
    "da": "Danish",
    "de": "German",
    "el": "Greek",
    "en": "English",
    "eo": "Esperanto",
    "es": "Spanish",
    "et": "Estonian",
    "fi": "Finnish",
    "fr": "French",
    "gu": "Gujarati",
    "od" : "odia",
    "hi": "Hindi",
    "hr": "Croatian",
    "hu": "Hungarian",
    "hy": "Armenian",
    "id": "Indonesian",
    "is": "Icelandic",
    "it": "Italian",
    "ja": "Japanese",
    "jw": "Javanese",
    "km": "Khmer",
    "kn": "Kannada",
    "ko": "Korean",
    "la": "Latin",
    "lv": "Latvian",
    "mk": "Macedonian",
    "ml": "Malayalam",
    "mr": "Marathi",
    "my": "Myanmar (Burmese)",
    "ne": "Nepali",
    "nl": "Dutch",
    "no": "Norwegian",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "si": "Sinhala",
    "sk": "Slovak",
    "sq": "Albanian",
    "sr": "Serbian",
    "su": "Sundanese",
    "sv": "Swedish",
    "sw": "Swahili",
    "ta": "Tamil",
    "te": "Telugu",
    "th": "Thai",
    "tl": "Filipino",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "ur": "Urdu",
    "vi": "Vietnamese",
    "zh-CN": "Chinese"
}



def get_binary_file_downloader_html(bin_file,file_label='File'):
    with open(bin_file,'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'     
    return href


c1,c2 = st.columns([4,3])


# I / O

if len(input_text)>0:
    try:
        output = translate(input_text,lang_array[choice])
        with c1:
            st.text_area('TRANSLATED TEXT',output,height=200)
            
        if choice in speech_langs.values():
            with c2:
                aud_file = gTTS(text = output,lang = lang_array[choice],slow=False)
                aud_file.save("lang.mp3")
                audio_file_read = open('lang.mp3','rb')
                audio_bytes = audio_file_read.read()
                bin_str = base64.b16encode(audio_bytes).decode()
                st.audio(audio_bytes,format = 'audio/mp3')
                st.markdown(get_binary_file_downloader_html('lang.mp3','Audio File'),unsafe_allow_html=True)
                
    except Exception as e:
        st.error(e)
        
