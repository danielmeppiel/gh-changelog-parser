import os
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
                IAM/Permissions (subcategory within DevEx)
                Actions (subcategory within DevEx)
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