# AI Reimagine Storytelling with Innovation
import os
import requests
import streamlit as st
from fpdf import FPDF
import pyttsx3
from ollama import Client
import re
import qrcode
import io
import tempfile
import speech_recognition as sr
from pydub import AudioSegment

# --- SETUP ---
OLLAMA_HOST = 'http://localhost:11434'
client = Client(host=OLLAMA_HOST)
DEEP_AI_API_URL = "https://api.deepai.org/api/text2img"
DEEP_AI_KEY = st.secrets["api"]["deepai_key"]

# --- SESSION STATE INIT ---
if "story_generated" not in st.session_state:
    st.session_state.story_generated = False
    st.session_state.story_title = ""
    st.session_state.full_story = ""
    st.session_state.scenes = []
    st.session_state.audio_path = ""
    st.session_state.character = "A robot who loves flowers"
    st.session_state.genre = "Fantasy"
    st.session_state.theme = "Friendship"
    st.session_state.style = "Cartoon"
    st.session_state.last_manual = {
        "Character": "A robot who loves flowers",
        "Genre": "Fantasy",
        "Theme": "Friendship",
        "Illustration Style": "Cartoon"
    }
    st.session_state.voice_target_field = "Character"
    st.session_state.voice_applied = False

# --- IMAGE GENERATION ---
def generate_image_deepai(prompt: str) -> str:
    headers = {"api-key": DEEP_AI_KEY}
    data = {"text": prompt}
    try:
        response = requests.post(DEEP_AI_API_URL, data=data, headers=headers)
        response.raise_for_status()
        output_url = response.json().get("output_url")
        if output_url:
            img_data = requests.get(output_url).content
            path = f"img_{hash(prompt)}.png"
            with open(path, "wb") as f:
                f.write(img_data)
            return path
    except Exception as e:
        st.warning(f"⚠️ Image skipped: {e}")
        return None

# --- AUDIO GENERATION ---
def generate_tts(text: str, filename: str, lang='en', speed='Normal'):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    if speed.lower() == 'slow':
        engine.setProperty('rate', rate - 50)
    elif speed.lower() == 'fast':
        engine.setProperty('rate', rate + 50)
    engine.save_to_file(text, filename)
    engine.runAndWait()
    return filename

