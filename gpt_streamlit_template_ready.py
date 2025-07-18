from openai import OpenAI
import os
import json
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime
import pathlib

# 🔐 Lade API-Key + Project-ID aus .env
load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    project=os.getenv("OPENAI_PROJECT_ID")
)

# 🎭 Mood → Emojis
def mood_to_emojis(mood):
    emoji_map = {
        "romantic": "💞🎶🌹",
        "dreamy": "🌙✨🫧",
        "clubby": "🪩🔥🎧",
        "emotional": "💔🕯️🎤",
        "funky": "🕺🎷💃",
        "cyber": "🤖💻⚡"
    }
    return emoji_map.get(mood, "🎵")

# ✨ GPTeezy Core Generator
def gpteezy_generate(topic, language, mood, include_suno, include_leonardo, emojis_enabled):
    lang_instruction = {
        "en": "Write everything in English.",
        "de": "Schreibe alles auf Deutsch."
    }
    lang_tag = lang_instruction.get(language, "Write everything in English.")
    emojis = mood_to_emojis(mood) if emojis_enabled else ""

    prompt = f"""
You are GPTeezy, a {mood} music AI artist. {lang_tag}
Your job is to write:
1. A full song text with a chorus and adlibs (e.g. [Oh baby], [Whisper: come closer]) about: "{topic}"
2. An Instagram caption for the release post – short, poetic, and engaging – with mood: "{mood}" and emojis: {emojis}
"""
    if include_leonardo:
        prompt += f"""
3. A Leonardo AI prompt to create the cover art – mood: {mood}, cinematic style
"""
    if include_suno:
        prompt += f"""
4. A matching Suno prompt with genre, tempo, mood and vocal style
"""
    prompt += "\n\nOutput format:\n### SONG TEXT\n...\n\n### INSTAGRAM CAPTION\n..."
    if include_leonardo:
        prompt += "\n\n### LEONARDO PROMPT\n..."
    if include_suno:
        prompt += "\n\n### SUNO PROMPT\n..."

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9
    )
    return response.choices[0].message.content

# 💾 Save-to-File Funktion
def save_to_file(content, topic, directory="."):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"gpt_output_{topic.replace(' ', '_')}_{timestamp}.txt"
    full_path = os.path.join(directory, filename)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    return full_path

# 🌐 Streamlit GUI
st.title("🎤 GPTeezy AI Songwriter Studio – Project Key Edition")

# Nutze Session State für persistente Ergebnisse
if "output" not in st.session_state:
    st.session_state.output = None

topic = st.text_input("🎧 Thema für den Song", placeholder="z.B. Neonliebe im Cyberspace")
language = st.selectbox("🌍 Sprache wählen", ["en", "de"])
mood = st.selectbox("🎛️ Musikstil/Mood", ["romantic", "dreamy", "clubby", "emotional", "funky", "cyber"])
emojis_enabled = st.checkbox("🎉 Emojis in der Caption einfügen", value=True)
include_leonardo = st.checkbox("🎨 Leonardo Prompt erstellen", value=True)
include_suno = st.checkbox("🎵 Suno Prompt erstellen", value=True)

if st.button("🚀 Generate with GPTeezy"):
    if topic.strip() == "":
        st.warning("Bitte gib ein Thema ein.")
    else:
        result = gpteezy_generate(topic, language, mood, include_suno, include_leonardo, emojis_enabled)
        st.session_state.output = result
        st.success("✅ GPTeezy Output erstellt!")

# 📃 Ergebnis anzeigen
if st.session_state.output:
    st.text_area("🎤 Ergebnis", value=st.session_state.output, height=500)

    st.markdown("---")
    st.subheader("📁 Speicherort wählen (optional)")
    default_path = str(pathlib.Path.cwd())
    save_path = st.text_input("📍 Zielordner (absoluter Pfad)", value=default_path)

    if st.button("💾 Speichern"):
        try:
            file_path = save_to_file(st.session_state.output, topic, save_path)
            abs_path = os.path.abspath(file_path)
            st.success("✅ Datei erfolgreich gespeichert!")
            st.markdown(f"📂 **Pfad zur Datei:** `{file_path}`")
            st.markdown(f"[📄 Öffnen im Explorer](file:///{abs_path.replace(os.sep, '/')})")
        except Exception as e:
            st.error(f"❌ Fehler beim Speichern: {e}")
