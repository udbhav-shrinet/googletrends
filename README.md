# Trends — Multi-Platform Real-Time Trend Intelligence Engine

[![Build](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Live Studio](https://img.shields.io/badge/live%20radar-GitHub%20Pages-purple.svg)](https://udbhav-shrinet.github.io/trends/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> I built **Trends** because I needed a unified, lightning-fast CLI and web dashboard to monitor what the internet is talking about in real time—without having to register for 10 different API keys or deal with rate limits.

---

## 🚀 Live Interactive Radar

👉 **[Launch Trends Live Studio](https://udbhav-shrinet.github.io/trends/)**

---

## ⚡ What it Does

- **Multi-Source Signals**: Ingests trending signals simultaneously across:
  - **Google Trends** (Daily search velocity & volume)
  - **Reddit** (High-engagement community posts from `r/all`, `r/technology`, `r/worldnews`)
  - **Hacker News** (Tech and systems discussions via Firebase endpoints)
  - **Wikipedia** (Daily top pageviews and spikes across global knowledge)
- **Zero API Keys Required**: Completely open endpoints and structured public feeds.
- **Python CLI Engine**: Run `python trends.py` from your terminal for an instant signal summary table.
- **Export Capabilities**: Instant JSON and CSV signal dumps for downstream analytics.

---

## 🛠️ CLI Quickstart

```bash
# Clone the repository
git clone https://github.com/udbhav-shrinet/trends.git
cd trends

# Run the CLI trend scraper
python trends.py
```

---

## 📄 License

MIT License. Feel free to use and adapt for your own data pipelines!
