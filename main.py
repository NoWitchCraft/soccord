import os
import asyncio
import subprocess # nosec B603
import sys
import discord
from discord.ext import commands
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# 2. Initialize Bot with command prefix and intents
intents = discord.Intents.default()
intents.message_content = True  # Required if plugins listen to chat messages
bot = commands.Bot(command_prefix="!", intents=intents)

def check_dependencies():
    """Audits installed Python packages for known security vulnerabilities."""
    print("[*] SOC Self-Check: Auditing dependencies for vulnerabilities...")
    try:
        # Run pip-audit tool in the active environment
        result = subprocess.run( # nosec B603
            [sys.executable, "-m", "pip_audit", "--format", "json"],
            capture_output=True, text=True, check=False
        )
        
        if result.returncode == 0:
            print("[+] SOC Self-Check passed: No known vulnerabilities found in dependencies.")
            return True
        else:
            print("[🚨] WARNING: Security vulnerabilities detected in your Python packages!")
            print(result.stdout)  # Prints the found CVEs in JSON format
            return False
            
    except FileNotFoundError:
        print("[!] Error: 'pip-audit' is not installed or not found in PATH.")
        return False

async def load_plugins():
    """Dynamically loads all Python files inside the plugins/ folder as extensions."""
    plugins_dir = "./plugins"
    if not os.path.exists(plugins_dir):
        os.makedirs(plugins_dir)
        print(f"[*] Created missing directory '{plugins_dir}'. Please place your plugins here.")
        return

    print("[*] Loading plugins...")
    for filename in os.listdir(plugins_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            plugin_name = f"plugins.{filename[:-3]}"
            try:
                await bot.load_extension(plugin_name)
                print(f"[+] Plugin loaded successfully: {plugin_name}")
            except Exception as e:
                print(f"[!] Error loading {plugin_name}: {e}")

@bot.event
async def on_ready():
    print(f"[+] SOC Bot logged in as {bot.user}")
    print("[🛡️] SOC framework is fully operational and protected.")

async def main():
    # Run the dependency audit first
    check_dependencies()
    
    # Load all modular plugins
    await load_plugins()
    
    # Start the Discord bot
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    if not TOKEN:
        print("[!] Configuration Error: DISCORD_TOKEN missing in .env file!")
    else:
        asyncio.run(main())
