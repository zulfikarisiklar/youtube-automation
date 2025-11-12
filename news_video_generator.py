"""Generate videos from news articles."""
import asyncio
from pathlib import Path
from typing import Optional, List
from datetime import datetime

from config import config
from news_fetcher import NewsFetcher, NewsArticle
from video_automation import VideoAutomation
from models import VideoRequest, AudioRequest, YouTubeMetadata
from video_processor import VideoProcessor


class NewsVideoGenerator:
    """Generate videos from news articles."""

    def __init__(self, news_api_key: Optional[str] = None):
        """Initialize news video generator.

        Args:
            news_api_key: NewsAPI key (uses config if not provided)
        """
        self.news_api_key = news_api_key or config.news_api_key
        if not self.news_api_key:
            raise ValueError("News API key not configured")

        self.news_fetcher = NewsFetcher(self.news_api_key)
        self.video_automation = VideoAutomation()
        self.video_processor = VideoProcessor()

    def initialize(self, video_model: str = "veo") -> None:
        """Initialize video automation system.

        Args:
            video_model: Video generation model to use
        """
        self.video_automation.initialize(video_model=video_model)

    async def generate_video_from_article(
        self,
        article: NewsArticle,
        video_duration: int = 10,
        language: str = "en",
        add_text_overlay: bool = True,
        output_path: Optional[Path] = None
    ) -> Path:
        """Generate a video from a news article.

        Args:
            article: News article
            video_duration: Video duration in seconds
            language: Audio language
            add_text_overlay: Whether to add title as text overlay
            output_path: Output path for the video

        Returns:
            Path to the generated video
        """
        print(f"\n{'='*60}")
        print(f"Generating video for: {article.title}")
        print(f"{'='*60}\n")

        # Generate video prompt from article
        video_prompt = article.get_video_prompt()
        print(f"Video prompt: {video_prompt}")

        # Generate audio script from article
        audio_script = article.get_audio_script(include_source=True)
        print(f"Audio script: {audio_script[:100]}...")

        # Create video request
        video_request = VideoRequest(
            prompt=video_prompt,
            duration=video_duration,
            model=self.video_automation.video_generator.get_model_name()
        )

        # Create audio request
        audio_request = AudioRequest(
            text=audio_script,
            language=language
        )

        # Generate video with audio
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = "".join(c for c in article.title[:50] if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_title = safe_title.replace(' ', '_')
            output_path = config.temp_dir / f"news_{safe_title}_{timestamp}.mp4"

        video_path = await self.video_automation.create_video(
            video_request=video_request,
            audio_request=audio_request,
            output_path=output_path
        )

        # Add text overlay with title if requested
        if add_text_overlay:
            print("\nAdding text overlay...")
            overlay_path = config.temp_dir / f"overlay_{output_path.name}"
            video_path = await self.video_processor.add_text_overlay(
                video_path=video_path,
                text=article.title[:100],  # Limit title length
                output_path=overlay_path,
                position=('center', 'bottom'),
                fontsize=40,
                color='white'
            )

        print(f"\n✓ Video generated: {video_path}")
        return video_path

    async def generate_videos_from_headlines(
        self,
        country: str = "us",
        category: Optional[str] = None,
        max_articles: int = 5,
        video_duration: int = 10,
        language: str = "en",
        add_text_overlay: bool = True,
        query: Optional[str] = None
    ) -> List[Path]:
        """Generate videos from top headlines.

        Args:
            country: Country code
            category: News category
            max_articles: Maximum number of articles
            video_duration: Duration per video
            language: Audio language
            add_text_overlay: Whether to add text overlays
            query: Search query (optional)

        Returns:
            List of generated video paths
        """
        print(f"\n{'='*60}")
        print(f"Fetching Top Headlines")
        print(f"{'='*60}\n")

        # Fetch articles
        articles = self.news_fetcher.fetch_top_headlines(
            country=country,
            category=category,
            max_articles=max_articles,
            query=query
        )

        if not articles:
            print("No articles found!")
            return []

        # Generate videos for each article
        video_paths = []
        for i, article in enumerate(articles, 1):
            print(f"\n[{i}/{len(articles)}] Processing article...")
            try:
                video_path = await self.generate_video_from_article(
                    article=article,
                    video_duration=video_duration,
                    language=language,
                    add_text_overlay=add_text_overlay
                )
                video_paths.append(video_path)
            except Exception as e:
                print(f"✗ Failed to generate video: {e}")
                continue

        print(f"\n{'='*60}")
        print(f"Generated {len(video_paths)} videos successfully")
        print(f"{'='*60}\n")

        return video_paths

    async def generate_videos_from_search(
        self,
        query: str,
        max_articles: int = 5,
        video_duration: int = 10,
        language: str = "en",
        add_text_overlay: bool = True
    ) -> List[Path]:
        """Generate videos from search query.

        Args:
            query: Search query
            max_articles: Maximum number of articles
            video_duration: Duration per video
            language: Audio language
            add_text_overlay: Whether to add text overlays

        Returns:
            List of generated video paths
        """
        print(f"\n{'='*60}")
        print(f"Searching for: {query}")
        print(f"{'='*60}\n")

        # Fetch articles
        articles = self.news_fetcher.fetch_everything(
            query=query,
            max_articles=max_articles,
            language=language
        )

        if not articles:
            print("No articles found!")
            return []

        # Generate videos for each article
        video_paths = []
        for i, article in enumerate(articles, 1):
            print(f"\n[{i}/{len(articles)}] Processing article...")
            try:
                video_path = await self.generate_video_from_article(
                    article=article,
                    video_duration=video_duration,
                    language=language,
                    add_text_overlay=add_text_overlay
                )
                video_paths.append(video_path)
            except Exception as e:
                print(f"✗ Failed to generate video: {e}")
                continue

        print(f"\n{'='*60}")
        print(f"Generated {len(video_paths)} videos successfully")
        print(f"{'='*60}\n")

        return video_paths

    async def create_news_compilation(
        self,
        video_paths: List[Path],
        output_path: Optional[Path] = None,
        add_intro: bool = False,
        intro_text: Optional[str] = None
    ) -> Path:
        """Merge multiple news videos into a compilation.

        Args:
            video_paths: List of video paths to merge
            output_path: Output path for compilation
            add_intro: Whether to add an intro screen
            intro_text: Text for intro screen

        Returns:
            Path to the merged compilation video
        """
        if not video_paths:
            raise ValueError("No videos to merge")

        print(f"\n{'='*60}")
        print(f"Creating News Compilation")
        print(f"Merging {len(video_paths)} videos")
        print(f"{'='*60}\n")

        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = config.output_dir / f"news_compilation_{timestamp}.mp4"

        # Merge videos
        compilation_path = await self.video_processor.concatenate_videos(
            video_paths=video_paths,
            output_path=output_path
        )

        print(f"\n✓ Compilation created: {compilation_path}")
        return compilation_path

    async def create_and_upload_news_compilation(
        self,
        country: str = "us",
        category: Optional[str] = None,
        max_articles: int = 5,
        video_duration: int = 10,
        language: str = "en",
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        privacy_status: str = "private"
    ) -> dict:
        """Create a news compilation and upload to YouTube.

        Args:
            country: Country code
            category: News category
            max_articles: Maximum number of articles
            video_duration: Duration per video
            language: Audio language
            title: YouTube video title
            description: YouTube video description
            tags: YouTube video tags
            privacy_status: YouTube privacy status

        Returns:
            Upload information dictionary
        """
        # Generate videos from headlines
        video_paths = await self.generate_videos_from_headlines(
            country=country,
            category=category,
            max_articles=max_articles,
            video_duration=video_duration,
            language=language
        )

        if not video_paths:
            raise RuntimeError("No videos were generated")

        # Create compilation
        compilation_path = await self.create_news_compilation(
            video_paths=video_paths
        )

        # Generate title and description if not provided
        if not title:
            category_str = f"{category.title()} " if category else ""
            title = f"{category_str}News Highlights - {datetime.now().strftime('%B %d, %Y')}"

        if not description:
            description = (
                f"Daily {category or 'news'} highlights from {country.upper()}. "
                f"This video compilation features {len(video_paths)} top news stories. "
                f"AI-generated content for informational purposes."
            )

        if not tags:
            tags = ["news", "headlines", "daily news"]
            if category:
                tags.append(category)
            tags.append(country)

        # Create YouTube metadata
        youtube_metadata = YouTubeMetadata(
            title=title,
            description=description,
            tags=tags,
            privacy_status=privacy_status,
            category_id="25",  # News & Politics
            language=language
        )

        # Upload to YouTube
        print(f"\n{'='*60}")
        print(f"Uploading to YouTube")
        print(f"{'='*60}\n")

        # Authenticate and upload
        self.video_automation.youtube_uploader.authenticate()
        upload_info = await self.video_automation.youtube_uploader.upload(
            video_path=compilation_path,
            metadata=youtube_metadata
        )

        print(f"\n✓ Upload complete!")
        print(f"Video URL: {upload_info['url']}")

        return upload_info
