import os
import zipfile
import pathlib

# 🔍 Zielverzeichnis (z. B. "Songs" innerhalb deines GPTeezy-Projekts)
song_dir = pathlib.Path.cwd() / "Songs"
zip_name = "gpt_output_archive.zip"

# ✅ Suche nach .txt-Dateien im Zielordner
txt_files = list(song_dir.glob("gpt_output_*.txt"))

if not txt_files:
    print("❌ Keine Song-Dateien gefunden im Ordner:", song_dir)
    print("💡 Tipp: Erst einen Song speichern, dann erneut exportieren.")
else:
    with zipfile.ZipFile(zip_name, "w") as zipf:
        for file in txt_files:
            zipf.write(file, arcname=file.name)
    print(f"✅ ZIP-Archiv erstellt: {zip_name} mit {len(txt_files)} Datei(en)")
