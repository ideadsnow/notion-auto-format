# Notion-Auto-Format

| See also in Chinese: **[中文文档](README.zh.md)**

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
   cd Notion-Auto-Format
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Notion Token**:
   Make sure to manually replace `NOTION_TOKEN = "your_integration_token"` in the code with your own Notion integration token. You can create your integration and obtain the token at this address: [Create Notion Integration](https://www.notion.so/profile/integrations).

## Usage

To use Notion-Auto-Format, you can check the usage instructions by running:
```bash
python format_notion.py -h
```
The specific usage is:
```bash
usage: format_notion.py [-h] page_id
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.