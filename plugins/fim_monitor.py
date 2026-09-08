import asyncio
import hashlib
import os
import discord
from discord.ext import commands
from config.settings import settings


class FileIntegrityMonitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = settings.DISCORD_CHANNEL_ID
        self.watch_paths = getattr(settings, "FIM_WATCH_PATHS", ["/etc/passwd", "/etc/ssh/sshd_config"])
        self.check_interval = getattr(settings, "FIM_CHECK_INTERVAL", 60)
        self.file_hashes: dict[str, str] = {}
        self.bg_task = asyncio.create_task(self.monitor_files())

    def compute_hash(self, filepath: str) -> str | None:
        """Berechnet den SHA-256 Hash einer Datei."""
        if not os.path.exists(filepath):
            return None
        hasher = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                while chunk := f.read(8192):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except (PermissionError, FileNotFoundError):
            return None

    async def monitor_files(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(self.channel_id)
        if not channel:
            print(f"[!] FIM Error: Channel ID {self.channel_id} nicht gefunden.")
            return

        print(f"[*] FIM Plugin gestartet. Überwache {len(self.watch_paths)} Pfade...")

        # Initiales Hashen beim Start
        for path in self.watch_paths:
            self.file_hashes[path] = self.compute_hash(path)

        while True:
            await asyncio.sleep(self.check_interval)
            for path in self.watch_paths:
                current_hash = self.compute_hash(path)
                old_hash = self.file_hashes.get(path)

                if old_hash is not None and current_hash != old_hash:
                    if current_hash is None:
                        # Datei wurde gelöscht
                        embed = discord.Embed(
                            title="🚨 FIM ALERT: Datei gelöscht",
                            description=f"Die überwachte Datei `{path}` wurde entfernt!",
                            color=discord.Color.red()
                        )
                    else:
                        # Datei wurde verändert
                        embed = discord.Embed(
                            title="⚠️ FIM ALERT: Datei verändert",
                            description=f"Änderung in `{path}` erkannt!",
                            color=discord.Color.orange()
                        )
                        embed.add_field(name="Vorher (SHA256)", value=f"`{old_hash[:16]}...`", inline=False)
                        embed.add_field(name="Nachher (SHA256)", value=f"`{current_hash[:16]}...`", inline=False)

                    await channel.send(embed=embed)
                    self.file_hashes[path] = current_hash
                elif old_hash is None and current_hash is not None:
                    # Datei wurde neu erstellt
                    self.file_hashes[path] = current_hash


async def setup(bot):
    await bot.add_cog(FileIntegrityMonitor(bot))