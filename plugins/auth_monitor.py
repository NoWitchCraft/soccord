import os
import asyncio
import re
import discord
from discord.ext import commands

class AuthMonitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = int(os.getenv("DISCORD_CHANNEL_ID"))
        self.log_path = os.getenv("AUTH_LOG_PATH", "/var/log/auth.log")
        
        # Regex patterns for SSH log analysis
        self.ssh_success = re.compile(r"Accepted password for (\S+) from (\S+) port")
        self.ssh_key_success = re.compile(r"Accepted publickey for (\S+) from (\S+) port")
        self.ssh_failed = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\S+) port")
        
        # Start the log watching routine as a background task
        self.bg_task = asyncio.create_task(self.watch_log())

    async def parse_line(self, line, channel):
        """Analyzes a log line and triggers Discord alerts for SSH events."""
        # Check for successful logins (Password or Key)
        m_pw, m_key = self.ssh_success.search(line), self.ssh_key_success.search(line)
        if m_pw or m_key:
            match = m_pw if m_pw else m_key
            user, ip = match.group(1), match.group(2)
            
            embed = discord.Embed(title="🟢 Successful SSH Login", color=discord.Color.green())
            embed.add_field(name="User", value=f"`{user}`", inline=True)
            embed.add_field(name="IP Address", value=f"`{ip}`", inline=True)
            embed.add_field(name="Auth Method", value="`Password`" if m_pw else "`SSH-Key`", inline=True)
            await channel.send(embed=embed)
            return

        # Check for failed login attempts
        m_fail = self.ssh_failed.search(line)
        if m_fail:
            user, ip = m_fail.group(1), m_fail.group(2)
            
            embed = discord.Embed(title="🚨 Failed SSH Login Attempt", color=discord.Color.red())
            embed.add_field(name="Target User", value=f"`{user}`", inline=True)
            embed.add_field(name="IP Address", value=f"`{ip}`", inline=True)
            await channel.send(embed=embed)

    async def watch_log(self):
        """Asynchronously streams the log file in real-time (similar to tail -f)."""
        # Wait until the bot connection is fully established
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(self.channel_id)
        
        if not channel:
            print(f"[!] AuthMonitor Error: Discord Channel ID {self.channel_id} not found.")
            return

        print(f"[*] AuthMonitor Plugin: Monitoring {self.log_path}...")
        try:
            with open(self.log_path, "r", encoding="utf-8", errors="ignore") as f:
                # Move pointer to the end of file to ignore past events
                f.seek(0, os.SEEK_END)
                while True:
                    line = f.readline()
                    if not line:
                        # No new line, sleep briefly to prevent CPU spinning
                        await asyncio.sleep(1)
                        continue
                    await self.parse_line(line, channel)
        except (FileNotFoundError, PermissionError) as e:
            print(f"[!] AuthMonitor Plugin critical failure: {e}")

# Setup function required by main.py to dynamically register the Cog
async def setup(bot):
    await bot.add_cog(AuthMonitor(bot))
