# 🤖 RSS Auto Reader

An AI‑assisted RSS reader that scans arXiv feeds, filters papers by your interests, and sends crisp, structured summaries to Telegram or a Markdown file.

[Features](#-features) •
[Installation](#-installation) •
[Configuration](#-configuration) •
[Usage](#-usage) •

---

## 🌟 Features

- **🎯 Smart filtering**: Classifies entries via abstract analysis against your `INTERESTS` and `EXCLUSIONS`.
- **📄 Auto summarization**: Produces concise, structured summaries (Problems, Core Method, Results, Limitations).
- **📱 Telegram or file output**: Send messages to Telegram or append Markdown to a file.
- **🔗 arXiv‑aware**: Converts arXiv abs links to PDFs automatically for summarization.
- **⚙️ Configurable models**: Set separate selector/summarizer models; optional reasoning setting.
- **🔒 API flexibility**: Works with OpenAI API or API‑compatible endpoints via `API_BASE_URL`.

## 📋 Requirements

- Python 3.8+
- OpenAI API key (env `OPENAI_API_KEY` or in config)
- Telegram Bot token and chat ID (only if using Telegram output)
- Internet connection

## 🚀 Installation

1. Clone and enter the project directory
   ```bash
   git clone https://github.com/yourusername/rss-auto-reader.git
   cd rss-auto-reader
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

You can either edit `config.yaml` directly or create your own file and pass it with `--config my-config.yaml`.

Fill in your API key and model names, set your topics of interest and exclusions, and choose an output method (Telegram or file).

```yaml
# API endpoint (omit to use default OpenAI endpoint)
API_BASE_URL: https://api.openai.com/v1

# Provide here or via env var OPENAI_API_KEY
API_KEY: your_api_key_here

# Models for filtering (selector) and summarization
SELECTOR_MODEL: gpt-5-nano
# Comment out if the model does not support reasoning
SELECTOR_MODEL_REASONING: low

SUMMARIZER_MODEL: gpt-5-mini
# Comment out if the model does not support reasoning
SUMMARIZER_MODEL_REASONING: low

# Telegram output (optional)
TELEGRAM_BOT_TOKEN: your_telegram_bot_token_here
TELEGRAM_CHAT_ID: your_telegram_chat_id_here

# File output (optional; use instead of Telegram)
# OUTPUT_FILE: /absolute/path/to/output.md

# RSS feed to monitor (arXiv example)
RSS:
  feed_url: https://rss.arxiv.org/rss/cs.ai+cs.cl+cs.cv
  name: "ArXiv AI Papers"

# Topic filters
INTERESTS:
  - "LLM Inference"

EXCLUSIONS:
  - "Robots"

# Optional logging level (INFO, DEBUG, WARN, ERROR)
# LOG_LEVEL: INFO
```

## 🎯 Usage

### Basic usage
```bash
# If OPENAI_API_KEY is not in config.yaml, export it here
export OPENAI_API_KEY=sk-...

python main.py
```

### Custom config
```bash
python main.py --config my-config.yaml
```

## 📊 Example Output

```
📄 *Attention Is All You Need*

TL;DR:
❓ Problem: Traditional sequence models rely on recurrence or convolution, limiting parallelization and long-range dependencies.

🛠️ Core Method: Introduces the Transformer architecture using self-attention mechanisms exclusively. Multi-head attention processes sequences in parallel while positional encoding maintains sequence order information.

📈 Main Results/Impact: Achieves state-of-the-art BLEU scores on translation tasks (28.4 on WMT 2014 En-De) with significantly reduced training time and better parallelization.

⚠️ Limitation: Requires large amounts of training data and computational resources. Memory usage scales quadratically with sequence length.

🔗 [Read more](https://arxiv.org/abs/1706.03762)
```

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and research purposes. Please ensure you comply with:
- OpenAI's usage policies
- arXiv's terms of service  
- Telegram's bot guidelines
- Respect rate limits and fair usage

## ℹ️ Notes & limits

- Summarization downloads the arXiv PDF and skips files larger than ~10 MB.
- Telegram output requires both `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`; otherwise configure `OUTPUT_FILE`.
- Model names in examples are placeholders; use any supported model ID from your provider.
- `API_BASE_URL` allows usage of API‑compatible endpoints; leave it unset for the default OpenAI API.
