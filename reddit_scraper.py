import praw
import os
from dotenv import load_dotenv
import pandas as pd
import re

# Load Reddit credentials
load_dotenv()
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# Top 10 relationship terms
relationship_terms = [
    "brother", "son", "partner", "boyfriend", "husband",
    "friend", "nephew", "coworker", "roommate", "neighbour", "neighbor"
]

# Subreddits to scan
subreddits = [
    "TrueOffMyChest", "relationship_advice", "AskReddit", "AmItheAsshole", "AITAH",
    "advice", "AITA_Relationships", "AmIOverreacting", "QAnonCasualties", "confessions",
    "LifeAdvice", "Vent", "incelexit", "helpme", "family", "abusiverelationships"
]

# Prep
collected_posts = []
max_total_posts = 500

print("🔍 Scanning Reddit...")

for subreddit_name in subreddits:
    print(f"📂 Checking r/{subreddit_name}...")
    subreddit = reddit.subreddit(subreddit_name)

    try:
        for post in subreddit.new(limit=100):  # Adjust if needed
            title = post.title.lower()
            if any(term in title for term in relationship_terms):
                collected_posts.append({
                    "subreddit": subreddit_name,
                    "title": post.title.strip(),
                    "url": f"https://www.reddit.com{post.permalink}",
                    "created_utc": post.created_utc
                })
                if len(collected_posts) >= max_total_posts:
                    break
        if len(collected_posts) >= max_total_posts:
            break
    except Exception as e:
        print(f"⚠️ Skipped r/{subreddit_name} due to error: {e}")

# Save to CSV
df = pd.DataFrame(collected_posts)
df.to_csv("relationship_posts.csv", index=False)
print(f"\n✅ Done! {len(collected_posts)} posts saved to 'relationship_posts.csv'")