💪 RAMbo is ready for action! Will you keep him as a fun chatbot, or turn him into an AI warrior? 🚀🔥

**RAMbo** is a fun, local AI assistant supporting **OpenAI GPT-4**, **Google Gemini**, and **Anthropic Claude**. It maintains conversation context and can also browse & summarize webpages.

## Features

- **Conversation Memory**: Stores your chat history so RAMbo can use context.
- **Multi-Model Support**: Switch between GPT-4, Gemini, or Claude via `config.py`.
- **Browse & Summarize**: Enter a URL, and RAMbo will fetch it with Selenium and provide a summary.

## Table of Contents

1. [Requirements](#requirements)  
2. [Installation](#installation)  
3. [Configuration](#configuration)  
4. [Usage](#usage)  
5. [Switching AI Models](#switching-ai-models)  
6. [Notes & Limitations](#notes--limitations)  
7. [License](#license)

## Requirements

- **Python 3.7+**  
- **Chrome Browser** plus the matching [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)  
- Valid **API keys** (OpenAI, Gemini, or Claude)

## Installation

```bash
git clone https://github.com/YourUsername/RAMbo.git
cd RAMbo
pip install -r requirements.txt
```

## Configuration

1. **Edit `config.py`:**  
   - Paste your API keys into the relevant fields.  
   - By default, `ACTIVE_MODEL = "openai"`.

2. **(Optional)** Add `.gitignore` to exclude `config.py` if you plan on committing.

## Usage

1. **Run the Flask app:**

   ```bash
   python app.py
   ```

2. **Open your browser** and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/).  
   - **Chat**: Type a message and click **Send**. RAMbo will respond, retaining context.  
   - **Browse**: Click **“Try browsing a webpage!”** or go to [http://127.0.0.1:5000/browse](http://127.0.0.1:5000/browse) to summarize a page.

## Switching AI Models

In **`config.py`**:

```python
ACTIVE_MODEL = "openai"  # or "gemini" or "claude"
```

Make sure you have **uncommented** and provided the correct API key for your chosen model.

## Notes & Limitations

- **Session Memory**: If you restart the server or clear your session, the chat history resets.
- **Selenium**: Ensure ChromeDriver matches your local Chrome version.
- **API Costs**: Each query to an external AI may incur usage fees.
- **Security**: Use environment variables or secrets management in production.

## License

[GPLv3 License](LICENSE) – Use, modify, and distribute freely.
