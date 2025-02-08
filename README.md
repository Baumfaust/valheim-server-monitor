# Valheim Server Monitor Project ⚔️🏹

Welcome to the **Valheim Server Monitor Project** – an all-in-one solution to monitor your Valheim server, send real-time notifications to your Discord community, and visualize server metrics on a Grafana board. Inspired by the rugged spirit of Norse legends, this project is built with modern Python async technology to keep you in the loop during every epic server battle!

---

## 🚀 Features

- **Log Monitoring:**  
  Continuously watch your server logs for key events such as session starts and player joins.
  
- **Discord Bot Integration:**  
  Instantly notify your Discord community about important events. 🤖
  
- **Grafana Dashboard:**  
  Visualize server metrics and trends on a sleek Grafana board. 📊
  
- **Async & Event-Driven:**  
  Built with Python's `asyncio` and a custom event bus for efficient, real-time processing.
  
- **Graceful Shutdown:**  
  All components will cleanly exit on Ctrl+C or system signals (like `systemctl stop`), ensuring data integrity and resource cleanup. 🚦

---

## 🏗️ Architecture

The project is divided into three main components:

1. **Log Monitor:**  
   Reads server logs and extracts events (using pattern matching) to create structured log entries.

2. **Discord Bot:**  
   Subscribes to the event bus and sends notifications to your Discord server in the appropriate channel.

3. **Grafana Sender:**  
   Publishes parsed log events to your Grafana dashboard for real-time visualization.

All components communicate via an internal async event bus, ensuring that messages are processed quickly and efficiently.

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/valheim-server-monitor.git
cd valheim-server-monitor
```

### 2. Create & Activate a Virtual Environment

```bash
python -m venv .venv
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Your Environment

Create a `.env` file in the root directory and add your configuration variables:

```dotenv
DISCORD_TOKEN=your-discord-bot-token
DISCORD_CHANNEL_ID=your-discord-channel-id
# (Add any additional configuration as needed)
```

---

## 🚀 Running the Project

Start the project with:

```bash
python main.py
```

The monitor will begin watching your server logs, the Discord bot will be active and subscribe to events, and your Grafana board will receive real-time metrics.

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for improvements, bug fixes, or additional features, please:

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- Thanks to the Python community for powerful async libraries.
- Kudos to Discord and Grafana for their robust platforms.
- Inspired by Norse mythology and the spirit of adventure – may your server always stand victorious! 🛡️🗡️

---

Happy monitoring, and may your battles be legendary! ⚔️🏰
