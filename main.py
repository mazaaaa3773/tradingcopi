import os
import asyncio
from telethon import TelegramClient, events
from deep_translator import GoogleTranslator

# Récupération du BOT TOKEN depuis les variables d'environnement
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID", 0))       # à mettre depuis Telegram
API_HASH = os.getenv("API_HASH", "")       # à mettre depuis Telegram

if not BOT_TOKEN or not API_ID or not API_HASH:
    print("[ERREUR] BOT_TOKEN, API_ID ou API_HASH manquant !")
    exit(1)

# Canal source et canal cible
SOURCE_CHANNEL = "KZTrade08"
TARGET_CHANNEL = "NexusSignelForex"

# Initialisation du client Telethon avec api_id et api_hash (obligatoire)
client = TelegramClient('bot_session', API_ID, API_HASH)

async def translate_text(text: str) -> str:
    """Traduit le texte en français"""
    try:
        return GoogleTranslator(source='auto', target='fr').translate(text)
    except Exception as e:
        print(f"[ERREUR TRADUCTION] {e}")
        return text

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    try:
        original_text = event.message.message or ""
        translated_text = ""
        if original_text:
            translated_text = await asyncio.to_thread(translate_text, original_text)

        # Reposter la photo si présente
        if event.photo:
            await client.send_file(
                TARGET_CHANNEL,
                event.photo,
                caption=translated_text if translated_text else None
            )
            print(f"[PHOTO] Repostée avec légende: {translated_text[:50]}...")
        elif translated_text:
            await client.send_message(TARGET_CHANNEL, translated_text)
            print(f"[TEXTE] Reposté: {translated_text[:50]}...")
    except Exception as e:
        print(f"[ERREUR MESSAGE] {e}")

print("Le bot tourne 24/7 avec BOT TOKEN…")
client.start(bot_token=BOT_TOKEN)  # DÉFINITIF pour les bots
client.run_until_disconnected()
