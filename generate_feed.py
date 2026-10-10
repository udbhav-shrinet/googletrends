#!/usr/bin/env python3
"""
trends data aggregator & live snapshot generator
Fetches signals across 10+ public, zero-auth APIs and RSS feeds:
1. Google Trends (Daily search trends RSS - US & Global)
2. Hacker News (Top Frontpage via Algolia & Firebase)
3. GitHub Trending & Breakout Repos (Repositories exploding in stars)
4. Hugging Face AI Models (Top trending open-source models)
5. arXiv AI/ML Papers (Latest breakthrough research)
6. CoinGecko Crypto & Fear/Greed Index (Trending tokens & sentiment)
7. Fediverse / Mastodon (Trending viral posts, hashtags, and shared news)
8. Techmeme & Tech News (Top tech journalism headlines)
9. Wikipedia Trending (Most viewed articles globally)
10. Global News Feeds (BBC Top World Stories)
"""

import os
import sys
import json
import ssl
import re
from datetime import datetime, timezone, timedelta
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

# SSL context bypassing expired local store certificates
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 TrendsIntelligence/3.0'
}

def fetch_json(url, timeout=7):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        return json.loads(r.read().decode('utf-8'))

def fetch_xml(url, timeout=7):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        return ET.fromstring(r.read())

def get_google_trends(geo='US'):
    items = []
    try:
        root = fetch_xml(f'https://trends.google.com/trending/rss?geo={geo}')
        for it in root.findall('.//item')[:12]:
            title = it.find('title')
            traffic = it.find('{https://trends.google.com/trending/rss}approx_traffic')
            link = it.find('link')
            news_items = it.findall('{https://trends.google.com/trending/rss}news_item')
            snippet = ''
            if news_items:
                snip_node = news_items[0].find('{https://trends.google.com/trending/rss}news_item_snippet')
                if snip_node is not None and snip_node.text:
                    snippet = snip_node.text
            title_text = title.text.strip() if title is not None and title.text else 'Unknown'
            traffic_text = traffic.text.strip() if traffic is not None and traffic.text else '10K+'
            items.append({
                'category': 'search',
                'source': f'Google Trends ({geo})',
                'title': title_text,
                'traffic': traffic_text,
                'snippet': snippet,
                'url': link.text.strip() if link is not None and link.text else f'https://trends.google.com/trends/explore?q={urllib.parse.quote(title_text)}',
                'badge': 'Search Spike',
                'metric': f"🔥 {traffic_text} searches"
            })
    except Exception as e:
        print(f"[!] Google Trends ({geo}) error: {e}", file=sys.stderr)
    return items

def get_hacker_news(limit=15):
    items = []
    try:
        data = fetch_json(f'https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage={limit}')
        for h in data.get('hits', []):
            items.append({
                'category': 'tech',
                'source': 'Hacker News',
                'title': h.get('title') or 'Untitled HN Post',
                'author': h.get('author'),
                'points': h.get('points', 0),
                'comments': h.get('num_comments', 0),
                'url': h.get('url') or f"https://news.ycombinator.com/item?id={h.get('objectID')}",
                'badge': 'Front Page',
                'metric': f"▲ {h.get('points', 0):,} pts • 💬 {h.get('num_comments', 0):,} comments"
            })
    except Exception as e:
        print(f"[!] HN Algolia error: {e}", file=sys.stderr)
    return items

