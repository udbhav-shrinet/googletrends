# Google Trends Automated Analytics & Intelligence Engine

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Interactive Demo](https://img.shields.io/badge/demo-GitHub%20Pages-purple.svg)](https://udbhav-shrinet.github.io/googletrends/)
[![Python Version](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11-blue.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> Production-ready automated data pipeline and analytics dashboard for multi-region keyword interest extraction, volatility scoring, and search trend exploration.

---

## 🚀 Live Interactive Showcase

Experience the live interactive Google Trends Explorer deployed on GitHub Pages:  
👉 **[Launch Interactive Trends Dashboard](https://udbhav-shrinet.github.io/googletrends/)**

---

## ✨ Key Capabilities

- **Multi-Keyword Comparative Extraction**: Simultaneously analyze and normalize relative search volume across up to 5 keywords.
- **Geographic Granularity**: Query global search indices or filter by country, sub-region, and city codes.
- **Automated CSV/JSON Pipeline**: Export time-series interest over time and geographic distribution datasets for downstream ETL pipelines.
- **Interactive Visual Studio**: Client-side dashboard with live Chart.js time-series charts, category presets, and regional penetration metrics.

---

## 🛠️ System Architecture

```text
┌─────────────────┐       ┌────────────────────────┐       ┌──────────────────────┐
│  CLI Parameters │ ───>  │  Pytrends API Client   │ ───>  │ Data Transformation  │
│  Keywords & Geo │       │  Google Trends Gateway │       │   (Pandas Engine)    │
└─────────────────┘       └────────────────────────┘       └──────────┬───────────┘
                                                                      │
                                                   ┌──────────────────┴──────────────────┐
                                                   ▼                                     ▼
                                       ┌───────────────────────┐             ┌───────────────────────┐
                                       │  Structured CSV Export│             │  GitHub Pages Studio  │
                                       │    Time & Region      │             │  Interactive Web App  │
                                       └───────────────────────┘             └───────────────────────┘
```

---

## 📦 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/udbhav-shrinet/googletrends.git
   cd googletrends
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Usage & CLI Reference

### Basic Keyword Comparison
```bash
python main.py --keywords "Python" "JavaScript" "Rust" "Go"
```

### Specify Timeframe & Region
```bash
python main.py --keywords "Docker" "Kubernetes" --timeframe "today 1-m" --geo "US" --export
```

### CLI Flags
| Flag | Description | Default |
| :--- | :--- | :--- |
| `-k`, `--keywords` | List of search keywords to compare (max 5) | `["Python", "JavaScript", "Rust"]` |
| `-t`, `--timeframe` | Google Trends query timeframe string | `today 12-m` |
| `-g`, `--geo` | ISO 3166-1 alpha-2 country code | `""` (Worldwide) |
| `-o`, `--export` | Flag to export outputs to CSV | `False` |

---

## 📊 Interactive Web Demo

The repository includes a web studio in `docs/index.html` configured for GitHub Pages. You can test keyword presets, visualize trend curves, and observe comparative velocity metrics directly in your browser.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
