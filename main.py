# Import necessary libraries
from pytrends.request import TrendReq
import pandas as pd
import time

# Initialize pytrends
pytrends = TrendReq(hl='en-US', tz=330)

# Fetch top 20 trending searches in India
trending_searches_df = pytrends.trending_searches(pn='india')
top_20_trends = trending_searches_df.head(20)[0].tolist()  # Convert to list of trend topics

# Prepare a list to store all data
all_data = []

# Loop through each trend and get interest by region for Indian states
for trend in top_20_trends:
    # Build the payload with the current trend
    pytrends.build_payload([trend], geo='IN')
    
    # Fetch interest by region data
    interest_by_region_df = pytrends.interest_by_region(resolution='region')
    
    # Filter only non-zero states (indicating search interest in India)
    interest_by_region_df = interest_by_region_df[interest_by_region_df[trend] > 0]
    interest_by_region_df = interest_by_region_df.sort_values(by=trend, ascending=False)
    
    # Store data with the specified format
    for j, (region, interest) in enumerate(interest_by_region_df[trend].items(), start=1):
        # Append each entry with the trend name, region, and interest score
        all_data.append([trend, region, interest])
    
    # Sleep to avoid rate limiting by Google
    time.sleep(1)

# Convert all data to a DataFrame
df = pd.DataFrame(all_data, columns=["Trend", "Region", "Interest"])

# Save DataFrame to an Excel file
df.to_excel("Top_20_Trends_Interest_by_Region.xlsx", index=False)

print("Data saved to Top_20_Trends_Interest_by_Region.xlsx")
