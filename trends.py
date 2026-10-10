#!/usr/bin/env python3
"""
trends - Unified Multi-Platform Real-Time Trend Scraper & Intelligence CLI
Author: Udbhav Shrinet

Collects trending signals across Google Trends, Reddit, Hacker News, Wikipedia, and Global News
without requiring any API keys or tokens.
"""

import sys
import os
import argparse
import json
from datetime import datetime, timezone
from generate_feed import (
    get_google_trends,
    get_hacker_news,
    get_github_trending,
    get_huggingface_trending,
    get_arxiv_recent,
    get_crypto_trending,
    get_mastodon_trends,
    get_techmeme,
    get_bbc_news,
    get_wikipedia_top,
    build_snapshot
)

# ANSI terminal formatting
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
PURPLE = "\033[38;2;192;132;252m"
CYAN = "\033[36m"
GREEN = "\033[32m"
AMBER = "\033[33m"
BLUE = "\033[34m"
RED = "\033[31m"

def print_banner():
    banner = f"""
{PURPLE}{BOLD}  ⚡ TRENDS — MULTI-PLATFORM SIGNAL INTELLIGENCE{RESET}
{DIM}  Unified Real-Time Radar across 10+ Public Global Channels{RESET}
{DIM}  Timestamp: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}{RESET}
{"─" * 78}
"""
    print(banner)

def print_section(title, icon, items, max_items=8):
    if not items:
        return
    print(f"\n{BOLD}{PURPLE}● {icon} {title.upper()}{RESET} {DIM}({len(items)} signals detected){RESET}")
    print(f"{DIM}{'─' * 74}{RESET}")
    for idx, it in enumerate(items[:max_items], 1):
        name = it.get('title') or it.get('name') or 'Untitled'
        source = it.get('source', '')
        metric = it.get('metric', '')
        url = it.get('url', '')
        
        print(f" {CYAN}{idx:2d}.{RESET} {BOLD}{name[:62]}{RESET}")
        print(f"     {DIM}↳ [{source}] {metric}{RESET}")
        if url:
            print(f"       {DIM}{url[:70]}{RESET}")

def main():
    parser = argparse.ArgumentParser(description="Multi-Platform Trend Intelligence Radar CLI")
    parser.add_argument('--channel', choices=['all', 'search', 'tech', 'dev', 'ai', 'crypto', 'social', 'news'], default='all', help="Specific channel to inspect")
    parser.add_argument('--limit', type=int, default=8, help="Max signals to display per channel")
    parser.add_argument('--json', action='store_true', help="Output raw JSON signal bundle")
    parser.add_argument('--build', action='store_true', help="Re-build docs/data.json snapshot for web dashboard")
    args = parser.parse_args()

    if args.build:
        print("[*] Rebuilding snapshot for web dashboard...")
        payload = build_snapshot()
        print(f"[✓] Done. Total signals: {payload['total_signals']}")
        return

    if args.json:
        payload = build_snapshot()
        print(json.dumps(payload, indent=2))
        return

    print_banner()

    if args.channel in ['all', 'search']:
        gt = get_google_trends('US')
        print_section("Google Trends (High Search Velocity)", "📈", gt, args.limit)

    if args.channel in ['all', 'tech']:
        hn = get_hacker_news(args.limit)
        tm = get_techmeme()
        print_section("Tech & Systems Discussions (Hacker News & Techmeme)", "💻", hn + tm, args.limit)

    if args.channel in ['all', 'dev']:
        gh = get_github_trending()
        print_section("Developer Ecosystem (GitHub Trending Repos)", "⚡", gh, args.limit)

    if args.channel in ['all', 'ai']:
        hf = get_huggingface_trending()
        arxiv = get_arxiv_recent()
        print_section("AI & Research (Hugging Face Models & arXiv Papers)", "🤖", hf + arxiv, args.limit)

    if args.channel in ['all', 'crypto']:
        crypto, fng = get_crypto_trending()
        print(f"\n{AMBER}{BOLD}💰 CRYPTO RADAR{RESET} {DIM}• Fear & Greed Index: {fng['value']} ({fng['sentiment']}){RESET}")
        print_section("CoinGecko Trending Tokens", "💎", crypto, args.limit)

    if args.channel in ['all', 'social']:
        fedi, tags = get_mastodon_trends()
        if tags:
            print(f"\n{BOLD}{PURPLE}🏷️  TRENDING HASHTAGS:{RESET} {DIM}{', '.join(['#' + t for t in tags[:8]])}{RESET}")
        print_section("Fediverse / Social Discussions (Mastodon)", "🌐", fedi, args.limit)

    if args.channel in ['all', 'news']:
        bbc = get_bbc_news()
        wiki = get_wikipedia_top()
        print_section("Global Awareness & Knowledge (BBC & Wikipedia Top Pageviews)", "🌍", bbc + wiki, args.limit)

    print(f"\n{'─' * 78}")
    print(f"{DIM}Tip: Run `python trends.py --channel ai` or explore the live web dashboard at:{RESET}")
    print(f"{PURPLE}https://udbhav-shrinet.github.io/trends/{RESET}\n")

if __name__ == '__main__':
    main()

