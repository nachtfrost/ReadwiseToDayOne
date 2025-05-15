# Readwise to Day One

Automatically import your daily Readwise highlights into Day One journal with proper formatting and images.

## Features

- Fetches all highlights created today from your Readwise account
- Creates beautifully formatted Day One entries
- Preserves metadata (author, source, URL, etc.)
- Includes cover images
- Supports custom emoji mappings for tags
- Groups highlights by source
- Maintains original formatting and structure

## Prerequisites

- Python 3.6 or higher
- Day One CLI (for macOS)
- Readwise API token
- Day One installed on your Mac

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/nachtfrost/ReadwiseToDayOne.git
   cd readwise-to-dayone
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Install Day One CLI if you haven't already:
   - Installation instructions: https://dayoneapp.com/downloads/dayone-cli.pkg
   - Run the shell script mentioned on the page
   - Verify installation by running `dayone2 --version`

4. Create a `.env` file with your configuration:
   ```
   READWISE_TOKEN=your_readwise_token_here
   DAYONE_JOURNAL_PATH=/path/to/your/journal.dayone  # Optional
   ```

   To get your Readwise token:
   1. Go to https://readwise.io/access_token
   2. Copy your token

## Usage

Simply run the script:
```bash
python readwise_to_dayone.py
```

The script will:
1. Fetch all highlights created today from Readwise
2. Format them with proper metadata and structure
3. Include cover images as attachments
4. Create entries in Day One

## Output Format

Each Day One entry will be formatted as follows:

```markdown
# Article/Book Title

## Metadata
Author: Author Name
Category: articles/books
Source: source_name
URL: source_url

Summary: Article/book summary

Cover Image:
[{attachment}]

## Highlights

> Highlight text

Tags: 💡 Inspiration 🤖 AI

Note: Any notes added to the highlight
```

## Tag Emoji Mapping

The script includes emoji mappings for common tags:
- inspiration -> 💡 Inspiration
- ai -> 🤖 AI
- insight -> 🤔 Insight

You can customize these mappings in the `tag_emoji_map` dictionary in the script.

## Error Handling

The script includes comprehensive error handling for:
- Missing API tokens
- Failed API requests
- Network issues
- File system operations
- Day One CLI integration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to Readwise for their excellent API
- Thanks to Day One for their CLI tool
- Inspired by the need to maintain a clean journal of daily readings 