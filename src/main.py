import json
from scrapers.dawn_scraper import scrape_dawn_article
from scrapers.reddit_scraper import scrape_r_pakistan

def main():
    """
    Main function to orchestrate the scraping process.
    """
    all_records = []

    # --- Reddit Scraper ---
    # Scrapes r/Pakistan based on a keyword search
    reddit_records = scrape_r_pakistan(keywords=["education", "student frustration", "school fees", "university crisis"], limit=20)
    all_records.extend(reddit_records)

    # --- Dawn Scraper ---
    # In a real scenario, you'd have a list of URLs from a sitemap or RSS feed.
    # For this example, we use a few recent, relevant articles.
    dawn_urls = [
        "https://www.dawn.com/news/1814917/a-failing-grade",
        "https://www.dawn.com/news/1795777/the-problem-with-our-education-system",
        "https://www.dawn.com/news/1776510"
    ]
    
    for url in dawn_urls:
        print(f"Scraping Dawn URL: {url}")
        dawn_record = scrape_dawn_article(url)
        if dawn_record:
            all_records.append(dawn_record)

    # --- Save Output ---
    output_filename = "crawled_data.jsonl"
    with open(output_filename, 'w', encoding='utf-8') as f:
        for record in all_records:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')

    print(f"\nScraping complete. Saved {len(all_records)} records to {output_filename}.")


if __name__ == "__main__":
    main()