def get_github_trending():
    items = []
    try:
        req = urllib.request.Request('https://github.com/trending?since=daily', headers=HEADERS)
        with urllib.request.urlopen(req, timeout=7, context=ctx) as r:
            html = r.read().decode('utf-8')
            articles = re.findall(r'<article class=\"Box-row\">([\s\S]*?)</article>', html)
            for art in articles[:12]:
                repo_m = re.search(r'href=\"/([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)\"', art)
                if not repo_m or repo_m.group(1).startswith('sponsors/'):
                    continue
                repo_name = repo_m.group(1)
                desc_m = re.search(r'<p class=\"col-9 color-fg-muted my-1 pr-4\">\s*([\s\S]*?)\s*</p>', art)
                desc = re.sub(r'<[^>]+>', '', desc_m.group(1)).strip() if desc_m else ''
                lang_m = re.search(r'itemprop=\"programmingLanguage\">([^<]+)<', art)
                lang = lang_m.group(1).strip() if lang_m else 'Code'
                stars_today_m = re.search(r'([0-9,]+)\s+stars today', art)
                stars_today = stars_today_m.group(1) if stars_today_m else ''

                items.append({
                    'category': 'dev',
                    'source': 'GitHub Trending',
                    'title': repo_name,
                    'description': desc,
                    'language': lang,
                    'url': f"https://github.com/{repo_name}",
                    'badge': lang,
                    'metric': f"⭐ +{stars_today} today" if stars_today else "⭐ High Velocity"
                })
    except Exception as e:
        print(f"[!] GitHub trending scrape error: {e}", file=sys.stderr)

    if len(items) < 6:
        try:
            cutoff = (datetime.now(timezone.utc) - timedelta(days=25)).strftime('%Y-%m-%d')
            data = fetch_json(f'https://api.github.com/search/repositories?q=created:>{cutoff}+stars:>200&sort=stars&order=desc&per_page=10')
            for r in data.get('items', []):
                items.append({
                    'category': 'dev',
                    'source': 'GitHub Breakout',
                    'title': r.get('full_name'),
                    'description': r.get('description') or '',
                    'language': r.get('language') or 'Code',
                    'url': r.get('html_url'),
                    'badge': r.get('language') or 'Code',
                    'metric': f"⭐ {r.get('stargazers_count', 0):,} stars"
                })
        except Exception as e:
            print(f"[!] GitHub API fallback error: {e}", file=sys.stderr)
    return items

def get_huggingface_trending():
    items = []
    try:
        data = fetch_json('https://huggingface.co/api/models?sort=trendingScore&direction=-1&limit=12')
        for m in data:
            model_id = m.get('id')
            downloads = m.get('downloads', 0)
            likes = m.get('likes', 0)
            pipeline = m.get('pipeline_tag', 'AI Model')
            items.append({
                'category': 'ai',
                'source': 'Hugging Face',
                'title': model_id,
                'description': f"Trending AI Foundation Model ({pipeline})",
                'url': f"https://huggingface.co/{model_id}",
                'badge': pipeline,
                'metric': f"❤️ {likes:,} likes • 📥 {downloads:,} dls"
            })
    except Exception as e:
        print(f"[!] Hugging Face error: {e}", file=sys.stderr)
    return items

def get_arxiv_recent():
    items = []
    try:
        url = 'https://export.arxiv.org/api/query?search_query=cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL&sortBy=submittedDate&sortOrder=descending&max_results=8'
        root = fetch_xml(url)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        for entry in root.findall('atom:entry', ns):
            title_node = entry.find('atom:title', ns)
            summary_node = entry.find('atom:summary', ns)
            link_node = entry.find('atom:id', ns)
            title = title_node.text.strip().replace('\n', ' ') if title_node is not None and title_node.text else 'arXiv Research'
            summary = summary_node.text.strip().replace('\n', ' ') if summary_node is not None and summary_node.text else ''
            author = entry.find('atom:author/atom:name', ns)
            author_name = author.text if author is not None and author.text else 'arXiv Researcher'
            link = link_node.text if link_node is not None and link_node.text else 'https://arxiv.org'
            items.append({
                'category': 'ai',
                'source': 'arXiv AI/ML',
                'title': title,
                'description': summary[:140] + '...' if len(summary) > 140 else summary,
                'author': author_name,
                'url': link,
                'badge': 'Research Paper',
                'metric': f"📄 {author_name}"
            })
    except Exception as e:
        print(f"[!] arXiv error: {e}", file=sys.stderr)
    return items

