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

# Timeframe selection
timeframe = st.selectbox("Select Timeframe:", ["Last 5 minutes", "Last 1 hour", "Last 24 hours"])

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
                "maxResults": 50,
                "key": API_KEY,
            }

            response = requests.get(YOUTUBE_API_URL, params=params)
            data = response.json()

            # Error handling
            if "error" in data:
                st.error(f"❌ API Error: {data['error']['message']}")
            else:
                recent_trends = []
                now = datetime.now(timezone.utc)  # timezone-aware current time

                # Define time thresholds
                time_limits = {
                    "Last 5 minutes": now - timedelta(minutes=5),
                    "Last 1 hour": now - timedelta(hours=1),
                    "Last 24 hours": now - timedelta(hours=24),
                }
                selected_limit = time_limits[timeframe]

                # Process video data
                for item in data.get("items", []):
                    published_at = parser.parse(item["snippet"]["publishedAt"])

                    # Check if video was published after the selected limit
                    if published_at >= selected_limit:
                        recent_trends.append({
                            "title": item["snippet"]["title"],
                            "url": f"https://www.youtube.com/watch?v={item['id']}",
                            "published_at": published_at.strftime("%Y-%m-%d %H:%M:%S UTC"),
                            "channel": item["snippet"]["channelTitle"],
                            "views": item["statistics"].get("viewCount", "N/A"),
                        })

                if recent_trends:
                    st.success(f"🚀 Found {len(recent_trends)} trending videos in the selected timeframe!")
                    for trend in recent_trends:
                        st.markdown(f"""
                        **🎬 Title:** [{trend['title']}]({trend['url']})  
                        🕒 **Published:** {trend['published_at']}  
                        📺 **Channel:** {trend['channel']}  
                        👁️‍🗨️ **Views:** {trend['views']}  
                        ---
                        """)
                else:
                    st.warning(f"⚠️ No trending videos found for the selected timeframe ({timeframe}).")
                    
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {e}")
