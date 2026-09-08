import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Discord
    DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN", "")
    DISCORD_CHANNEL_ID: int = int(os.getenv("DISCORD_CHANNEL_ID", 0))

    # Logs
    AUTH_LOG_PATH: str = os.getenv("AUTH_LOG_PATH", "/var/log/auth.log")

    # FIM (Liest kommagetrennte Pfade aus .env, sonst Fallback-Liste)
    FIM_WATCH_PATHS: list[str] = [
        path.strip() 
        for path in os.getenv("FIM_WATCH_PATHS", "/etc/passwd,/etc/ssh/sshd_config,/etc/shadow").split(",") 
        if path.strip()
    ]
    FIM_CHECK_INTERVAL: int = int(os.getenv("FIM_CHECK_INTERVAL", 60))

    # Thresholds
    BRUTEFORCE_THRESHOLD: int = int(os.getenv("BRUTEFORCE_THRESHOLD", 5))
    BRUTEFORCE_WINDOW: int = int(os.getenv("BRUTEFORCE_WINDOW", 60))
    CPU_ALERT_THRESHOLD: float = float(os.getenv("CPU_ALERT_THRESHOLD", 85.0))
    RAM_ALERT_THRESHOLD: float = float(os.getenv("RAM_ALERT_THRESHOLD", 90.0))

    # API Keys
    ABUSEIPDB_API_KEY: str = os.getenv("ABUSEIPDB_API_KEY", "")

settings = Settings()