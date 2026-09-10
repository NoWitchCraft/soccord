# soccord 🛡️🐍

**soccord** is a lightweight, automated SOC (Security Operations Center) companion written in Python. It runs as a Discord bot that monitors your server for security-relevant events — SSH logins, file integrity changes, and resource exhaustion — and posts alerts directly into a dedicated Discord channel as color-coded embeds.

Perfect for small teams, developers, and DevOps homelabs who want real-time security visibility without leaving their primary chat application.

## ✨ Key Features
* **SSH Login Monitoring** — tails your auth log in real time, flags failed/successful logins, and detects brute-force attempts via a sliding-window threshold. Brute-force alerts include a one-click "Block IP (UFW)" button.
* **File Integrity Monitoring (FIM)** — periodically SHA-256-hashes a configurable list of files and alerts on any change, creation, or deletion.
* **System Resource Monitoring** — alerts when CPU or RAM usage crosses configured thresholds.
* **Threat Intelligence Enrichment** — attaches GeoIP location and (optionally) AbuseIPDB abuse score to every IP-related alert.
* **Rich Embeds** — color-coded Discord embeds (green = success, orange = warning, red = critical).
* **Plugin Architecture** — drop a new cog into `plugins/` and it's loaded automatically at startup, no registration needed.

## 🚀 Getting Started

### Prerequisites
* A Discord server and a [Discord Bot application](https://discord.com/developers/applications) invited to it, with the `Message Content` privileged intent enabled.
* Python 3.10 or higher installed.
* A Linux host (the log/FIM/firewall integrations assume `/var/log/auth.log` and `ufw`).

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/NoWitchCraft/soccord
   cd soccord
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your `DISCORD_TOKEN` and `DISCORD_CHANNEL_ID` at minimum. See `.env.example` for the full list of variables (log paths, FIM watch list, brute-force/resource thresholds, optional `ABUSEIPDB_API_KEY`).
4. Run the application:
   ```bash
   python main.py
   ```

For running soccord persistently on a server, see [INSTALL.MD](INSTALL.MD) for a systemd service example.

## 🔍 Quality & Security Checks
Every push/PR to `main` runs through CI (`.github/workflows/ci.yml`): `flake8` linting, a `bandit` security scan, and a `pip-audit` dependency vulnerability check.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) before opening a PR, and [SECURITY.md](SECURITY.md) for how to report vulnerabilities responsibly.

## 📝 License
This project is licensed under the MIT License.
