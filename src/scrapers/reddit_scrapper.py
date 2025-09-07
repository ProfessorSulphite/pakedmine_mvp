import praw
from datetime import datetime, timedelta
import hashlib
from src import config

def scrape_r_pakistan(keywords=["education", "school", "university", "exams"], limit=50):
    """
    Scrapes r/Pakistan for posts matching keywords within the last 5 years.
    """
    if not all([config.REDDIT_CLIENT_ID, config.REDDIT_CLIENT_SECRET, config.REDDIT_USER_AGENT]):
        print("Reddit credentials not found. Skipping Reddit scraper.")
        return []

    reddit = praw.Reddit(
        client_id=config.REDDIT_CLIENT_ID,
        client_secret=config.REDDIT_CLIENT_SECRET,
        user_agent=config.REDDIT_USER_AGENT,
    )

    subreddit = reddit.subreddit("pakistan")
    query = " OR ".join(keywords)
    
    records = []
    five_years_ago_ts = (datetime.utcnow() - timedelta(days=5*365)).timestamp()

    print(f"Searching r/Pakistan for: '{query}'")
    for submission in subreddit.search(query, sort="new", time_filter="all", limit=limit):
        # Filter by recency
        if submission.created_utc < five_years_ago_ts:
            continue

        publish_date = datetime.utcfromtimestamp(submission.created_utc)
        url = f"https://www.reddit.com{submission.permalink}"
        record_id = hashlib.sha256((url + publish_date.isoformat()).encode()).hexdigest()

        record = {
            "id": record_id,
            "source": {
                "type": "reddit",
                "site": "reddit.com/r/pakistan",
                "url": url,
                "scrape_ts": datetime.utcnow().isoformat() + "Z"
            },
            "published_date": publish_date.isoformat() + "Z",
            "title": submission.title,
            "text": submission.selftext
        }
        records.append(record)
    
    print(f"Found {len(records)} relevant posts from r/Pakistan.")
    return records