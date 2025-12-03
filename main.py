from telethon import TelegramClient, events
from googletrans import Translator
import os

# Récupérer les identifiants depuis Railway (variables d'environnement)
api_id = int(os.getenv("37953717"))
api_hash = os.getenv("3795420c49e410851262efb2d859585e")

# Canal source (public)
SOURCE_CHANNEL = "KZTrade08"

# Canal cible (ton canal)
TARGET_CHANNEL = "NexusSignelForex"

client = TelegramClient("session", api_id, api_hash)
translator = Translator()

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    # Traduire le texte si présent
    translated_text = ""
    if event.message.message:
        translated = translator.translate(event.message.message, dest='fr')
        translated_text = translated.text

    # Reposter l'image brute si présente
    if event.photo:
        await client.send_file(
            TARGET_CHANNEL,
            event.photo,
            caption=translated_text if translated_text else None
        )
    else:
        # Texte seul
        await client.send_message(
            TARGET_CHANNEL,
            translated_text
        )

print("Le bot tourne 24/7…")
client.start()
client.run_until_disconnected()
