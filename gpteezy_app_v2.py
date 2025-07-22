# 🚀 GPTeezy Studio v2.0 – All-in-One Legendary Edition (Mobile Ready)
# Includes: Songwriter, Voice Prompt Generator, Instrumental Generator, Mood Selector,
# GPTeezy Chat, Export Tools, Preset Manager, Style Switcher, Voice Input (EN/DE)

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
import json

# === API Key Handling ===
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# === Streamlit Setup ===
st.set_page_config(page_title="GPTeezy Studio – Legendary Edition", layout="wide")

# === Tabs ===
tabs = st.tabs([
    "🎤 Songwriter",
    "🔊 Voice Prompt Generator",
    "🎛️ Instrumental Generator",
    "🧠 AI Mood Selector",
    "💬 GPTeezy Chat",
    "📦 Export Tools"
])

# === Preset + Style Defaults Setup (global) ===
PRESET_FOLDER = "presets/lyrics"
os.makedirs(PRESET_FOLDER, exist_ok=True)

style_defaults = {
    "Lo-Fi": {"bpm": 80, "key": "C Minor", "mood": "Chill, nostalgic, smooth"},
    "Funk": {"bpm": 105, "key": "E Minor", "mood": "Groovy, upbeat, retro vibes"},
    "Soul": {"bpm": 95, "key": "A Minor", "mood": "Emotional, warm, classic"},
    "RnB": {"bpm": 90, "key": "D Minor", "mood": "Smooth, sexy, heartfelt"},
    "Club": {"bpm": 120, "key": "F Minor", "mood": "Energetic, danceable, confident"},
    "Custom": {"bpm": 100, "key": "C Major", "mood": "Feel free to define your vibe"}
}

st.success("✅ GPTeezy Studio v2.0 vollständig fusioniert – bereit für den finalen Export!")
