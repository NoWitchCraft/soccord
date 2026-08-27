# soccord 🛡️🐍

**soccord** is a lightweight, automated SOC (Security Operations Center) companion written in Python. It turns your Discord server into a centralized security monitoring hub by collecting security alerts, system logs, and threat indicators from your infrastructure and forwarding them instantly to dedicated Discord channels via Webhooks.

Perfect for small teams, developers, and DevOps homelabs who want real-time security visibility without leaving their primary chat application.

## ✨ Key Features
* **Real-Time Alerting:** Instant push notifications for critical security events.
* **Smart Filtering:** Deduplicates repetitive logs to prevent alert fatigue in your channels.
* **Rich Embeds:** Displays alerts using clean, color-coded Discord embeds (e.g., Red for critical threats, Yellow for warnings).
* **Multi-Source Integration:** Easily ingest logs from firewalls, servers (syslog), cloud services, or custom applications.
* **Pure Python:** Highly extensible, easy to deploy, and low resource footprint.

## 🚀 Getting Started

### Prerequisites
* A Discord server where you have permissions to manage Webhooks.
* Python 3.10 or higher installed.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com
   cd soccord
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -bin/venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Configure your `.env` file with your Discord Webhook URL.
4. Run the application:
   ```bash
   python main.py
   ```

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📝 License
This project is licensed under the MIT License.
