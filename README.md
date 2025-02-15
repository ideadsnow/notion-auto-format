# Notion-Auto-Format

> See also in Chinese: **[中文文档](README.zh.md)**

Notion-Auto-Format is a tool that automatically formats specified Notion documents. It currently supports adding spaces between Chinese and English text, as well as between Chinese and numbers in document titles and bodies.

## Features

- Automatically adds spaces between Chinese and English text.
- Automatically adds spaces between Chinese text and numbers.

## Requirements

- **Python**: Version 3.x
- **Dependencies**:
  - `notion-client`

## Limitations

Due to Notion API rate limits and performance constraints of the editing interface, a maximum of 3 blocks can be modified concurrently by default. If you encounter an editing conflict error, the tool will automatically retry.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ideadsnow/notion-auto-format.git
   ```

2. Navigate to the project directory:
   ```bash
   cd notion-auto-format
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Notion Token**:
   Make sure to manually replace `NOTION_TOKEN = "your_integration_token"` in the code with your own Notion integration token. You can create your integration and obtain the token here: [Create Notion Integration](https://www.notion.so/profile/integrations).

## Usage

To use Notion-Auto-Format, you can check the usage instructions by running:
```bash
python auto_format.py -h
```
The specific usage is:
```bash
usage: auto_format.py [-h] page_id
```


**Where can I find my page's ID?**
> Open the page in Notion. Use the Share menu to Copy link. Now paste the link in your text editor so you can take a closer look. The URL ends in a page ID.
It should be a 32 character long string. Format this value by inserting hyphens (-) in the following pattern: 8-4-4-4-12 (each number is the length of characters between the hyphens).
Example: 1429989fe8ac4effbc8f57f56486db54 becomes 1429989f-e8ac-4eff-bc8f-57f56486db54.
This value is your page ID.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.