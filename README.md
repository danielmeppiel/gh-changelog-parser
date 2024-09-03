# GitHub Changelog Parser

## Overview

This script is designed to fetch and parse the GitHub changelog from the [GitHub Changelog](https://github.blog/changelog/) website. It extracts relevant information such as the title, link, published date, and summary of each changelog entry and saves this information in both Markdown and HTML formats. The script allows users to specify the number of days to look back from today to filter the changelog entries.

## Why It Is Useful

- **Automated Changelog Extraction**: Automates the process of fetching and parsing changelog entries from GitHub, saving time and effort.
- **Customizable Time Frame**: Allows users to specify the number of days to look back, making it flexible to fetch recent or older changelog entries.
- **Multiple Output Formats**: Saves the extracted changelog entries in both Markdown and HTML formats, making it easy to integrate with various documentation tools and platforms.
- **Easy Integration**: Can be integrated into CI/CD pipelines to keep track of changes and updates in GitHub.

## How to Use

### Prerequisites

Ensure you have the required libraries installed:
```sh
pipenv install
```

### Running the Script
1. **Default Usage (Last 90 Days)**
   ```sh
   pipenv run python parser-web.py
    ```
    This will fetch the changelog entries from the last 90 days and save the extracted information in both Markdown and HTML formats.
2. **Custom Time Frame**  
   ```sh
   pipenv run python parser-web.py --days 60
    ```
    This will fetch and parse the changelog entries from the last 60 days and save them in `changelog.md` and `changelog.html` files.

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