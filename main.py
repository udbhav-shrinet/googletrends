"""
Google Trends Automated Analytics & Extraction Engine
Automated data pipeline for multi-region keyword interest extraction and comparative trend analysis.
"""

import argparse
import sys
import json
import pandas as pd
from datetime import datetime

try:
    from pytrends.request import TrendReq
except ImportError:
    TrendReq = None

def fetch_trends(keywords, timeframe='today 12-m', geo='', category=0):
    if not TrendReq:
        print("[ERROR] pytrends is not installed. Run 'pip install -r requirements.txt'")
        return None
    
    print(f"[*] Initializing Google Trends connection for keywords: {keywords}")
    pytrend = TrendReq(hl='en-US', tz=360, timeout=(10, 25))
    pytrend.build_payload(kw_list=keywords, cat=category, timeframe=timeframe, geo=geo)
    
    df_iot = pytrend.interest_over_time()
    if df_iot.empty:
        print("[!] No interest over time data returned.")
    else:
        print(f"[+] Successfully extracted {len(df_iot)} historical time points.")
        
    df_region = pytrend.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
    
    return {
        "interest_over_time": df_iot,
        "interest_by_region": df_region
    }

def export_data(data_dict, prefix="trends_output"):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    if data_dict.get("interest_over_time") is not None and not data_dict["interest_over_time"].empty:
        csv_file = f"{prefix}_time_{ts}.csv"
        data_dict["interest_over_time"].to_csv(csv_file)
        print(f"[+] Exported time series to {csv_file}")
        
    if data_dict.get("interest_by_region") is not None and not data_dict["interest_by_region"].empty:
        csv_reg = f"{prefix}_region_{ts}.csv"
        data_dict["interest_by_region"].to_csv(csv_reg)
        print(f"[+] Exported regional data to {csv_reg}")

def main():
    parser = argparse.ArgumentParser(description="Google Trends Automated Analytics & Extraction Engine")
    parser.add_argument("-k", "--keywords", nargs="+", default=["Python", "JavaScript", "Rust"], help="Keywords to compare (max 5)")
    parser.add_argument("-t", "--timeframe", default="today 12-m", help="Timeframe (e.g., 'today 1-m', 'today 12-m', 'today 5-y')")
    parser.add_argument("-g", "--geo", default="", help="Two-letter country code (e.g., 'US', 'GB', 'IN', or empty for global)")
    parser.add_argument("-o", "--export", action="store_true", help="Export extracted metrics to CSV files")
    
    args = parser.parse_args()
    results = fetch_trends(keywords=args.keywords[:5], timeframe=args.timeframe, geo=args.geo)
    if results and args.export:
        export_data(results)

if __name__ == "__main__":
    main()
