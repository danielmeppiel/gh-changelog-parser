import os
import time
import requests

# Load environment variables from a .env file
from dotenv import load_dotenv
load_dotenv()

# Configuration
AZURE_GPT4O_ENDPOINT = os.environ["AZURE_GPT4O_ENDPOINT"]
AZURE_GPT4OMINI_ENDPOINT = os.environ["AZURE_GPT4OMINI_ENDPOINT"]
API_KEY = os.environ["AZURE_API_KEY"]
headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
}

def categorize_changelog(changelog, format="markdown"):
    system_message = '''Taking the following categories and subcategories:
                DevEx
                Security
                AI
            I'll give you one or several product changelog update items that you all have to classify into each of those categories. Never skip classifying an item. If you are not sure where the item should be classified, pick the best guess. Please take into account that "Copilot" and "Content Exclusion" is clearly AI and "Copilot Autofix" and "Secret scanning" is always security related. For each category, order the items by chronological descending order. My next prompt will contain the list you need to order.'''
    
    system_message += 'Print the result in raw {} format.'.format(format)
    if format == "html":
        system_message += 'Ensure each Category title is rendered as an HTML header.'
    
    # Payload for the request
    payload = {
        "messages": [
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": system_message
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": changelog
                }
            ]
            }
        ],
        "temperature": 1,
        "top_p": 1,
        "max_tokens": 4096
    }
    
    # Send request
    try:
        response = requests.post(AZURE_GPT4O_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")

    return response.json()['choices'][0]['message']['content']

def summarize_text(text, limit, limit_type="characters"):
    system_message = f'''Summarize any text I give you to {limit} {limit_type}. 
    Try to capture the essence of the text in the most concise and impactful way. 
    If needed, and to make sure you never go beyond the limit,
    remove information that you consider less important or use widely understood acronyms. 
    Some useful acronyms are: GA for General Availability, PR for Pull Requests, Repo for Repository, 
    GHAS for GitHub Advanced Security, GHE for GitHub Enterprise, GHEC for GitHub Enterprise Cloud,
    JS for JavaScript, TS for TypeScript, Actions for GitHub Actions.
    Generally, a shorter summary is better than a more concise one.
    Do not finish the text with a dot.
    Always choose shorter words that convey the same meaning.'''

    # Payload for the request
    payload = {
        "messages": [
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": system_message
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": text
                }
            ]
            }
        ],
        "temperature": 1,
        "top_p": 1,
        "max_tokens": 4096
    }

    # Send request
    try:
        response = requests.post(AZURE_GPT4OMINI_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
        if isinstance(e, requests.HTTPError) and e.response.status_code == 429:
            print("Received 429 error. Retrying in 60 seconds...")
            time.sleep(60)
            return summarize_text(text, limit, limit_type)
        else:
            raise SystemExit(f"Failed to make the request. Error: {e}")

    return response.json()['choices'][0]['message']['content']