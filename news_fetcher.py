"""News fetcher using NewsAPI."""
from typing import Optional, List
from datetime import datetime, timedelta
from newsapi import NewsApiClient
from pydantic import BaseModel


class NewsArticle(BaseModel):
    """News article data model."""

    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    url: str
    source: str
    published_at: datetime
    author: Optional[str] = None
    image_url: Optional[str] = None

    def get_summary(self, max_length: int = 200) -> str:
        """Get a summary of the article.

        Args:
            max_length: Maximum length of the summary

        Returns:
            Article summary
        """
        # Try description first, then content
        text = self.description or self.content or self.title

        if len(text) <= max_length:
            return text

        # Truncate at word boundary
        truncated = text[:max_length].rsplit(' ', 1)[0]
        return truncated + "..."

    def get_video_prompt(self) -> str:
        """Generate a video prompt from the article.

        Returns:
            Video generation prompt
        """
        # Create a descriptive prompt based on the article
        summary = self.get_summary(150)

        # Try to make the prompt more visual
        prompt_templates = [
            f"A news broadcast scene showing: {summary}",
            f"Visual representation of news story: {summary}",
            f"News coverage scene depicting: {summary}",
        ]

        # Choose based on title keywords
        title_lower = self.title.lower()
        if any(word in title_lower for word in ['technology', 'tech', 'ai', 'computer', 'digital']):
            return f"A futuristic technology news scene about: {summary}"
        elif any(word in title_lower for word in ['business', 'economy', 'market', 'stock']):
            return f"A professional business news broadcast about: {summary}"
        elif any(word in title_lower for word in ['sports', 'game', 'match', 'championship']):
            return f"A dynamic sports news coverage of: {summary}"
        elif any(word in title_lower for word in ['entertainment', 'celebrity', 'movie', 'music']):
            return f"An entertainment news segment featuring: {summary}"
        else:
            return prompt_templates[0]

    def get_audio_script(self, include_source: bool = True) -> str:
        """Generate an audio script from the article.

        Args:
            include_source: Whether to include the source name

        Returns:
            Audio narration script
        """
        parts = []

        # Add source if requested
        if include_source and self.source:
            parts.append(f"From {self.source}.")

        # Add title
        parts.append(self.title)

        # Add description/content
        if self.description:
            parts.append(self.description)
        elif self.content:
            # Use first 300 characters of content
            content_summary = self.content[:300]
            if len(self.content) > 300:
                content_summary = content_summary.rsplit(' ', 1)[0] + "..."
            parts.append(content_summary)

        return " ".join(parts)


