import streamlit as st
import requests
from datetime import datetime, timedelta, timezone
from dateutil import parser

# YouTube API Key Input
API_KEY = st.text_input("AIzaSyDE7pUZFUQa200OKUvkbEeEQDCtoNgk7-o:", type="password")

# YouTube API Endpoint
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/videos"

# Input: Country Code
country = st.text_input("Enter Country Code (e.g., US, IN, GB):", value="US")

# Fetch recent trends
if st.button("Track YouTube Trends"):
    if not API_KEY:
        st.error("❌ Please provide a valid YouTube API Key!")
    else:
        try:
            # Fetch trending videos
            params = {
                "part": "snippet,statistics",
                "chart": "mostPopular",
                "regionCode": country,
                "maxResults": 25,
                "key": API_KEY,
            }

            response = requests.get(YOUTUBE_API_URL, params=params)
            data = response.json()

            # Error handling
            if "error" in data:
                st.error(f"❌ API Error: {data['error']['message']}")
            else:
                recent_trends = []
                now = datetime.now(timezone.utc)  # Corrected timezone handling

                for item in data.get("items", []):
                    published_at = parser.parse(item["snippet"]["publishedAt"])

                    # Calculate time difference in minutes
                    time_diff = (now - published_at).total_seconds() / 60

                    # Check if video is published within the last 5 minutes
                    if time_diff <= 5:
                        recent_trends.append({
                            "title": item["snippet"]["title"],
                            "url": f"https://www.youtube.com/watch?v={item['id']}",
                            "published_at": published_at.strftime("%Y-%m-%d %H:%M:%S UTC"),
                            "channel": item["snippet"]["channelTitle"],
                            "views": item["statistics"].get("viewCount", "N/A"),
                        })

                if recent_trends:
                    st.success(f"🚀 Found {len(recent_trends)} trending videos from the last 5 minutes!")
                    for trend in recent_trends:
                        st.markdown(f"""
                        **🎬 Title:** [{trend['title']}]({trend['url']})  
                        🕒 **Published:** {trend['published_at']}  
                        📺 **Channel:** {trend['channel']}  
                        👁️‍🗨️ **Views:** {trend['views']}  
                        ---
                        """)
                else:
                    st.warning("⚠️ No trending videos found from the last 5 minutes.")
                    
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {e}")
