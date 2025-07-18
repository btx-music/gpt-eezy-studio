# ⚡ GPTeezy Studio – Legendary Edition (Mobile Ready)
# All-in-One Streamlit App by B:TX x GPTeezy 💚
# Includes: Songwriter, Voice Prompt Generator, Instrumental Generator, Mood Selector, GPTeezy Chat, Export Tools, Studio Branding Upload

import streamlit as st
import os
import glob
import shutil
import pyperclip
from datetime import datetime
import random
import re
import platform
import zipfile
from dotenv import load_dotenv
import openai
import time
from pathlib import Path

# === API Key Handling ===
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# === Streamlit Setup ===
st.set_page_config(page_title="GPTeezy Studio – Legendary Edition", layout="wide")

# === Responsive Mobile Layout Detection ===
try:
    from streamlit.runtime.scriptrunner import get_script_run_ctx
    ctx = get_script_run_ctx()
    if ctx and hasattr(ctx, "request") and ctx.request:
        user_agent = ctx.request.headers.get("User-Agent", "").lower()
    else:
        user_agent = ""
except:
    user_agent = ""

if any(x in user_agent for x in ["iphone", "android", "mobile"]):
    st.session_state["is_mobile"] = True
else:
    st.session_state["is_mobile"] = False

# === Songwriter Tab – Legendary Update + Style Switcher + Hook-Bar + Adlib Engine + Suno Export Enhancer ===
with st.expander("🎼 Songwriter Tab – Lyrik & Love"):
    st.markdown("**🎤 Voice to Song Generator**")

    voice_input_html = """
    <script>
    function startDictation() {
      if (window.hasOwnProperty('webkitSpeechRecognition')) {
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "en-US";
        recognition.start();

        recognition.onresult = function(e) {
          document.getElementById('voice_input').value = e.results[0][0].transcript;
          recognition.stop();
          document.getElementById('voice_input_form').dispatchEvent(new Event('submit'));
        };

        recognition.onerror = function(e) {
          recognition.stop();
        }
      }
    }
    </script>
    <form id=\"voice_input_form\" method=\"post\">
        <input type=\"text\" id=\"voice_input\" name=\"voice_input\" placeholder=\"🎙️ Say your lyric or hook...\" style=\"width: 80%; padding: 0.5rem; font-size: 1rem;\">
        <button type=\"button\" onclick=\"startDictation()\" style=\"padding: 0.5rem 1rem; font-size: 1rem; background-color: #00f7ff; color: black; border: none; border-radius: 0.8rem;\">🎤 Speak</button>
    </form>
    """
    st.components.v1.html(voice_input_html, height=100)

    voice_input = st.text_input("🎶 Oder gib den Text manuell ein:", value="")

    style_choice = st.selectbox("🎧 Style auswählen", ["RnB Smooth", "Lo-Fi Chill", "Club Anthem", "Cyber Love", "Trap Love"])

    if "editable_adlibs" not in st.session_state:
        st.session_state["editable_adlibs"] = {
            "RnB Smooth": "yeah, uh-huh, oh baby",
            "Lo-Fi Chill": "mmm, ahh, uh",
            "Club Anthem": "let's go, come on, woo!",
            "Cyber Love": "transmit, glitch, mmm",
            "Trap Love": "yeah, uh, skrrt"
        }

    st.markdown("---")
    st.markdown("### 🎯 Hook-Bar™ + Adlibs Preset Editor")

    adlib_edit = st.text_input("✏️ Bearbeite Adlibs (Komma getrennt)", value=st.session_state["editable_adlibs"].get(style_choice, ""))
    if st.button("💾 Adlibs aktualisieren"):
        st.session_state["editable_adlibs"][style_choice] = adlib_edit
        st.success("✅ Adlibs aktualisiert!")

    if "custom_hooks" not in st.session_state:
        st.session_state["custom_hooks"] = []

    new_hook = st.text_input("➕ Eigene Hook speichern")
    if st.button("💾 Hook speichern") and new_hook:
        st.session_state["custom_hooks"].append(new_hook)
        st.success("✅ Hook gespeichert!")

    if st.session_state["custom_hooks"]:
        selected_custom = st.selectbox("📜 Eigene Hooks auswählen", st.session_state["custom_hooks"])
        if st.button("🔁 In Voice Input einsetzen"):
            voice_input = selected_custom
            st.experimental_rerun()

    if st.button("💡 Generate Hook mit GPTeezy"):
        import random
        hook_suggestions = {
            "RnB Smooth": ["Your touch is my spark", "I melt into your rhythm", "Can't breathe without your love"],
            "Lo-Fi Chill": ["Raindrops on my window thoughts", "Sinking in the vinyl haze", "Dreaming past the static"],
            "Club Anthem": ["We own the night, right here", "Drop the love, no filter", "Flash me with your fire"],
            "Cyber Love": ["Signal found – it's you", "Glitch in my heart system", "Upload your kiss to me"],
            "Trap Love": ["Heart on loop, can't escape", "All in with no signal", "I got love encrypted deep"]
        }
        generated = random.choice(hook_suggestions.get(style_choice, ["Love is... you."]))
        st.success(f"🧠 GPTeezy says: {generated}")
        voice_input = generated
        st.experimental_rerun()

    def apply_adlibs(text, adlibs):
        import random
        words = text.split()
        patched = []
        for i, word in enumerate(words):
            patched.append(word)
            if i % 4 == 2 and random.random() > 0.5:
                patched.append(f"({random.choice(adlibs)})")
        return " ".join(patched)

    def generate_song(style, input_text):
        now = datetime.now().strftime("%Y-%m-%d_%H-%M")
        title = f"{style} Vibe {now}"

        raw_adlibs = st.session_state["editable_adlibs"].get(style, "")
        adlib_list = [a.strip() for a in raw_adlibs.split(",") if a.strip()]
        adlibbed = apply_adlibs(input_text, adlib_list)

        return title, f"**🎵 {title}**\n\n[Verse]\n{adlibbed}\n\n[Chorus]\nGenerated chorus based on style.\n[FX: placeholder]"

    st.markdown("---")
    if st.button("✨ Song generieren") and voice_input:
        auto_title, song_text = generate_song(style_choice, voice_input)
        st.session_state["song_title"] = auto_title
        st.session_state["song_text"] = song_text

    if "song_text" in st.session_state:
        st.subheader(f"📄 {st.session_state['song_title']}")
        st.code(st.session_state["song_text"])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button(
                label="📥 Download als .txt",
                data=st.session_state["song_text"],
                file_name=st.session_state["song_title"] + ".txt",
                mime="text/plain"
            )
        with col2:
            if st.button("📋 In Zwischenablage kopieren"):
                pyperclip.copy(st.session_state["song_text"])
                st.success("✅ Songtext kopiert!")
        with col3:
            if st.button("🎧 Suno-kompatibler Prompt anzeigen"):
                suno_prompt = st.session_state["song_text"].replace("**🎵", "").replace("**", "")
                st.text_area("🎵 Suno Prompt:", suno_prompt, height=300)

                st.markdown("---")
                st.markdown("### 🎶 Zusatzinfos für Suno")
                melody_prompt = st.text_input("🎼 Melody Prompt Vorschlag", value=f"Melodic {style_choice} vocal line, emotional phrasing")
                vocal_style = st.selectbox("🎤 Gesangsstil", ["Soft Male", "Emotional Female", "Energetic AI", "Breathy Whisper", "Robotic Funk"])
                bpm = st.slider("⏱️ Tempo (BPM)", 60, 160, 100)
                key = st.selectbox("🎹 Key (Tonart)", ["C Major", "A Minor", "D Minor", "E Major", "G Minor"])

                full_suno_prompt = f"Title: {st.session_state['song_title']}\n\nLyrics:\n{suno_prompt}\n\nMelody Prompt: {melody_prompt}\nVocal Style: {vocal_style}\nTempo: {bpm} BPM\nKey: {key}"

                st.text_area("🧠 Full Suno Prompt", full_suno_prompt, height=400)

