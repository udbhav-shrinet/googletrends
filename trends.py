#!/usr/bin/env python3
"""
trends - Unified Multi-Platform Real-Time Trend Scraper & Intelligence CLI
Author: Udbhav Shrinet

Collects trending signals across Google Trends, Reddit, Hacker News, Wikipedia, and Global News
without requiring any API keys or tokens.
"""

import sys
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def fetch_json(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=8) as resp:
        return json.loads(resp.read().decode('utf-8'))

def fetch_xml(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=8) as resp:
        return ET.fromstring(resp.read().decode('utf-8'))

def get_hacker_news(limit=15):
    items = []
    try:
        top_ids = fetch_json('https://hacker-news.firebaseio.com/v0/topstories.json')[:limit]
        for sid in top_ids:
            try:
                story = fetch_json(f'https://hacker-news.firebaseio.com/v0/item/{sid}.json')
                if story and 'title' in story:
                    items.append({
                        'source': 'Hacker News',
                        'title': story.get('title'),
                        'score': story.get('score', 0),
                        'comments': story.get('descendants', 0),
                        'url': story.get('url', f'https://news.ycombinator.com/item?id={sid}')
                    })
            except Exception:
                continue
    except Exception as e:
        print(f"[!] Hacker News fetch error: {e}", file=sys.stderr)
    return items

def get_reddit(subreddit='all', limit=15):
    items = []
    try:
        data = fetch_json(f'https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}')
        for child in data.get('data', {}).get('children', []):
            d = child.get('data', {})
            items.append({
                'source': f'Reddit (r/{d.get("subreddit")})',
                'title': d.get('title'),
                'score': d.get('score', 0),
                'comments': d.get('num_comments', 0),
                'url': f'https://reddit.com{d.get("permalink")}'
            })
    except Exception as e:
        print(f"[!] Reddit fetch error: {e}", file=sys.stderr)
    return items

def get_wikipedia_trending():
    items = []
    try:
        yesterday = datetime.utcnow()
        # YYYY/MM/DD
        d_str = yesterday.strftime('%Y/%m/%d')
        url = f'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{d_str}'
        data = fetch_json(url)
        articles = data.get('items', [{}])[0].get('articles', [])
        for art in articles[:15]:
            title = art.get('article', '').replace('_', ' ')
            if title in ['Main Page', 'Special:Search', '-']:
                continue
            items.append({
                'source': 'Wikipedia Trending',
                'title': title,
                'views': art.get('views', 0),
                'url': f'https://en.wikipedia.org/wiki/{art.get("article")}'
            })
    except Exception as e:
        print(f"[!] Wikipedia fetch error: {e}", file=sys.stderr)
    return items

def get_google_daily_trends(geo='US'):
    items = []
    try:
        url = f'https://trends.google.com/trends/trending/rss?geo={geo}'
        root = fetch_xml(url)
        for item in root.findall('.//item'):
            title = item.find('title')
            traffic = item.find('{https://trends.google.com/trends/trending}approx_traffic')
            link = item.find('link')
            items.append({
                'source': f'Google Trends ({geo})',
                'title': title.text if title is not None else 'Unknown',
                'traffic': traffic.text if traffic is not None else 'N/A',
                'url': link.text if link is not None else ''
            })
    except Exception as e:
        print(f"[!] Google Trends fetch error: {e}", file=sys.stderr)
    return items

def main():
    print("=" * 70)
    print("🔥 TRENDS - Multi-Platform Real-Time Signal Ingestion")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    print("
[+] Pulling Google Trends Daily Feed...")
    g_trends = get_google_daily_trends('US')
    for idx, t in enumerate(g_trends[:8], 1):
        print(f" {idx:2d}. [Google {t['traffic']}] {t['title']}")
        
    print("
[+] Pulling Reddit Top Signals (r/all)...")
    r_trends = get_reddit('all', 8)
    for idx, t in enumerate(r_trends[:8], 1):
        print(f" {idx:2d}. [Reddit ▲{t['score']}] {t['title'][:65]}")
        
    print("
[+] Pulling Hacker News Top Stories...")
    hn_trends = get_hacker_news(8)
    for idx, t in enumerate(hn_trends[:8], 1):
        print(f" {idx:2d}. [HN ▲{t['score']}] {t['title'][:65]}")

    print("
[+] Pulling Wikipedia Trending Topics...")
    wiki_trends = get_wikipedia_trending()
    for idx, t in enumerate(wiki_trends[:8], 1):
        print(f" {idx:2d}. [Wiki {t.get('views', 0):,} views] {t['title']}")

    print("
" + "=" * 70)
    print("✓ Signals collected. Launch web dashboard: https://udbhav-shrinet.github.io/trends/")

if __name__ == '__main__':
    main()
