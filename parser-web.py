import requests
import argparse
from bs4 import BeautifulSoup
from datetime import datetime
import os
from datetime import datetime, timedelta

land = "DevEx"
secure = "Security"
accelerate = "AI"

class Article:
    def __init__(self, title, link, published, summary):
        self.title = title
        self.link = link
        self.published = published
        self.summary = summary

    def to_markdown(self):
        return f"({self.published}) [{self.title}]({self.link})"
    
    def to_html(self):
        return f'({self.published}) <a href="{self.link}">{self.title}</a>'

    def __str__(self):
        return (f"Title: {self.title}\n"
                f"Link: {self.link}\n"
                f"Published: {self.published}\n"
                f"Summary: {self.summary}\n"
                + "-" * 40)

def fetch_and_parse_changelog(url, stop_date):
    page = 1
    stop_date = datetime.strptime(stop_date, '%Y-%m-%d')
    articles = []

    while True:
        # Construct the URL for the current page
        page_url = f"{url}page/{page}/"
        
        # Fetch the webpage content
        response = requests.get(page_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract and store relevant information
        entries = soup.find_all('article')
        if not entries:
            break

        for entry in entries:
            title = entry.find('a', class_='Link--primary').text.strip()
            link = entry.find('a', class_='Link--primary')['href']
            published = entry.find('time')['datetime']
            published_date = datetime.strptime(published, '%Y-%m-%d')
            summary = entry.find('div', class_='changelog-single-content').text.strip()

            if published_date < stop_date:
                return articles

            article = Article(title, link, published, summary)
            articles.append(article)

        page += 1

def parse_categories(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    category_div = soup.find('div', class_='changelog-category-dropdown-content')
    if category_div:
        categories = [a.text.strip() for a in category_div.find_all('a')]
        for category in categories:
            print(category)
    else:
        print("No categories found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch and parse GitHub changelog.")
    parser.add_argument('--days', type=int, default=90, help='Number of days to look back from today (default: 90)')
    args = parser.parse_args()

    changelog_url = "https://github.blog/changelog/"
    # Obtain the stop date as the specified number of days older than today
    stop_date = (datetime.now() - timedelta(days=args.days)).strftime('%Y-%m-%d')
    articles = fetch_and_parse_changelog(changelog_url, stop_date)
    
    current_path = os.path.dirname(os.path.abspath(__file__))
    output_md_file = os.path.join(current_path, "changelog.md")
    output_html_file = os.path.join(current_path, "changelog.html")

    with open(output_md_file, 'w') as file:
        for article in articles:
            file.write(f"- {article.to_markdown()}\n")

    with open(output_html_file, 'w') as file:
        for article in articles:
            file.write(f'<p>- {article.to_html()}</p>\n')