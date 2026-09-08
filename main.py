import asyncio
import os
import discord
from discord.ext import commands
from config.settings import settings


class SoccordBot(commands.Bot):
    def __init__(self):
        # standardmäßige Intents aktivieren
        intents = discord.Intents.default()
        intents.message_content = True  # Erforderlich für Textinteraktionen / Commands

        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        """Wird aufgerufen, bevor der Bot sich mit Discord verbindet.
        Lädt dynamisch alle Plugins aus dem plugins/-Ordner.
        """
        print("[*] Lade Plugins...")
        
        # Gehe durch den Ordner 'plugins' und lade alle Python-Dateien
        plugins_dir = os.path.join(os.path.dirname(__file__), "plugins")
        
        if os.path.exists(plugins_dir):
            for filename in os.listdir(plugins_dir):
                if filename.endswith(".py") and not filename.startswith("__"):
                    plugin_name = f"plugins.{filename[:-3]}"
                    try:
                        await self.load_extension(plugin_name)
                        print(f"  [+] Plugin geladen: {plugin_name}")
                    except Exception as e:
                        print(f"  [!] Fehler beim Laden von {plugin_name}: {e}")
        else:
            print("[!] Warnung: Ordner 'plugins/' wurde nicht gefunden.")

    async def on_ready(self):
        print(f"\n[✓] Bot erfolgreich eingeloggt als {self.user} (ID: {self.user.id})")
        print("[*] Soccord Security Monitor ist aktiv.\n")


async def main():
    # Validierung des Bot-Tokens
    if not settings.DISCORD_TOKEN:
        print("[!] KRITISCHER FEHLER: DISCORD_TOKEN fehlt in den Einstellungen / .env Datei!")
        return

    bot = SoccordBot()
    
    async with bot:
        await bot.start(settings.DISCORD_TOKEN)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[*] Bot wurde vom Benutzer beendet.")