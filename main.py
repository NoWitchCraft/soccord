import asyncio
from config.settings import settings
from core.bot import SOCBot
from utils.security import run_dependency_audit

async def main():
    # 1. Self-audit on startup
    run_dependency_audit()

    # 2. Initialize and start SOC Bot
    bot = SOCBot()
    async with bot:
        await bot.start(settings.DISCORD_TOKEN)

if __name__ == "__main__":
    if settings.DISCORD_TOKEN:
        asyncio.run(main())
    else:
        print("[!] Configuration error: DISCORD_TOKEN missing.")