from utils.yaml_helper import YAMLHelper
from utils.rss_helper import RSSFeedHelper
from utils.openai_helper import OpenAIHelper
from argparse import ArgumentParser
from logging import basicConfig, INFO, DEBUG, getLogger, ERROR, WARN
import requests

logger = getLogger(__name__)

def summarize_selected_paper(config, entry):
    summarizer = OpenAIHelper(api_key=config.data.get("API_KEY", ""), model=config.data.get("SUMMARIZER_MODEL", "gpt-5-mini"), api_base_url=config.data.get("API_BASE_URL", None))
    link = entry.get("link", "")
    if not link:
        logger.warning("No link found for entry.")
        return

    link = link.replace("https://arxiv.org/abs/", "https://arxiv.org/pdf/") + ".pdf"
    file_size = int(requests.head(link, allow_redirects=True).headers.get("Content-Length", 0))
    if file_size / (1024 * 1024) > 10:
        # TODO: use file upload method to get rid of the limitation
        logger.warning(f"File size is {file_size / (1024 * 1024):.2f} MB, no summary will be generated.")
        return
    logger.info(f"Summarizing paper: {entry['title']} from {link}")
    summary = summarizer.summarize_paper(link)
    logger.debug(f"Summary for {entry['title']}: {summary}")

    return summary

def send_message_to_telegram(config, text):
    telegram_bot_token = config.data.get("TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id = config.data.get("TELEGRAM_CHAT_ID", "")
    if not telegram_bot_token or not telegram_chat_id:
        logger.warning("Telegram bot token or chat ID is not set.")
        return

    # Send message to Telegram
    telegram_api_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {
        "chat_id": telegram_chat_id,
        "text": text
    }
    response = requests.post(telegram_api_url, json=payload)
    if response.status_code == 200:
        logger.info("Message sent to Telegram successfully.")
    else:
        logger.error(f"Failed to send message to Telegram: {response.text}")


def main():
    parser = ArgumentParser(description="RSS Auto Reader")
    parser.add_argument("--config", default="config.yaml", help="Path to the config file")
    # parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    # Load configuration
    config = YAMLHelper(args.config)
    log_level = config.data.get("LOG_LEVEL", INFO)
    basicConfig(level=log_level)

    rss_helper = RSSFeedHelper()
    rss_url = config.data.get("RSS", {}).get("feed_url", "")
    logger.info(f"Using RSS feed URL: {rss_url}")

    # Process RSS feed
    try:
        result = rss_helper.process_feed(rss_url)
        logger.info(f"Successfully fetched RSS feed: {result['feed_info']['title']}")
    except Exception as e:
        logger.error(f"Error fetching RSS feed: {e}")
        return
    logger.info(f"Fetched {len(result['entries'])} entries from the feed.")

    subject_analyzer = OpenAIHelper(api_key=config.data.get("API_KEY", ""), model=config.data.get("SELECTOR_MODEL", "gpt-5-nano"), api_base_url=config.data.get("API_BASE_URL", None))

    for entry in result['entries']:
        is_relevant = subject_analyzer.analyze_subject_from_abstract(
            entry['content'], config.data.get("Interests", [])
        )

        if is_relevant:
            logger.info(f"Relevant entry found: {entry['title']}")
            summary = summarize_selected_paper(config, entry)
            if summary:
                message = f"📄 *{entry['title']}*\n\n{summary}\n\n🔗 [Read more]({entry['link']})"
                send_message_to_telegram(config, message)
            else:
                message = f"📄 *{entry['title']}*\n\nThis is the abstract:\n\n{entry['content']}\n\n🔗 [Read more]({entry['link']})"
                send_message_to_telegram(config, message)
                logger.info(f"No summary available for entry: {entry['title']}")
        else:
            logger.debug(f"Ignoring entry: {entry['title']}")

if __name__ == "__main__":
    main()