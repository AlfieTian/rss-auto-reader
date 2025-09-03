# 🤖 RSS Auto Reader

*An intelligent RSS feed reader that automatically filters, summarizes, and delivers relevant academic papers to your Telegram*

[Features](#-features) •
[Installation](#-installation) •
[Configuration](#-configuration) •
[Usage](#-usage) •

---

## 🌟 Features

- **🎯 Smart Filtering**: Uses AI to analyze paper abstracts and filter content based on your research interests
- **📄 Automatic Summarization**: Generates concise, structured summaries of relevant papers using OpenAI's latest models
- **📱 Telegram Integration**: Delivers summaries directly to your Telegram chat with formatted messages
- **🔗 arXiv Support**: Optimized for arXiv RSS feeds with direct PDF processing
- **⚡ Configurable Models**: Choose between different OpenAI models for content filtering and summarization

## 📋 Requirements

- Python 3.8+
- OpenAI API Key
- ~~Telegram Bot Token~~(Optional now)
- Internet connection

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/rss-auto-reader.git
   cd rss-auto-reader
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

1. **Copy and edit the configuration file**
   ```bash
   cp config.yaml.example config.yaml
   ```

2. **Update `config.yaml`**
   
   Fill in your API key and model name, and specify any subjects you’re interested in or want to exclude. You can choose to send the summary to a Telegram bot or save it to a Markdown file.

   ```yaml
   API_BASE_URL: https://api.openai.com/v1
   API_KEY: your_api_key_here
   SELECTOR_MODEL: gpt-5-nano
   # Comment the following line if the model is not capable of reasoning
   SELECTOR_MODEL_REASONING: low
   SUMMARIZER_MODEL: gpt-5-mini
   # Comment the following line if the model is not capable of reasoning
   SUMMARIZER_MODEL_REASONING: low
   TELEGRAM_BOT_TOKEN: your_telegram_bot_token_here
   TELEGRAM_CHAT_ID: your_telegram_chat_id_here
   # Uncomment the following line and comment the two above to enable file output
   # OUTPUT_FILE: /path/to/your/output/file.txt
   RSS:
      feed_url: https://rss.arxiv.org/rss/cs.ai+cs.cl+cs.cv
      name: "Arxiv AI Papers"
   INTERESTS:
   - "LLM Inference"

   EXCLUSIONS:
   - "Robots"
   ```

## 🎯 Usage

### Basic Usage
```bash
python main.py
```

### Options
```bash
# Use custom config file
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
