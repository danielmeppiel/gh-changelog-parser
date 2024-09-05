# GitHub Changelog Parser

- [GitHub Changelog Parser](#github-changelog-parser)
  - [Overview](#overview)
  - [Why It Is Useful](#why-it-is-useful)
  - [How to Use](#how-to-use)
    - [Prerequisites](#prerequisites)
    - [Running the Script](#running-the-script)
      - [HTML (`changelog.html`)](#html-changeloghtml)
  - [AI-powered Categorization](#ai-powered-categorization)
    - [Prerequisites for AI Categorization](#prerequisites-for-ai-categorization)
    - [Running with AI Categorization](#running-with-ai-categorization)


## Overview

This script is designed to fetch and parse the [GitHub Changelog](https://github.blog/changelog/) website. It extracts relevant information such as the title, link, published date, and summary of each changelog entry and saves this information in both Markdown and HTML formats. The script allows users to specify the number of days to look back from today to filter the changelog entries. It also allows you to use AI to automatically categorize the changelog items per product area (DevEx, Security, AI).

## Why It Is Useful

- **Automated Changelog Extraction**: Automates the process of fetching and parsing changelog entries from GitHub, saving time and effort.
- **Customizable Time Frame**: Allows users to specify the number of days to look back, making it flexible to fetch recent or older changelog entries.
- **Multiple Output Formats**: Saves the extracted changelog entries in both Markdown and HTML formats, making it easy to integrate with various documentation tools and platforms.
- **Easy Integration**: Can be integrated into CI/CD pipelines to keep track of changes and updates in GitHub.

## How to Use

### Prerequisites

   To install `pipenv`, a Python package manager, follow these steps on macOS:
   ```sh
   brew install pipenv
   ```

   Then, ensure you have the required libraries installed:
   ```sh
   pipenv install
   ```

### Running the Script
1. **Default Usage (Last 90 Days in Markdown)**
   ```sh
   pipenv run python parser_web.py
    ```
    This will fetch the changelog entries from the last 90 days and save the extracted information in Markdown format in a `changelog.md` file.
2. **Custom Time Frame**  
   ```sh
   pipenv run python parser_web.py --days 60
    ```
    This will fetch and parse the changelog entries from the last 60 days and save them in a `changelog.md` file.
3. **HTML Format**  
   ```sh
   pipenv run python parser_web.py --format html
    ```
    This will fetch and parse the changelog entries from the last 90 days and save them in HTML format in a `changelog.html` file.

### Output Files

- `changelog.md`: Contains the changelog entries in Markdown format.
- `changelog.html`: Contains the changelog entries in HTML format.

### Example Output

#### Markdown (`changelog.md`)

```markdown
- (2024-08-29) [Add repository permissions to custom organization roles](https://github.blog/changelog/2024-08-29-add-repository-permissions-to-custom-organization-roles)
- (2024-08-29) [Unkey is now a GitHub secret scanning partner](https://github.blog/changelog/2024-08-29-unkey-is-now-a-github-secret-scanning-partner)
- (2024-08-29) [Secret scanning fine-grained permissions for bypasses](https://github.blog/changelog/2024-08-29-secret-scanning-fine-grained-permissions-for-bypasses)
```
#### HTML (`changelog.html`)

```html
<p>- (2024-08-29) <a href="https://github.blog/changelog/2024-08-29-add-repository-permissions-to-custom-organization-roles">Add repository permissions to custom organization roles</a></p>
<p>- (2024-08-29) <a href="https://github.blog/changelog/2024-08-29-unkey-is-now-a-github-secret-scanning-partner">Unkey is now a GitHub secret scanning partner</a></p>
<p>- (2024-08-29) <a href="https://github.blog/changelog/2024-08-29-secret-scanning-fine-grained-permissions-for-bypasses">Secret scanning fine-grained permissions for bypasses</a></p>
```

## AI-powered Categorization
You can use AI to automatically categorize the changelog items per product area (DevEx, Security, AI).

### Prerequisites for AI Categorization

**Create a [`.env`](https://github.com/danielmeppiel/gh-changelog-parser/.env) File**:
   Create a [`.env`](https://github.com/danielmeppiel/gh-changelog-parser/.env) file within the repository and add a line with your GitHub token. This token should be created in GitHub with no scopes and no permissions.
   ```sh
   echo "GITHUB_TOKEN=your_github_token_here" > .env
   ```

   To create a GitHub token:
   - Go to your GitHub settings.
   - Navigate to "Developer settings" > "Personal access tokens".
   - Click "Generate new token".
   - Ensure the token has no scopes and no permissions.

### Running with AI Categorization

This feature can be enabled by using the `-c` flag when running the script:

```sh
pipenv run python parser_web.py -c
```

It uses [GitHub Models](https://docs.github.com/en/github-models) to categorize the changelog items with GPT-4o. The output will look something like this:

```markdown
## DevEx
- (2024-08-29) [GitHub Enterprise Server 3.14 is generally available](https://github.blog/changelog/2024-08-29-github-enterprise-server-3-14-is-generally-available)
- (2024-08-29) [What’s New in GitHub Sponsors](https://github.blog/changelog/2024-08-29-whats-new-in-github-sponsors)
- (2024-08-29) [Add repository permissions to custom organization roles](https://github.blog/changelog/2024-08-29-add-repository-permissions-to-custom-organization-roles)

## Security
- (2024-08-29) [Unkey is now a GitHub secret scanning partner](https://github.blog/changelog/2024-08-29-unkey-is-now-a-github-secret-scanning-partner)
- (2024-08-29) [Secret scanning fine-grained permissions for bypasses](https://github.blog/changelog/2024-08-29-secret-scanning-fine-grained-permissions-for-bypasses)
- (2024-08-28) [CodeQL code scanning can analyze Java and C# codebases without needing a build (GA)](https://github.blog/changelog/2024-08-28-codeql-code-scanning-can-analyze-java-and-c-codebases-without-needing-a-build-ga)

## AI
- (2024-08-29) [Copilot Chat in GitHub.com now can search across GitHub entities](https://github.blog/changelog/2024-08-29-copilot-chat-in-github-com-now-can-search-across-github-entities)
- (2024-08-27) [Custom models for GitHub Copilot are now in Limited Public Beta](https://github.blog/changelog/2024-08-27-custom-models-for-github-copilot-are-now-in-limited-public-beta)
```

Please be aware that categorization is not perfect and may require manual intervention to correct mistakes of the AI. You can tweak the categories in the System Message at `ai_tools.py:20`. 
