import feedparser
import requests
from typing import List, Dict, Optional
from datetime import datetime
import html2text


class RSSFeedHelper:
    def __init__(self):
        self.h = html2text.HTML2Text()
        self.h.ignore_links = False
        self.h.ignore_images = True
        
    def fetch_feed(self, url: str) -> feedparser.FeedParserDict:
        """Fetch and parse RSS feed from URL"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return feedparser.parse(response.content)
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch RSS feed: {e}")
    
    def parse_feed(self, feed: feedparser.FeedParserDict) -> Dict:
        """Parse feed data and extract metadata"""
        return {
            'title': getattr(feed.feed, 'title', 'Unknown'),
            'description': getattr(feed.feed, 'description', ''),
            'link': getattr(feed.feed, 'link', ''),
            'updated': getattr(feed.feed, 'updated', ''),
            'entries_count': len(feed.entries)
        }
    
    def get_entries(self, feed: feedparser.FeedParserDict, limit: Optional[int] = None) -> List[Dict]:
        """Extract entries from RSS feed"""
        entries = []
        feed_entries = feed.entries[:limit] if limit else feed.entries
        
        for entry in feed_entries:
            entry_data = {
                'title': getattr(entry, 'title', 'No Title'),
                'link': getattr(entry, 'link', ''),
                'description': getattr(entry, 'description', ''),
                'published': getattr(entry, 'published', ''),
                'author': getattr(entry, 'author', ''),
                'tags': [tag.term for tag in getattr(entry, 'tags', [])],
                'content': self._extract_content(entry)
            }
            entries.append(entry_data)
        
        return entries
    
    def _extract_content(self, entry) -> str:
        """Extract and clean content from entry"""
        content = ''
        
        if hasattr(entry, 'content') and entry.content:
            content = entry.content[0].value
        elif hasattr(entry, 'summary') and entry.summary:
            content = entry.summary
        elif hasattr(entry, 'description') and entry.description:
            content = entry.description
        
        return self.h.handle(content).strip()
    
    def process_feed(self, url: str, limit: Optional[int] = None) -> Dict:
        """Complete RSS processing pipeline"""
        feed = self.fetch_feed(url)
        
        if feed.bozo and feed.bozo_exception:
            raise Exception(f"Invalid RSS feed: {feed.bozo_exception}")
        
        feed_info = self.parse_feed(feed)
        entries = self.get_entries(feed, limit)
        
        return {
            'feed_info': feed_info,
            'entries': entries,
            'fetched_at': datetime.now().isoformat()
        }


if __name__ == "__main__":
    helper = RSSFeedHelper()

    # Example usage
    try:
        result = helper.process_feed("https://feeds.bbci.co.uk/news/rss.xml", limit=5)
        print(f"Feed: {result['feed_info']['title']}")
        print(f"Entries: {len(result['entries'])}")
        
        for i, entry in enumerate(result['entries'], 1):
            print(f"\n{i}. {entry['title']}")
            print(f"   Link: {entry['link']}")
            print(f"   Published: {entry['published']}")
            if entry['content']:
                print(f"   Content: {entry['content'][:200]}...")
    
    except Exception as e:
        print(f"Error: {e}")