def get_crypto_trending():
    items = []
    fng_val = '50'
    fng_class = 'Neutral'
    try:
        fng_data = fetch_json('https://api.alternative.me/fng/?limit=1')
        fng_val = fng_data['data'][0]['value']
        fng_class = fng_data['data'][0]['value_classification']
    except Exception:
        pass

    try:
        cg = fetch_json('https://api.coingecko.com/api/v3/search/trending')
        for c in cg.get('coins', [])[:8]:
            it = c.get('item', {})
            price_change = it.get('data', {}).get('price_change_percentage_24h', {}).get('usd', 0)
            symbol = it.get('symbol', '').upper()
            items.append({
                'category': 'finance',
                'source': 'CoinGecko Trending',
                'title': f"{it.get('name')} ({symbol})",
                'rank': it.get('market_cap_rank', 'N/A'),
                'url': f"https://www.coingecko.com/en/coins/{it.get('id')}",
                'badge': f"Rank #{it.get('market_cap_rank', '?')}",
                'metric': f"💎 24h: {price_change:+.1f}% • Sentiment: {fng_val} ({fng_class})",
                'fng': {'value': fng_val, 'sentiment': fng_class}
            })
    except Exception as e:
        print(f"[!] CoinGecko error: {e}", file=sys.stderr)
    return items, {'value': fng_val, 'sentiment': fng_class}

def get_mastodon_trends():
    items = []
    try:
        statuses = fetch_json('https://mastodon.social/api/v1/trends/statuses')
        for s in statuses[:8]:
            clean_text = re.sub(r'<[^>]+>', '', s.get('content', '')).strip()
            if not clean_text:
                continue
            account = s.get('account', {})
            favs = s.get('favourites_count', 0)
            reblogs = s.get('reblogs_count', 0)
            items.append({
                'category': 'social',
                'source': 'Fediverse / Mastodon',
                'title': clean_text[:140] + ('...' if len(clean_text) > 140 else ''),
                'author': f"@{account.get('username')}",
                'url': s.get('url'),
                'badge': 'Viral Post',
                'metric': f"❤️ {favs:,} • 🔁 {reblogs:,}"
            })
    except Exception as e:
        print(f"[!] Mastodon status trends error: {e}", file=sys.stderr)

    try:
        links = fetch_json('https://mastodon.social/api/v1/trends/links')
        for l in links[:6]:
            items.append({
                'category': 'social',
                'source': 'Mastodon Viral News',
                'title': l.get('title'),
                'description': (l.get('description') or '')[:120],
                'url': l.get('url'),
                'badge': 'Shared Link',
                'metric': f"🔥 {l.get('history', [{}])[0].get('uses', 0)} shares"
            })
    except Exception as e:
        print(f"[!] Mastodon links trends error: {e}", file=sys.stderr)

    tags = []
    try:
        tags_raw = fetch_json('https://mastodon.social/api/v1/trends/tags')
        tags = [t['name'] for t in tags_raw[:12]]
    except Exception:
        pass

    return items, tags

def get_techmeme():
    items = []
    try:
        root = fetch_xml('https://www.techmeme.com/feed.xml')
        for it in root.findall('.//item')[:10]:
            title = it.find('title')
            link = it.find('link')
            desc = it.find('description')
            clean_desc = re.sub(r'<[^>]+>', '', desc.text or '').strip() if desc is not None and desc.text else ''
            items.append({
                'category': 'tech',
                'source': 'Techmeme',
                'title': title.text.strip() if title is not None and title.text else 'Techmeme Brief',
                'description': clean_desc[:130] + '...' if len(clean_desc) > 130 else clean_desc,
                'url': link.text.strip() if link is not None and link.text else 'https://www.techmeme.com',
                'badge': 'Curated Tech',
                'metric': '⚡ Top Industry Story'
            })
    except Exception as e:
        print(f"[!] Techmeme error: {e}", file=sys.stderr)
    return items

