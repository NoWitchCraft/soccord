import os
import asyncio
import re
import discord
from discord.ext import commands
<<<<<<< HEAD
from core.rate_limiter import SlidingWindowTracker
from utils.threat_intel import ThreatIntel
from config.settings import settings
import subprocess # nosec B404

class BlockIPView(discord.ui.View):
    def __init__(self, ip: str):
        super().__init__(timeout=None) # Persistent button
        self.ip = ip

    @discord.ui.button(label="🚫 Block IP (UFW)", style=discord.ButtonStyle.danger)
    async def block_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Command execution to block IP
        try:
            # Executes: sudo ufw deny from <IP> to any
            result = subprocess.run( # nosec B603
                ["sudo", "ufw", "deny", "from", self.ip, "to", "any"],
                capture_output=True, text=True, check=False
            )
            if result.returncode == 0:
                await interaction.response.send_message(
                    f"✅ **IP `{self.ip}` has been successfully blocked via UFW.**", ephemeral=False
                )
                button.disabled = True
                await interaction.message.edit(view=self)
            else:
                await interaction.response.send_message(
                    f"❌ **Failed to block IP `{self.ip}`:** {result.stderr}", ephemeral=True
                )
        except Exception as e:
            await interaction.response.send_message(f"❌ **Error executing firewall command:** {e}", ephemeral=True)

            
class AuthMonitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = settings.DISCORD_CHANNEL_ID
        self.log_path = settings.AUTH_LOG_PATH
        
=======

class AuthMonitor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = int(os.getenv("DISCORD_CHANNEL_ID"))
        self.log_path = os.getenv("AUTH_LOG_PATH", "/var/log/auth.log")
        
        # Regex patterns for SSH log analysis
>>>>>>> d5197c4d9754fe58d44f9db2c40f5b72d9d23d9b
        self.ssh_success = re.compile(r"Accepted password for (\S+) from (\S+) port")
        self.ssh_key_success = re.compile(r"Accepted publickey for (\S+) from (\S+) port")
        self.ssh_failed = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\S+) port")
        
<<<<<<< HEAD
        self.brute_force_tracker = SlidingWindowTracker(
            threshold_count=settings.BRUTEFORCE_THRESHOLD,
            window_seconds=settings.BRUTEFORCE_WINDOW
        )

        self.bg_task = asyncio.create_task(self.watch_log())

    async def parse_line(self, line: str, channel: discord.TextChannel):
        # 1. Successful Logins
=======
        # Start the log watching routine as a background task
        self.bg_task = asyncio.create_task(self.watch_log())

    async def parse_line(self, line, channel):
        """Analyzes a log line and triggers Discord alerts for SSH events."""
        # Check for successful logins (Password or Key)
>>>>>>> d5197c4d9754fe58d44f9db2c40f5b72d9d23d9b
        m_pw, m_key = self.ssh_success.search(line), self.ssh_key_success.search(line)
        if m_pw or m_key:
            match = m_pw if m_pw else m_key
            user, ip = match.group(1), match.group(2)
            
<<<<<<< HEAD
            self.brute_force_tracker.reset(ip)
            intel = await ThreatIntel.get_ip_reputation(ip)
            
            embed = discord.Embed(title="🟢 Successful SSH Login", color=discord.Color.green())
            embed.add_field(name="User", value=f"`{user}`", inline=True)
            embed.add_field(name="IP Address", value=f"`{ip}`", inline=True)
            embed.add_field(name="Location", value=f"`{intel['country']}`", inline=True)
            embed.add_field(name="Method", value="`Password`" if m_pw else "`SSH-Key`", inline=True)
            await channel.send(embed=embed)
            return

        # 2. Failed Logins & Brute-Force
        m_fail = self.ssh_failed.search(line)
        if m_fail:
            user, ip = m_fail.group(1), m_fail.group(2)
            is_threshold_exceeded = self.brute_force_tracker.register_attempt(ip)
            intel = await ThreatIntel.get_ip_reputation(ip)
            
            if is_threshold_exceeded:
                embed = discord.Embed(
                    title="🚨 BRUTE-FORCE ALERT",
                    description="Excessive failed login attempts detected.",
                    color=discord.Color.dark_red()
                )
                embed.add_field(name="Target User", value=f"`{user}`", inline=True)
                embed.add_field(name="Attacker IP", value=f"`{ip}`", inline=True)
                embed.add_field(name="Location", value=f"`{intel['country']}`", inline=True)
                embed.add_field(name="Abuse Confidence", value=f"`{intel['abuse_score']}%`", inline=True)
                await channel.send(embed=embed, view=BlockIPView(ip))
            elif ip not in self.brute_force_tracker.alerted_keys:
                embed = discord.Embed(title="⚠️ Failed SSH Login", color=discord.Color.orange())
                embed.add_field(name="Target User", value=f"`{user}`", inline=True)
                embed.add_field(name="IP Address", value=f"`{ip}`", inline=True)
                embed.add_field(name="Location", value=f"`{intel['country']}`", inline=True)
                await channel.send(embed=embed)

    async def watch_log(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(self.channel_id)
        if not channel:
=======
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
>>>>>>> d5197c4d9754fe58d44f9db2c40f5b72d9d23d9b
            return

        print(f"[*] AuthMonitor Plugin: Monitoring {self.log_path}...")
        try:
            with open(self.log_path, "r", encoding="utf-8", errors="ignore") as f:
<<<<<<< HEAD
=======
                # Move pointer to the end of file to ignore past events
>>>>>>> d5197c4d9754fe58d44f9db2c40f5b72d9d23d9b
                f.seek(0, os.SEEK_END)
                while True:
                    line = f.readline()
                    if not line:
<<<<<<< HEAD
                        await asyncio.sleep(1)
                        continue
                    await self.parse_line(line, channel)
        except Exception as e:
            print(f"[!] AuthMonitor Error: {e}")

async def setup(bot):
    await bot.add_cog(AuthMonitor(bot))
=======
                        # No new line, sleep briefly to prevent CPU spinning
                        await asyncio.sleep(1)
                        continue
                    await self.parse_line(line, channel)
        except (FileNotFoundError, PermissionError) as e:
            print(f"[!] AuthMonitor Plugin critical failure: {e}")

# Setup function required by main.py to dynamically register the Cog
async def setup(bot):
    await bot.add_cog(AuthMonitor(bot))
>>>>>>> d5197c4d9754fe58d44f9db2c40f5b72d9d23d9b
