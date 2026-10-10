# Trends — Global Multi-Platform Trend Intelligence Radar ⚡

[![Build](https://img.shields.io/badge/signals-120%2B%20live-brightgreen.svg)]()
[![Live Radar](https://img.shields.io/badge/live%20radar-GitHub%20Pages-purple.svg)](https://udbhav-shrinet.github.io/trends/)
[![Zero Auth](https://img.shields.io/badge/auth-zero%20api%20keys-blue.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> A modern, zero-API-key trend intelligence engine and interactive visual dashboard. Ingests, normalizes, and analyzes what the internet is searching, debating, building, and researching in real time across 10+ public channels.

---

## 🚀 Live Interactive Radar

👉 **[Launch Trends Live Studio](https://udbhav-shrinet.github.io/trends/)**

- **Live Pulse Ticker**: Continuous ticker displaying fast-moving signals across the globe.
- **Unified Analytics**: Key metrics tracking Search Spikes, Tech Discourse, Breakout Code, AI Foundation Models, and Macro Market Sentiment (Crypto Fear & Greed).
- **Domain Channels**: Instant filter tabs for Search Trends, Tech & Systems, Dev/GitHub, AI & Research, Crypto/Macro, Fediverse/Social, and Global News.
- **Search & Filter**: Real-time keyword filtering and instant JSON signal export.

---

## ⚡ Cross-Platform Data Channels (Zero API Keys)

| Channel | Source Platforms | Signal Metrics |
|---|---|---|
| **Search Velocity** | Google Trends Daily (US & Global) | Search volume spikes (`100K+`, `500K+`) & contextual news |
| **Tech Discourse** | Hacker News & Techmeme | Community upvotes (`▲ pts`), comment velocity, tech news |
| **Open Source** | GitHub Trending & Breakout Repos | Daily star acceleration (`⭐ +stars today`) & languages |
| **AI Breakthroughs** | Hugging Face Models & arXiv | Top trending foundation models (`❤️ likes`, `📥 downloads`) & preprints |
| **Crypto & Macro** | CoinGecko & Alternative.me | Top trending tokens, 24h price movement & Fear & Greed Index |
| **Social / Fediverse** | Mastodon / Fediverse | Viral public statuses, trending hashtags (`#tags`), shared articles |
| **World Awareness** | BBC World News & Wikipedia Top | Breaking world headlines & most-viewed encyclopedic pageviews |

---

## 🛠️ CLI Quickstart

```bash
# Clone repository
git clone https://github.com/udbhav-shrinet/trends.git
cd trends

# Run the complete multi-platform radar
python trends.py

# Inspect specific channels
python trends.py --channel ai
python trends.py --channel dev
python trends.py --channel crypto
python trends.py --channel tech

# Output full structured JSON signal payload
python trends.py --json

# Rebuild local docs/data.json snapshot
python trends.py --build
```

---

## 🤖 Automated CI/CD Sync

The repository includes a GitHub Actions workflow (`.github/workflows/update_trends.yml`) that automatically executes `generate_feed.py` every 6 hours, re-ingesting live signals and updating `docs/data.json` without requiring any external keys.

---

## 📄 License

MIT License. Engineered with ❤️ by [Udbhav Shrinet](https://github.com/udbhav-shrinet).