class NewsFetcher:
    """Fetches news articles from NewsAPI."""

    # Available categories
    CATEGORIES = [
        'business', 'entertainment', 'general', 'health',
        'science', 'sports', 'technology'
    ]

    # Available countries (ISO 3166-1 alpha-2 codes)
    COUNTRIES = [
        'ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co', 'cu',
        'cz', 'de', 'eg', 'fr', 'gb', 'gr', 'hk', 'hu', 'id', 'ie', 'il', 'in',
        'it', 'jp', 'kr', 'lt', 'lv', 'ma', 'mx', 'my', 'ng', 'nl', 'no', 'nz',
        'ph', 'pl', 'pt', 'ro', 'rs', 'ru', 'sa', 'se', 'sg', 'si', 'sk', 'th',
        'tr', 'tw', 'ua', 'us', 've', 'za'
    ]

    def __init__(self, api_key: str):
        """Initialize news fetcher.

        Args:
            api_key: NewsAPI key
        """
        self.api_key = api_key
        self.client = NewsApiClient(api_key=api_key)

    def fetch_top_headlines(
        self,
        country: str = 'us',
        category: Optional[str] = None,
        max_articles: int = 5,
        query: Optional[str] = None
    ) -> List[NewsArticle]:
        """Fetch top headlines.

        Args:
            country: Country code (e.g., 'us', 'gb', 'ca')
            category: News category (business, technology, etc.)
            max_articles: Maximum number of articles to fetch
            query: Search query (optional)

        Returns:
            List of news articles
        """
        if country not in self.COUNTRIES:
            raise ValueError(
                f"Invalid country code: {country}. "
                f"Must be one of: {', '.join(self.COUNTRIES)}"
            )

        if category and category not in self.CATEGORIES:
            raise ValueError(
                f"Invalid category: {category}. "
                f"Must be one of: {', '.join(self.CATEGORIES)}"
            )

        print(f"Fetching top headlines from {country.upper()}")
        if category:
            print(f"Category: {category}")
        if query:
            print(f"Query: {query}")

        try:
            response = self.client.get_top_headlines(
                country=country,
                category=category,
                q=query,
                page_size=max_articles
            )

            articles = []
            for article_data in response.get('articles', []):
                try:
                    article = NewsArticle(
                        title=article_data.get('title', 'Untitled'),
                        description=article_data.get('description'),
                        content=article_data.get('content'),
                        url=article_data.get('url', ''),
                        source=article_data.get('source', {}).get('name', 'Unknown'),
                        published_at=datetime.fromisoformat(
                            article_data.get('publishedAt', '').replace('Z', '+00:00')
                        ),
                        author=article_data.get('author'),
                        image_url=article_data.get('urlToImage')
                    )
                    articles.append(article)
                except Exception as e:
                    print(f"Warning: Failed to parse article: {e}")
                    continue

            print(f"Successfully fetched {len(articles)} articles")
            return articles

        except Exception as e:
            raise RuntimeError(f"Failed to fetch news: {str(e)}")

    def fetch_everything(
        self,
        query: str,
        max_articles: int = 5,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        language: str = 'en',
        sort_by: str = 'publishedAt'
    ) -> List[NewsArticle]:
        """Search all articles with query.

        Args:
            query: Search query
            max_articles: Maximum number of articles to fetch
            from_date: Start date for articles
            to_date: End date for articles
            language: Language code (e.g., 'en', 'es', 'fr')
            sort_by: Sort order (relevancy, popularity, publishedAt)

        Returns:
            List of news articles
        """
        print(f"Searching for articles: {query}")
        print(f"Language: {language}, Sort by: {sort_by}")

        # Default to last 7 days if no date specified
        if not from_date:
            from_date = datetime.now() - timedelta(days=7)

        try:
            response = self.client.get_everything(
                q=query,
                from_param=from_date.isoformat() if from_date else None,
                to=to_date.isoformat() if to_date else None,
                language=language,
                sort_by=sort_by,
                page_size=max_articles
            )

            articles = []
            for article_data in response.get('articles', []):
                try:
                    article = NewsArticle(
                        title=article_data.get('title', 'Untitled'),
                        description=article_data.get('description'),
                        content=article_data.get('content'),
                        url=article_data.get('url', ''),
                        source=article_data.get('source', {}).get('name', 'Unknown'),
                        published_at=datetime.fromisoformat(
                            article_data.get('publishedAt', '').replace('Z', '+00:00')
                        ),
                        author=article_data.get('author'),
                        image_url=article_data.get('urlToImage')
                    )
                    articles.append(article)
                except Exception as e:
                    print(f"Warning: Failed to parse article: {e}")
                    continue

            print(f"Successfully fetched {len(articles)} articles")
            return articles

        except Exception as e:
            raise RuntimeError(f"Failed to search news: {str(e)}")

    def get_sources(
        self,
        category: Optional[str] = None,
        language: Optional[str] = None,
        country: Optional[str] = None
    ) -> List[dict]:
        """Get available news sources.

        Args:
            category: Filter by category
            language: Filter by language
            country: Filter by country

        Returns:
            List of news sources
        """
        try:
            response = self.client.get_sources(
                category=category,
                language=language,
                country=country
            )

            return response.get('sources', [])

        except Exception as e:
            raise RuntimeError(f"Failed to get sources: {str(e)}")