# === GOD MODE: Mobile UI Level 4 ===
if st.session_state.get("is_mobile"):
    st.markdown("""
        <style>
            html, body, [class*='css']  { font-size: 16px !important; }
            .block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; }
            button[kind="primary"] { font-size: 1.1rem !important; padding: 0.75rem 1.5rem !important; border-radius: 1.2rem !important; }
            .stTextInput > div > input,
            .stTextArea textarea,
            .stSelectbox div[role='button'] {
                font-size: 1rem !important;
                padding: 0.5rem !important;
            }
            .floating-quick-buttons {
                position: fixed;
                bottom: 1.2rem;
                right: 1.2rem;
                z-index: 100;
                display: flex;
                flex-direction: column;
                gap: 0.75rem;
            }
            .floating-quick-buttons button {
                background-color: #00f7ff;
                color: black;
                font-weight: bold;
                border-radius: 1.2rem;
                border: none;
                padding: 0.6rem 1rem;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            }
            .floating-darkmode {
                position: fixed;
                top: 1.2rem;
                left: 1.2rem;
                z-index: 100;
            }
            .floating-darkmode button {
                background-color: #333;
                color: #eee;
                border-radius: 1.2rem;
                border: none;
                padding: 0.5rem 1rem;
                font-size: 0.9rem;
            }
            .mobile-nav {
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                background: #111;
                color: #fff;
                display: flex;
                justify-content: space-around;
                padding: 0.5rem 0;
                z-index: 999;
            }
            .mobile-nav button {
                background: none;
                border: none;
                color: white;
                font-size: 1rem;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    # Floating Buttons (Scroll)
    st.markdown("""
        <div class="floating-quick-buttons">
            <form action="#" method="get">
                <button onclick="window.scrollTo({top: 0, behavior: 'smooth'})">🔝 Top</button>
            </form>
            <form action="#" method="get">
                <button onclick="window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})">🔚 Bottom</button>
            </form>
        </div>
    """, unsafe_allow_html=True)

    # Floating Dark Mode Toggle
    st.markdown("""
        <div class="floating-darkmode">
            <button onclick="document.body.classList.toggle('dark-mode');">🌓 Dark Mode</button>
        </div>
        <style>
            .dark-mode { background-color: #111 !important; color: #eee !important; }
            .dark-mode input, .dark-mode textarea, .dark-mode select {
                background-color: #222 !important;
                color: #eee !important;
            }
        </style>
    """, unsafe_allow_html=True)

    # Bottom Navigation Bar
    st.markdown("""
        <div class="mobile-nav">
            <button onclick="window.scrollTo({top: 0, behavior: 'smooth'})">🏠 Home</button>
            <button onclick="window.scrollTo({top: 600, behavior: 'smooth'})">🎵 Song</button>
            <button onclick="window.scrollTo({top: 1200, behavior: 'smooth'})">⚙️ Tools</button>
            <button onclick="window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'})">📁 Files</button>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("📱🚀 **Mobile UI: LEVEL 4 aktiviert** – Bottom Nav, Floating Controls, Cosmic Touch UX")
else:
    st.markdown("🖥️ **Desktop UI aktiv** – Vollbild, breite Tabs & große Kontrolle 🎛️")

# === 🎤 Voice Input Integration for Songwriter Tool ===
voice_input = ""
voice_input_html = """
    <script>
    function startDictation() {
      if (window.hasOwnProperty('webkitSpeechRecognition')) {
        var recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "en-US";
        recognition.start();

        recognition.onresult = function(e) {
          document.getElementById('voice_input').value = e.results[0][0].transcript;
          recognition.stop();
          document.getElementById('voice_input_form').dispatchEvent(new Event('submit'));
        };

        recognition.onerror = function(e) {
          recognition.stop();
        }
      }
    }
    </script>
    <form id="voice_input_form" method="post">
        <input type="text" id="voice_input" name="voice_input" placeholder="🎙️ Say your song idea..." style="width: 80%; padding: 0.5rem; font-size: 1rem;">
        <button type="button" onclick="startDictation()" style="padding: 0.5rem 1rem; font-size: 1rem; background-color: #00f7ff; color: black; border: none; border-radius: 0.8rem;">🎤 Speak</button>
    </form>
"""

st.markdown("### 🎙️ Voice-to-Text Input for Songwriter")
st.components.v1.html(voice_input_html, height=100)

voice_input = st.text_input("Oder gib deinen Songtext manuell ein:", value="")

# === Ab hier: Weiterverarbeitung im Songwriter Tool möglich ===
if voice_input:
    st.success("🎶 Songidee empfangen: " + voice_input)
    # → Du kannst den Text hier in ein Feld einsetzen, das dein Songwriting-Modul nutzt

# === Tabs ===
tabs = st.tabs([
    "🎤 Songwriter",
    "🔊 Voice Prompt Generator",
    "🎛️ Instrumental Generator",
    "🧠 AI Mood Selector",
    "💬 GPTeezy Chat",
    "📦 Export Tools"
])

# === Tab 1: Songwriter ===
with tabs[0]:
    st.header("🎤 GPTeezy Songwriter")
    if "song_history" not in st.session_state:
        st.session_state.song_history = []

    song_title = st.text_input("🎶 Songtitel (optional):")
    style = st.selectbox("🎧 Stil wählen", ["Lo-Fi", "Funk", "Soul", "RnB", "Club", "Custom"])
    user_prompt = st.text_area("📝 Dein Prompt:", height=200)

    def format_output(text):
        lines = text.splitlines()
        formatted = []
        for line in lines:
            line = re.sub(r"\\(?(Verse|Chorus|Bridge|Intro|Outro|Pre-Chorus|Drop)\\)?", r"[\\1]", line, flags=re.IGNORECASE)
            line = re.sub(r"\\[(.*?)\\]", r"(\\1)", line)
            formatted.append(line)
        return "\n".join(formatted)

    def generate_song(title, prompt, style):
        if not title:
            title = f"Untitled_{random.randint(1000,9999)}"
        content = f"{title}\n\n[Intro]\n(Ahh yeah)\nLet\u2019s vibe in {style} style...\n\n[Verse]\n{prompt}\n\n[Chorus]\n(feel the beat)\nYou know the vibe..."
        return format_output(content), title

    if st.button("🚀 Song generieren"):
        final_lyrics, used_title = generate_song(song_title, user_prompt, style)
        st.text_area("🎧 Songtext", final_lyrics, height=400)
        st.session_state.song_history.append((used_title, final_lyrics))

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{used_title}_{timestamp}.txt"
        folder = "VoicePrompts"
        os.makedirs(folder, exist_ok=True)
        full_path = os.path.join(folder, filename)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(final_lyrics)
        st.success(f"✅ Song gespeichert unter: {filename}")

        if st.button("📂 Ordner öffnen"):
            path = os.path.abspath(folder)
            if platform.system() == "Windows":
                os.startfile(path)
            elif platform.system() == "Darwin":
                os.system(f"open {path}")
            else:
                os.system(f"xdg-open {path}")

    if st.checkbox("📜 Show Song History"):
        for title, text in st.session_state.song_history[::-1]:
            st.markdown(f"**{title}**")
            st.code(text)

# === Tab 2: Voice Prompt Generator ===
with tabs[1]:
    st.header("🔊 GPTeezy Voice Prompt Generator")

    def get_voice_prompt(style):
        prompts = {
            "dreamy": "Soft male AI voice, slight glitch effect, digital warmth, whispery tone, emotional inflections",
            "funky": "Energetic funky male voice, talkbox-inspired, retro-futuristic flair",
            "clubby": "Deep robotic voice, heavy reverb and delay, confident",
            "emotional": "Cracked emotional tone, breathy delivery, intimate",
            "cyber": "Synthetic glitchy voice, metallic layer, vocoder FX"
        }
        return prompts.get(style, "Natural AI voice with standard tone and clarity.")

    style = st.selectbox("🎻 Wähle deinen Style", ["dreamy", "funky", "clubby", "emotional", "cyber"])

    with st.expander("🔧 Prompt Builder Tool"):
        voice_type = st.selectbox("👤 Stimme", ["Soft male", "Energetic male", "Deep robotic", "Breathy female", "Glitchy AI"])
        tone = st.selectbox("🎙️ Tonlage", ["Whispery", "Playful", "Confident", "Emotional", "Metallic"])
        fx = st.multiselect("🎛️ Effekte", ["Reverb", "Delay", "Glitch", "Compression", "Vocoder", "Distortion"])
        application = st.text_input("🧠 Einsatzzweck", placeholder="z.B. für Love Songs, Clubtracks...")

        builder_notes = f"{voice_type} voice, {tone.lower()} tone"
        if fx:
            builder_notes += f", with {' and '.join(fx)} effects"
        if application:
            builder_notes += f" – suitable for {application}"

        st.code(builder_notes)

        if st.button("🧩 Zusatz übernehmen"):
            st.session_state["custom_note"] = st.session_state.get("custom_note", "") + "\n" + builder_notes

    if "custom_note" not in st.session_state:
        st.session_state["custom_note"] = ""

    custom_note = st.text_area("📝 Zusatz (optional)", value=st.session_state["custom_note"])

    if st.button("🎤 Prompt generieren"):
        base_prompt = get_voice_prompt(style)
        if custom_note:
            base_prompt += f" Additional notes: {custom_note}"

        st.code(base_prompt)
        filename = f"voice_prompt_{style}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        folder = "VoicePrompts"
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(base_prompt)
        st.success(f"✅ Prompt gespeichert: {filename}")
        pyperclip.copy(base_prompt)
        st.download_button("📥 Download", data=base_prompt, file_name=filename)

# === Tab 3: Instrumental Generator ===
with tabs[2]:
    st.header("🎛️ GPTeezy Instrumental Generator")

    genre = st.selectbox("🎼 Genre", ["Lo-Fi", "Funk", "Deep House", "Trap", "Ambient", "Cyber Pop"])
    mood = st.selectbox("🎭 Stimmung", ["Chill Sunset Vibes", "Sexy Late Night", "Digital Dreamscape", "Retro Groove", "Dark Energy", "Uplifting Spark"])
    bpm = st.slider("🕺 Tempo (BPM)", 60, 160, 100)
    key = st.selectbox("🎹 Tonart", ["C", "D", "E", "F", "G", "A", "B"])
    scale = st.selectbox("🔑 Skala", ["Major", "Minor"])
    structure = st.multiselect("📐 Struktur", ["Intro", "Verse", "Chorus", "Bridge", "Drop", "Outro"], default=["Intro", "Verse", "Chorus", "Outro"])

    if st.button("🎵 Prompt generieren"):
        prompt = (
            f"Create a {genre.lower()} instrumental with {mood.lower()} vibe. "
            f"Use a tempo of {bpm} BPM in the key of {key} {scale}. "
            f"The track should include the following sections: {', '.join(structure)}. "
            f"Emphasize atmosphere, emotion, and rhythmic flow. No vocals. Pure instrumental."
        )
        st.code(prompt)
        filename = f"instrumental_prompt_{genre}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        folder = "VoicePrompts"
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(prompt)
        pyperclip.copy(prompt)
        st.success(f"✅ Prompt gespeichert unter: {filename}")
        st.download_button("📥 Prompt herunterladen", data=prompt, file_name=filename)

# === Tab 4: AI Mood Selector ===
with tabs[3]:
    st.header("🧠 AI Mood Selector")
    mood_options = {
        "💖 Romantic Bliss": {"lyric_hint": "Soft, sensual, heartfelt", "voice": "dreamy", "bpm": 95, "key": "A Minor"},
        "🔥 Club Heat": {"lyric_hint": "Bold, confident, dirty", "voice": "clubby", "bpm": 124, "key": "F Minor"},
        "🌙 Late Night Vibes": {"lyric_hint": "Moody, chill, introspective", "voice": "emotional", "bpm": 85, "key": "D Minor"},
        "🚀 Cyber Drive": {"lyric_hint": "Futuristic, fast-paced, sharp", "voice": "cyber", "bpm": 140, "key": "E Minor"},
        "🌞 Uplift & Shine": {"lyric_hint": "Positive, catchy, playful", "voice": "funky", "bpm": 110, "key": "C Major"}
    }
    selected_mood = st.selectbox("✨ Wähle deine Stimmung", list(mood_options.keys()))
    if selected_mood:
        mood = mood_options[selected_mood]
        st.markdown(f"**🎧 Voice Style:** `{mood['voice']}`\n\n**📝 Lyric-Hint:** *{mood['lyric_hint']}*\n\n**🎚️ BPM:** {mood['bpm']}\n\n**🎹 Key:** {mood['key']}")
        if st.button("💾 Stimmung übernehmen"):
            st.session_state["selected_mood"] = selected_mood
            st.session_state["voice"] = mood["voice"]
            st.session_state["bpm"] = mood["bpm"]
            st.session_state["key"] = mood["key"]
            st.session_state["lyric_hint"] = mood["lyric_hint"]
            st.success(f"✅ Stimmung '{selected_mood}' aktiviert!")

# === Tab 5: GPTeezy Chat Modus ===
with tabs[4]:
    st.header("💬 GPTeezy Chat")
    if not openai_api_key:
        st.error("❌ Kein API Key gefunden. Bitte mit gpt_keyvault.py setzen.")
    else:
        openai.api_key = openai_api_key
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        user_input = st.text_input("💬 Nachricht an GPTeezy", placeholder="z. B. 'Gib mir eine funky Hook'")
        if st.button("📨 Senden") and user_input:
            context = f"""
            Du bist GPTeezy, ein musikalischer KI-Coach.
            Stimmung: {st.session_state.get("selected_mood", "keine")}
            Voice Style: {st.session_state.get("voice", "unbekannt")}
            BPM: {st.session_state.get("bpm", "n/a")}
            Key: {st.session_state.get("key", "n/a")}
            Lyric-Vibe: {st.session_state.get("lyric_hint", "n/a")}
            Antworte locker, kreativ & musikalisch – mit Hooks, Reimen, Ideen.
            """
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": context},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.9,
                    max_tokens=400
                )
                reply = response.choices[0].message["content"]
                st.session_state.chat_history.append(("🧑", user_input))
                st.session_state.chat_history.append(("🤖", reply))
            except Exception as e:
                st.error(f"Fehler: {e}")

        for role, message in st.session_state.chat_history:
            with st.chat_message("user" if role == "🧑" else "assistant"):
                st.markdown(message)

# ⚡ GPTeezy Studio – Legendary Edition
# All-in-One Streamlit App by B:TX x GPTeezy 💚
# Includes: Songwriter, Voice Prompt Generator, Instrumental Generator, Mood Selector, GPTeezy Chat, Export Tools

import streamlit as st
import os
import glob
import shutil
import pyperclip
from datetime import datetime
import random
import re
import platform
import zipfile
from dotenv import load_dotenv
import openai
import time
from pathlib import Path

# === API Key Handling ===
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# === Streamlit Setup ===
st.set_page_config(page_title="GPTeezy Studio – Legendary Edition", layout="wide")

# === Branding Header ===
with st.container():
    st.markdown("""
    <h1 style='text-align: center; font-size: 45px; color: #00f7ff; margin-bottom: 0;'>
        ⚡ GPTeezy Studio – Legendary Edition ⚡
    </h1>
    <p style='text-align: center; font-size: 18px; color: #bbb; margin-top: 0;'>
        powered by B:TX | AI Artistry Mode ∞
    </p>
    """, unsafe_allow_html=True)

# === Tabs ===
tabs = st.tabs([
    "🎤 Songwriter",
    "🔊 Voice Prompt Generator",
    "🎛️ Instrumental Generator",
    "🧠 AI Mood Selector",
    "💬 GPTeezy Chat",
    "📦 Export Tools"
])

# === Tab 6: Export Tools ===
with tabs[5]:
    st.header("📦 Export Tools")
    st.markdown("Exportiere all deine Songs, Voice Prompts und Instrumentals als ZIP-Datei für Archiv, Weitergabe oder Contest-Submission.")

    base_folder = "VoicePrompts"
    file_types = [".txt"]

    all_files = [f for f in glob.glob(os.path.join(base_folder, "*")) if os.path.splitext(f)[1] in file_types]

    if not all_files:
        st.info("Keine Dateien zum Exportieren gefunden im Ordner 'VoicePrompts'.")
    else:
        selected = st.multiselect("🗂️ Wähle Dateien zum Export", all_files, default=all_files)

        if selected:
            zip_name = f"gpt_export_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.zip"
            zip_path = os.path.join(base_folder, zip_name)

            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file in selected:
                    zipf.write(file, os.path.basename(file))

            with open(zip_path, "rb") as f:
                st.download_button("📥 Download ZIP", data=f.read(), file_name=zip_name, mime="application/zip")

            st.success(f"✅ Export ZIP erstellt: {zip_name}")
