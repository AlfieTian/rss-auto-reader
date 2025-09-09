import requests
import json
from typing import Optional, Dict, List, Union
import time
import logging


class TelegramBotHelper:
    def __init__(self, bot_token: str):
        if not bot_token:
            raise ValueError("Bot token is required")
        
        self.bot_token = bot_token
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
        self.logger = logging.getLogger(__name__)
    
    def send_message(
        self, 
        chat_id: Union[str, int], 
        text: str, 
        parse_mode: Optional[str] = None,
        disable_web_page_preview: bool = False,
        disable_notification: bool = False,
        reply_to_message_id: Optional[int] = None
    ) -> Dict:
        """Send a text message to a chat"""
        url = f"{self.base_url}/sendMessage"
        
        payload = {
            "chat_id": chat_id,
            "text": text,
            "disable_web_page_preview": disable_web_page_preview,
            "disable_notification": disable_notification
        }
        
        if parse_mode:
            payload["parse_mode"] = parse_mode
        
        if reply_to_message_id:
            payload["reply_to_message_id"] = reply_to_message_id
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 400:
                raise Exception(f"Bad Request: {response.text}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Failed to send message: {e}")
            raise Exception(f"Failed to send message: {e}")
    
    def send_photo(
        self, 
        chat_id: Union[str, int], 
        photo: str, 
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None
    ) -> Dict:
        """Send a photo to a chat"""
        url = f"{self.base_url}/sendPhoto"
        
        payload = {
            "chat_id": chat_id,
            "photo": photo
        }
        
        if caption:
            payload["caption"] = caption
        
        if parse_mode:
            payload["parse_mode"] = parse_mode
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Failed to send photo: {e}")
            raise Exception(f"Failed to send photo: {e}")
    
    def send_document(
        self, 
        chat_id: Union[str, int], 
        document: str, 
        caption: Optional[str] = None,
        parse_mode: Optional[str] = None
    ) -> Dict:
        """Send a document to a chat"""
        url = f"{self.base_url}/sendDocument"
        
        payload = {
            "chat_id": chat_id,
            "document": document
        }
        
        if caption:
            payload["caption"] = caption
        
        if parse_mode:
            payload["parse_mode"] = parse_mode
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Failed to send document: {e}")
            raise Exception(f"Failed to send document: {e}")
    
    def get_me(self) -> Dict:
        """Get basic information about the bot"""
        url = f"{self.base_url}/getMe"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Failed to get bot info: {e}")
            raise Exception(f"Failed to get bot info: {e}")
    
    def get_updates(
        self, 
        offset: Optional[int] = None, 
        limit: int = 100, 
        timeout: int = 0
    ) -> Dict:
        """Get updates from Telegram"""
        url = f"{self.base_url}/getUpdates"
        
        params = {
            "limit": limit,
            "timeout": timeout
        }
        
        if offset:
            params["offset"] = offset
        
        try:
            response = requests.get(url, params=params, timeout=timeout + 10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Failed to get updates: {e}")
            raise Exception(f"Failed to get updates: {e}")
    
    def send_markdown_message(self, chat_id: Union[str, int], text: str) -> Dict:
        """Send a message with Markdown formatting"""
        return self.send_message(chat_id, text, parse_mode="Markdown")
    
    def send_html_message(self, chat_id: Union[str, int], text: str) -> Dict:
        """Send a message with HTML formatting"""
        return self.send_message(chat_id, text, parse_mode="HTML")
    
    def send_long_message(self, chat_id: Union[str, int], text: str, chunk_size: int = 4000) -> List[Dict]:
        """Send long messages by splitting them into chunks"""
        if len(text) <= chunk_size:
            return [self.send_message(chat_id, text)]
        
        results = []
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i + chunk_size]
            results.append(self.send_message(chat_id, chunk))
            time.sleep(0.1)  # Small delay to avoid rate limits
        
        return results
    
    def format_rss_entry(self, entry: Dict) -> str:
        """Format RSS entry for Telegram message"""
        title = entry.get('title', 'No Title')
        link = entry.get('link', '')
        published = entry.get('published', '')
        content = entry.get('content', '')
        
        message = f"📰 *{title}*\n\n"
        
        if content:
            # Limit content length for Telegram
            content_preview = content[:300] + "..." if len(content) > 300 else content
            message += f"{content_preview}\n\n"
        
        if published:
            message += f"📅 {published}\n"
        
        if link:
            message += f"🔗 [Read more]({link})"
        
        return message
    
    def send_rss_update(self, chat_id: Union[str, int], entries: List[Dict], feed_title: str = "") -> List[Dict]:
        """Send RSS entries as formatted messages"""
        results = []
        
        if feed_title:
            header = f"📡 *RSS Update: {feed_title}*\n\n"
            results.append(self.send_markdown_message(chat_id, header))
        
        for entry in entries:
            try:
                formatted_message = self.format_rss_entry(entry)
                result = self.send_markdown_message(chat_id, formatted_message)
                results.append(result)
                time.sleep(0.5)  # Delay to avoid rate limits
            except Exception as e:
                self.logger.error(f"Failed to send RSS entry: {e}")
                continue
        
        return results
    
    def test_connection(self) -> bool:
        """Test if the bot token is valid"""
        try:
            response = self.get_me()
            return response.get('ok', False)
        except Exception:
            return False


if __name__ == "__main__":
    import os
    
    # Example usage
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if bot_token and chat_id:
        try:
            bot = TelegramBotHelper(bot_token)
            
            # Test connection
            if bot.test_connection():
                print("Bot connection successful!")
                
                # Send test message
                result = bot.send_message(chat_id, "🤖 RSS Auto Reader bot is online!")
                print(f"Message sent: {result}")
                
                # Example RSS entry
                sample_entry = {
                    'title': 'Sample News Article',
                    'link': 'https://example.com/article',
                    'content': 'This is a sample news article content for testing.',
                    'published': '2024-01-01 12:00:00'
                }
                
                bot.send_rss_update(chat_id, [sample_entry], "Test Feed")
            else:
                print("Bot connection failed!")
        
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables")