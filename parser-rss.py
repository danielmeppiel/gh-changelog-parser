import feedparser
import requests

def fetch_and_parse_rss_feed(url):
    # Fetch the RSS feed
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Parse the RSS feed
    feed = feedparser.parse(response.content)

    # Extract and print relevant information
    for entry in feed.entries:
        print(f"Title: {entry.title}")
        print(f"Link: {entry.link}")
        print(f"Published: {entry.published}")
        print(f"Summary: {entry.summary}")
        print("-" * 40)

if __name__ == "__main__":
    rss_feed_url = "https://github.blog/changelog/label/copilot/feed/"
    fetch_and_parse_rss_feed(rss_feed_url)