def get_bbc_news():
    items = []
    try:
        root = fetch_xml('https://feeds.bbci.co.uk/news/rss.xml')
        for it in root.findall('.//item')[:10]:
            title = it.find('title')
            link = it.find('link')
            desc = it.find('description')
            clean_desc = desc.text.strip() if desc is not None and desc.text else ''
            items.append({
                'category': 'global',
                'source': 'BBC World News',
                'title': title.text.strip() if title is not None and title.text else 'BBC Story',
                'description': clean_desc,
                'url': link.text.strip() if link is not None and link.text else 'https://bbc.com/news',
                'badge': 'Breaking News',
                'metric': '🌐 World Headline'
            })
    except Exception as e:
        print(f"[!] BBC error: {e}", file=sys.stderr)
    return items

def get_wikipedia_top():
    items = []
    try:
        yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime('%Y/%m/%d')
        url = f'https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{yesterday}'
        data = fetch_json(url)
        articles = data.get('items', [{}])[0].get('articles', [])
        for a in articles[:18]:
            raw_title = a.get('article', '')
            if raw_title in ['Main_Page', 'Special:Search', '-', 'Wikipedia:Featured_pictures']:
                continue
            title = raw_title.replace('_', ' ')
            items.append({
                'category': 'global',
                'source': 'Wikipedia Top',
                'title': title,
                'views': a.get('views', 0),
                'url': f"https://en.wikipedia.org/wiki/{raw_title}",
                'badge': 'Knowledge Spike',
                'metric': f"👁️ {a.get('views', 0):,} views"
            })
    except Exception as e:
        print(f"[!] Wikipedia error: {e}", file=sys.stderr)
    return items

def build_snapshot():
    now_utc = datetime.now(timezone.utc)
    timestamp_str = now_utc.strftime('%Y-%m-%d %H:%M UTC')
    date_str = now_utc.strftime('%B %d, %Y')

    print(f"[*] Ingesting global multi-platform signals for {date_str}...")

    g_us = get_google_trends('US')
    g_global = get_google_trends('GB')
    hn = get_hacker_news(15)
    gh = get_github_trending()
    hf = get_huggingface_trending()
    arxiv = get_arxiv_recent()
    crypto, fng = get_crypto_trending()
    fediverse, fedi_tags = get_mastodon_trends()
    techmeme = get_techmeme()
    bbc = get_bbc_news()
    wiki = get_wikipedia_top()

    all_signals = []
    all_signals.extend(g_us)
    all_signals.extend(g_global)
    all_signals.extend(hn)
    all_signals.extend(gh)
    all_signals.extend(hf)
    all_signals.extend(arxiv)
    all_signals.extend(crypto)
    all_signals.extend(fediverse)
    all_signals.extend(techmeme)
    all_signals.extend(bbc)
    all_signals.extend(wiki)

    payload = {
        'generated_at': timestamp_str,
        'date_display': date_str,
        'total_signals': len(all_signals),
        'metrics': {
            'google_trends': len(g_us) + len(g_global),
            'hacker_news': len(hn),
            'github': len(gh),
            'huggingface': len(hf),
            'arxiv': len(arxiv),
            'crypto': len(crypto),
            'fediverse': len(fediverse),
            'techmeme': len(techmeme),
            'bbc_world': len(bbc),
            'wikipedia': len(wiki)
        },
        'sentiment': {
            'fear_and_greed': fng,
            'trending_tags': fedi_tags
        },
        'channels': {
            'search': g_us + g_global,
            'tech': hn + techmeme,
            'dev': gh,
            'ai': hf + arxiv,
            'social': fediverse,
            'finance': crypto,
            'global': bbc + wiki
        },
        'all_signals': all_signals
    }

    out_json = 'C:/Users/udish/gh_workspace/trends/docs/data.json'
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"[✓] Successfully wrote snapshot with {len(all_signals)} items to {out_json}")
    return payload

if __name__ == '__main__':
    build_snapshot()
