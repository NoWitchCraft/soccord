import asyncio
import discord
from discord.ext import commands
import psutil
from config.settings import settings

class SystemMonitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = settings.DISCORD_CHANNEL_ID
        self.cpu_threshold = settings.CPU_ALERT_THRESHOLD
        self.ram_threshold = settings.RAM_ALERT_THRESHOLD
        self.bg_task = asyncio.create_task(self.monitor_system())

    async def monitor_system(self):
        """Periodically checks CPU and RAM usage against threshold settings."""
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(self.channel_id)
        if not channel:
            return

        print("[*] SystemMonitor Plugin: Started resource tracking...")
        while True:
            await asyncio.sleep(300)  # Check every 5 minutes
            
            cpu_usage = psutil.cpu_percent(interval=1)
            ram_usage = psutil.virtual_memory().percent

            if cpu_usage >= self.cpu_threshold or ram_usage >= self.ram_threshold:
                embed = discord.Embed(
                    title="⚠️ System High Resource Warning",
                    color=discord.Color.gold()
                )
                embed.add_field(name="CPU Usage", value=f"`{cpu_usage}%`", inline=True)
                embed.add_field(name="RAM Usage", value=f"`{ram_usage}%`", inline=True)
                await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(SystemMonitor(bot))