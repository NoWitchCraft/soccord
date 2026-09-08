Create a file /etc/systemd/system/soccord.service

'''
[Unit]
Description=SOCCord Security Operations Center Discord Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/soccord
ExecStart=/opt/soccord/.venv/bin/python main.py
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
'''

# Service neu laden und aktivieren
sudo systemctl daemon-reload
sudo systemctl enable soccord
sudo systemctl start soccord

# Status und Logs prüfen
sudo systemctl status soccord
sudo journalctl -u soccord -f