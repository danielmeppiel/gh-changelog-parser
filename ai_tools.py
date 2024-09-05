import os
import time
from azure.core.exceptions import HttpResponseError
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage
from azure.ai.inference.models import UserMessage
from azure.core.credentials import AzureKeyCredential

# Load environment variables from a .env file
from dotenv import load_dotenv
load_dotenv()

# To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings. 
# Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
client = ChatCompletionsClient(
    endpoint="https://models.inference.ai.azure.com",
    credential=AzureKeyCredential(os.environ["GITHUB_TOKEN"]),
)

def categorize_changelog(changelog, format="markdown"):
    system_message = '''Taking the following categories and subcategories:
                DevEx
                Security
                AI
            I'll give you one or several product changelog update items that you all have to classify into each of those categories. Never skip classifying an item. If you are not sure where the item should be classified, pick the best guess. Please take into account that "Copilot" and "Content Exclusion" is clearly AI and "Copilot Autofix" and "Secret scanning" is always security related. For each category, order the items by chronological descending order. My next prompt will contain the list you need to order.'''
    
    system_message += 'Print the result in raw {} format.'.format(format)
    if format == "html":
        system_message += 'Ensure each Category title is rendered as an HTML header.'
    
    response = client.complete(
        messages=[
            SystemMessage(content=system_message),
            UserMessage(content=changelog),
        ],
        model="gpt-4o",
        temperature=1,
        max_tokens=4096,
        top_p=1
    )

    return response.choices[0].message.content

def summarize_text(text, limit, limit_type="characters"):
    system_message = f'''Summarize any text I give you to {limit} {limit_type}. 
    Try to capture the essence of the text in the most concise and impactful way. 
    If needed, and to make sure you never go beyond the limit,
    remove information that you consider less important or use widely understood acronyms.
    Generally, a shorter summary is better than a more concise one.'''

    try:
        response = client.complete(
            messages=[
                SystemMessage(content=system_message),
                UserMessage(content=text),
            ],
            model="gpt-4o-mini",
            temperature=1,
            max_tokens=4096,
            top_p=1
        )
    except HttpResponseError as e:
        if e.status_code == 429:  # Rate limit error
            print("Rate limit reached. Waiting for 45 seconds before retrying...")
            time.sleep(45)
            response = client.complete(
                messages=[
                    SystemMessage(content=system_message),
                    UserMessage(content=text),
                ],
                model="gpt-4o-mini",
                temperature=1,
                max_tokens=4096,
                top_p=1
            )
        else:
            raise

    return response.choices[0].message.content