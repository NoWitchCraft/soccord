import ipaddress
import os
import asyncio
import re
import subprocess # nosec B404
import discord
from discord.ext import commands
from core.rate_limiter import SlidingWindowTracker
from utils.threat_intel import ThreatIntel
from config.settings import settings


class BlockIPView(discord.ui.View):
    def __init__(self, ip: str):
        super().__init__(timeout=None) # Persistent button
        self.ip = ip

    @discord.ui.button(label="🚫 Block IP (UFW)", style=discord.ButtonStyle.danger)
    async def block_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            ipaddress.ip_address(self.ip)
        except ValueError:
            await interaction.response.send_message(
                f"❌ **Refusing to run firewall command: `{self.ip}` is not a valid IP address.**", ephemeral=True
            )
            return

        try:
            # Executes: sudo ufw deny from <IP> to any
            result = subprocess.run( # nosec B603 B607
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
        
        # Regex patterns for SSH log analysis
        self.ssh_success = re.compile(r"Accepted password for (\S+) from (\S+) port")
        self.ssh_key_success = re.compile(r"Accepted publickey for (\S+) from (\S+) port")
        self.ssh_failed = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\S+) port")
        
        self.brute_force_tracker = SlidingWindowTracker(
            threshold_count=settings.BRUTEFORCE_THRESHOLD,
            window_seconds=settings.BRUTEFORCE_WINDOW
        )

        self.bg_task = asyncio.create_task(self.watch_log())

    async def parse_line(self, line: str, channel: discord.TextChannel):
        """Analyzes a log line and triggers Discord alerts for SSH events."""
        # 1. Successful Logins
        m_pw, m_key = self.ssh_success.search(line), self.ssh_key_success.search(line)
        if m_pw or m_key:
            match = m_pw if m_pw else m_key
            user, ip = match.group(1), match.group(2)
            
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
        """Asynchronously streams the log file in real-time (similar to tail -f)."""
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(self.channel_id)
        if not channel:
            print(f"[!] AuthMonitor Error: Discord Channel ID {self.channel_id} not found.")
            return

        print(f"[*] AuthMonitor Plugin: Monitoring {self.log_path}...")
        try:
            f = open(self.log_path, "r", encoding="utf-8", errors="ignore")
            f.seek(0, os.SEEK_END)  # Move pointer to end of file to ignore past events
        except (FileNotFoundError, PermissionError) as e:
            print(f"[!] AuthMonitor Plugin critical failure: {e}")
            return

        try:
            while True:
                line = f.readline()
                if line:
                    await self.parse_line(line, channel)
                    continue

                await asyncio.sleep(1)
                # Log-Rotation erkennen: Datei wurde vom System ersetzt (z.B. durch logrotate)
                try:
                    if os.stat(self.log_path).st_ino != os.fstat(f.fileno()).st_ino:
                        f.close()
                        f = open(self.log_path, "r", encoding="utf-8", errors="ignore")
                except (FileNotFoundError, PermissionError):
                    continue
        finally:
            f.close()


async def setup(bot):
    await bot.add_cog(AuthMonitor(bot))