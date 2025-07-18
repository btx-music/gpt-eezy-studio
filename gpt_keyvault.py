import os
from dotenv import load_dotenv
from pathlib import Path

ENV_PATH = Path(".env")

def save_key_to_env(api_key):
    with open(ENV_PATH, "w") as f:
        f.write(f"OPENAI_API_KEY={api_key.strip()}")
    print("✅ API Key wurde sicher in .env gespeichert.")

def load_key_from_env():
    load_dotenv(dotenv_path=ENV_PATH)
    return os.getenv("OPENAI_API_KEY")

def delete_key_from_env():
    if ENV_PATH.exists():
        ENV_PATH.unlink()
        print("🗑️ .env-Datei wurde gelöscht (API Key entfernt).")
    else:
        print("⚠️ Keine .env-Datei gefunden.")

def menu():
    print("\n🔐 GPTeezy KeyVault Tool")
    print("==========================")
    print("1. API Key eingeben & speichern")
    print("2. API Key anzeigen")
    print("3. API Key löschen")
    print("4. Beenden")
    print("==========================")

    choice = input("👉 Auswahl: ")

    if choice == "1":
        key = input("🔑 Gib deinen OpenAI API Key ein: ")
        save_key_to_env(key)
    elif choice == "2":
        key = load_key_from_env()
        if key:
            print(f"🔍 Aktueller API Key: {key}")
        else:
            print("⚠️ Kein API Key gefunden.")
    elif choice == "3":
        delete_key_from_env()
    elif choice == "4":
        print("👋 Bis bald, bleib sicher!")
        exit()
    else:
        print("❌ Ungültige Auswahl.")

# Nur ausführen, wenn direkt gestartet
if __name__ == "__main__":
    while True:
        menu()
