import os

# Aktuelles Verzeichnis
base_dir = os.path.dirname(os.path.abspath(__file__))

# Name der Datei, die behalten werden soll
keep_file = "gpt_streamlit_template_ready.py"

# Alle .py-Dateien im Verzeichnis
files = [f for f in os.listdir(base_dir) if f.startswith("gpt_streamlit") and f.endswith(".py")]

deleted_files = []

for file in files:
    if file != keep_file:
        file_path = os.path.join(base_dir, file)
        os.remove(file_path)
        deleted_files.append(file)

if deleted_files:
    print("🧹 Folgende Dateien wurden entfernt:")
    for f in deleted_files:
        print(f"   - {f}")
else:
    print("✅ Alles ist schon clean! Keine überflüssigen Files gefunden.")
