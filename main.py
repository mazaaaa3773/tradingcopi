import os
import sys
import asyncio
from telethon import TelegramClient, events
from deep_translator import GoogleTranslator

# Vérification des variables d'environnement
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

if not api_id or not api_hash:
    print("[ERREUR] API_ID ou API_HASH manquant ! Vérifie tes variables d'environnement.")
    sys.exit(1)

api_id = int(api_id)  # Convertir en entier
api_hash = str(api_hash)

# Canal source et canal cible
SOURCE_CHANNEL = "KZTrade08"
TARGET_CHANNEL = "NexusSignelForex"

client = TelegramClient("session", api_id, api_hash)

async def translate_text(text):
    """Traduit le texte en français"""
    try:
        translated = GoogleTranslator(source='auto', target='fr').translate(text)
        return translated
    except Exception as e:
        print(f"[ERREUR TRADUCTION] {e}")
        return text  # Retourne le texte original en cas d'erreur

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    try:
        # Texte à traduire
        original_text = event.message.message or ""
        translated_text = ""
        if original_text:
            translated_text = await asyncio.to_thread(translate_text, original_text)

        # Si le message contient une photo
        if event.photo:
            await client.send_file(
                TARGET_CHANNEL,
                event.photo,
                caption=translated_text if translated_text else None
            )
            print(f"[PHOTO] Repostée avec légende: {translated_text[:50]}...")
        elif translated_text:
            await client.send_message(
                TARGET_CHANNEL,
                translated_text
            )
            print(f"[TEXTE] Reposté: {translated_text[:50]}...")
    except Exception as e:
        print(f"[ERREUR MESSAGE] {e}")

print("Le bot tourne 24/7…")
client.start()
client.run_until_disconnected()