# --- PDF EXPORT ---
def export_to_pdf(title: str, scenes: list, filename: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    try:
        pdf.add_font('DejaVu', '', 'DejaVuSans.ttf')
        pdf.set_font("DejaVu", size=14)
    except:
        pdf.set_font("Arial", size=14)
    pdf.multi_cell(0, 10, title + "\n")
    for scene in scenes:
        try:
            for line in scene.split('\n'):
                pdf.multi_cell(0, 10, line)
            pdf.ln()
        except Exception as e:
            print(f"⚠️ Skipped a scene in PDF: {e}")
    pdf.output(filename)
    return filename

# --- QR Code Generation ---
def generate_qr_code(data):
    qr = qrcode.make(data)
    buf = io.BytesIO()
    qr.save(buf)
    return buf

# --- THEME & BACKGROUND ---
background_url = "https://images.unsplash.com/photo-1519125323398-675f0ddb6308"
theme_mode = st.sidebar.radio("🌗 Theme Mode", ["Light", "Dark"])

if theme_mode == "Dark":
    st.markdown(f"""
        <style>
        html, body, .stApp {{
            background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)),
                        url('{background_url}') no-repeat center center fixed;
            background-size: cover;
            color: #FAFAFA;
        }}
        label,
        [data-testid="stCheckbox"] label,
        .stTextInput > label,
        .stSelectbox > label,
        .stSlider > label,
        .stCheckbox > div > label,
        .stCheckbox label,
        div[data-testid="stCheckbox"] > div label,
        .stButton > button,
        .stDownloadButton > button,
        .stCheckbox span {{
            color: #FAFAFA !important;
            font-weight: bold;
            text-shadow: 1px 1px 2px black;
        }}
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
        <style>
        html, body, .stApp {{
            background: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)),
                        url('{background_url}') no-repeat center center fixed;
            background-size: cover;
            color: #000000;
        }}
        label,
        .stTextInput > label,
        .stSelectbox > label,
        .stSlider > label,
        [data-testid="stCheckbox"] label,
        .stCheckbox span {{
            color: #000000 !important;
            font-weight: 600 !important;
            font-size: 16px !important;
            text-shadow: 1px 1px 1px #ffffff !important;
        }}
        </style>
    """, unsafe_allow_html=True)

# --- APP TITLE ---
st.title("📚 AI Reimagine Storytelling App")
st.markdown("### ✨ Create beautiful stories with live narration, illustrations, PDF, and QR sharing")

# --- SPEECH INPUT SECTION ---
with st.expander("🎙️ Record & Assign Speech Input"):
    field_target = st.selectbox("📌 Choose where to apply speech input:", ["Character", "Genre", "Theme", "Illustration Style"], key="target_select")
    if st.button("🎤 Start Recording"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("🎧 Listening (up to 10 seconds)...")
            audio = recognizer.listen(source, phrase_time_limit=10)
            try:
                spoken_text = recognizer.recognize_google(audio)
                st.session_state[field_target.lower()] = spoken_text
                st.session_state.voice_applied = True
                st.success(f"✅ Applied to *{field_target}*: `{spoken_text}`")
            except:
                st.error("❌ Could not recognize speech. Try again.")

    if st.session_state.voice_applied:
        if st.button("🔄 Undo Last Voice Input"):
            st.session_state[field_target.lower()] = st.session_state.last_manual[field_target]
            st.session_state.voice_applied = False
            st.success(f"↩️ Restored previous value for {field_target}.")

# --- TEXT FIELDS ---
character = st.text_input("Character Description", st.session_state.get("character", "A robot who loves flowers"))
genre = st.text_input("🎭 Enter your own Genre (e.g., Fantasy, Sci-Fi, Mystery, Adventure, Comedy)", st.session_state.get("genre", "Fantasy"))
theme = st.text_input("❤️ Enter your own Theme (e.g., Friendship, Curiosity, Courage, Love, Growth)", st.session_state.get("theme", "Friendship"))
style = st.text_input("🖌️ Enter Illustration Style (e.g., Cartoon, Watercolor, Pixel Art, Realistic, Paper Cutout)", st.session_state.get("style", "Cartoon"))

image_file = st.file_uploader("Upload character image (optional)", type=["jpg", "jpeg", "png"])
if image_file:
    st.image(image_file, caption="Uploaded Character", use_container_width=True)
    
language = st.sidebar.selectbox("🌐 Language", [
    ("English 🇬🇧", "en"),
    ("Chinese 🇨🇳", "zh-cn"),
    ("Japanese 🇯🇵", "ja"),
    ("Malay 🇲🇾", "ms"),
    ("Hindi 🇮🇳", "hi"),
    ("Urdu 🇵🇰", "ur"),
    ("Bengali 🇧🇩", "bn"),
    ("Arabic 🇸🇦", "ar"),
    ("German 🇩🇪", "de"),
    ("Spanish 🇪🇸", "es")
])
lang_code = language[1]
lang_name = language[0].split()[0]
voice_speed = st.sidebar.radio("🎵 Voice Speed", ["Normal", "Slow", "Fast"], index=0)
num_scenes = st.slider("🎬 Number of Scenes", min_value=2, max_value=9, value=4)
include_images = st.checkbox("🖼️ Generate Illustrations", value=False)

missing_inputs = []
if not character:
    missing_inputs.append("Character Description")
if not genre:
    missing_inputs.append("Genre")
if not theme:
    missing_inputs.append("Theme")
if not lang_code:
    missing_inputs.append("Language")
if not voice_speed:
    missing_inputs.append("Voice Speed")

story_trigger = st.button("🚀 Generate Story")
story_stop = st.button("🛑 Stop")

if story_trigger and not story_stop:
    if missing_inputs:
        st.warning(f"⚠️ Please fill in the following required fields: {', '.join(missing_inputs)}")
        st.stop()

    st.success("✅ Starting story generation...")
    with st.spinner("✨ Creating story..."):
        try:
            title_prompt = f"Give a creative and short title for a children's {genre} story about {character} with the theme of {theme}."
            title_response = client.chat(
                model="mistral",
                messages=[{"role": "user", "content": title_prompt}]
            )
            story_title = title_response['message']['content'].strip().replace('"', '')
        except:
            story_title = f"{theme} and {character}"

        story_prompt = f"""
        Write exactly {num_scenes} numbered scenes for a children's {genre} story in {lang_name} language.
        The story should feature the character: {character} and reflect the theme: {theme}.
        Each scene should begin with 'Scene {{n}}:' and be no longer than 4–5 sentences.
        Do not include a title or a moral at the end.
        """
        if image_file:
            story_prompt += " The character visually resembles the uploaded image."

        try:
            response = client.chat(
                model="mistral",
                messages=[{"role": "user", "content": story_prompt}]
            )
            full_story = response['message']['content']
        except Exception as e:
            st.error(f"❌ Failed to generate story: {e}")
            full_story = ""

    scenes = re.split(r"\n(?=Scene \d+:)", full_story)
    scenes = scenes[:num_scenes]

    if scenes:
        st.success("✅ Story Generated!")
        st.markdown(f"## 📝 *{story_title}*")

        progress_bar = st.progress(0)
        for i, scene in enumerate(scenes):
            progress_bar.progress((i + 1) / len(scenes))
            scene_clean = scene.strip()
            if not scene_clean.lower().startswith("scene"):
                st.markdown(f"**Scene {i+1}:** {scene_clean}")
            else:
                st.markdown(f"### {scene_clean.split(':')[0]}: {scene_clean.split(':',1)[1].strip()}")

            if include_images:
                with st.spinner(f"🎨 Creating image for Scene {i+1}..."):
                    short_prompt = scene_clean.split(".")[0][:100]
                    img_path = generate_image_deepai(f"{style} style illustration of {short_prompt}")
                    if img_path:
                        st.image(img_path, caption=f"Scene {i+1}", use_container_width=True)

            st.markdown("---")

        with st.spinner("🔊 Creating audio preview..."):
            tts_path = f"audio_{hash(full_story)}.mp3"
            generate_tts(f"{story_title}. {full_story}", tts_path, lang=lang_code, speed=voice_speed)
            st.audio(open(tts_path, 'rb').read(), format='audio/mp3')

        with st.spinner("📄 Exporting PDF..."):
            pdf_path = export_to_pdf(story_title, scenes, f"story_{hash(full_story)}.pdf")
            with open(pdf_path, "rb") as f:
                st.download_button("📥 Download PDF", f, file_name="your_story.pdf")

        st.markdown("### 📲 Share this story")
        qr_buf = generate_qr_code("https://drive.google.com/file/d/1PJzW2J4gq4yNr3hHDr-49wDomD_z0FCU/view?usp=drive_link")
        st.image(qr_buf.getvalue(), caption="📱 Scan this QR code to share")
