import requests
import argparse
from bs4 import BeautifulSoup
from datetime import datetime
import os
from datetime import datetime, timedelta
from categorizer import categorize_changelog

land = "DevEx"
secure = "Security"
accelerate = "AI"

class Article:
    def __init__(self, title, link, published, summary):
        self.title = title
        self.link = link
        self.published = published
        self.summary = summary
        self.category = None

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

def parse_entry(entry):
    title = entry.find('a', class_='Link--primary').text.strip()
    link = entry.find('a', class_='Link--primary')['href']
    published = entry.find('time')['datetime']
    summary = entry.find('div', class_='changelog-single-content').text.strip()
    return Article(title, link, published, summary)

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
            article = parse_entry(entry)
            published_date = datetime.strptime(article.published, '%Y-%m-%d')
            if published_date < stop_date:
                return articles
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

def write_articles_to_markdown(articles, do_categorize, output_file):
    markdown_content = ""
    for article in articles:
        markdown_content += f"- {article.to_markdown()}\n"
    if do_categorize:
        # Call the categorizer to categorize the changelog
        markdown_content = categorize_changelog(markdown_content, "markdown")
        # Strip the first and last lines to remove the raw markdown formatting
        markdown_lines = markdown_content.splitlines()[1:-1]
        markdown_content = "\n".join(markdown_lines) + "\n"
    # Write the markdown content to the file
    with open(output_file, 'w') as file:
        file.write(markdown_content)

def write_articles_to_html(articles, do_categorize, output_file):
    html_content = ""
    for article in articles:
        html_content += f'<p>- {article.to_html()}</p>\n'
    if do_categorize:
        # Call the categorizer to categorize the changelog
        html_content = categorize_changelog(html_content, "html")
        # Strip the first and last lines to remove the raw html formatting
        html_lines = html_content.splitlines()[1:-1]
        # Wrap the content with <html> tags
        html_content = "\n".join(html_lines) + "\n"
    html_content = "<html>\n" + html_content + "</html>"
    # Write the html content to the file
    with open(output_file, 'w') as file:
        file.write(html_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch and parse GitHub changelog.")
    parser.add_argument('--days', type=int, default=90, help='Number of days to look back from today (default: 90)')
    parser.add_argument('--format', type=str, default='md', help='Output format (md or html)')
    parser.add_argument('-c', action='store_true', help='Use AI to categorize the changelog items per product area (DevEx, Security, AI)')
    args = parser.parse_args()
    do_categorize = args.c

    changelog_url = "https://github.blog/changelog/"
    # Obtain the stop date as the specified number of days older than today
    stop_date = (datetime.now() - timedelta(days=args.days)).strftime('%Y-%m-%d')
    articles = fetch_and_parse_changelog(changelog_url, stop_date)
    
    current_path = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(current_path, "changelog." + args.format)

    if args.format == 'md':
        write_articles_to_markdown(articles, do_categorize, output_file)
    elif args.format == 'html':
        write_articles_to_html(articles, do_categorize, output_file)
    else:
        print("Invalid format specified.")