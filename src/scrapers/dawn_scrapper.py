import requests
from bs4 import BeautifulSoup
from newspaper import Article
import hashlib
import time
from datetime import datetime, timedelta

def scrape_dawn_article(url):
    """
    Scrapes a single article from dawn.com, extracts key information,
    and checks if it was published within the last 5 years.
    """
    try:
        headers = {'User-Agent': 'PakEdMine/0.1'}
        # Using newspaper3k for robust article parsing
        article = Article(url)
        article.download(headers=headers)
        article.parse()

        publish_date = article.publish_date
        if not publish_date:
            return None # Skip if no date found

        # Filter by recency (<= 5 years)
        five_years_ago = datetime.now(publish_date.tzinfo) - timedelta(days=5*365)
        if publish_date < five_years_ago:
            print(f"Skipping old article: {url}")
            return None

        # Generate a unique ID
        record_id = hashlib.sha256((url + publish_date.isoformat()).encode()).hexdigest()

        canonical_record = {
            "id": record_id,
            "source": {
                "type": "news",
                "site": "dawn.com",
                "url": url,
                "scrape_ts": datetime.utcnow().isoformat() + "Z"
            },
            "published_date": publish_date.isoformat() + "Z",
            "title": article.title,
            "text": article.text
            # 'language' and other fields to be added in NLP stage
        }
        return canonical_record

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None