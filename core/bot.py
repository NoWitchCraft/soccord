import os
import discord
from discord.ext import commands

class SOCBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        """Asynchronously loads all plugins from the /plugins directory upon startup."""
        plugins_dir = "./plugins"
        if not os.path.exists(plugins_dir):
            os.makedirs(plugins_dir)
            return

        for filename in os.listdir(plugins_dir):
            if filename.endswith(".py") and not filename.startswith("__"):
                ext = f"plugins.{filename[:-3]}"
                try:
                    await self.load_extension(ext)
                    print(f"[+] Loaded plugin: {ext}")
                except Exception as e:
                    print(f"[!] Failed to load plugin {ext}: {e}")

    async def on_ready(self):
        print(f"[+] SOC Bot logged in as {self.user} (ID: {self.user.id})")
        print("[🛡️] SOC Framework active and monitoring.")