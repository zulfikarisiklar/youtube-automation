# News Video Generation Features 📰

Automatically generate and upload YouTube videos from news articles with AI-generated visuals and multi-language narration.

## Overview

The news video generation system fetches news articles from NewsAPI and automatically creates engaging videos with:
- AI-generated visuals matching the news content
- Professional narration in 30+ languages
- Title overlays for better viewer engagement
- Automatic video merging for longer compilations
- Direct upload to YouTube

## Setup

### 1. Get NewsAPI Key

1. Visit [https://newsapi.org/](https://newsapi.org/)
2. Sign up for a free account
3. Copy your API key from the dashboard
4. Add to `.env` file:

```bash
NEWS_API_KEY=your_newsapi_key_here
```

### 2. Configure News Settings (Optional)

Edit `.env` to customize default settings:

```bash
NEWS_COUNTRY=us          # Default country code
NEWS_CATEGORY=           # Default category (leave empty for all)
NEWS_MAX_ARTICLES=5      # Maximum articles per fetch
NEWS_VIDEO_DURATION=10   # Duration per video in seconds
```

## CLI Commands

### Generate Videos from Headlines

Create videos from top news headlines:

```bash
python cli.py news-videos --country us --category technology --max-articles 5
```

**Options:**
- `--country, -c`: Country code (us, gb, ca, etc.)
- `--category`: News category (business, technology, sports, entertainment, health, science, general)
- `--max-articles, -n`: Maximum number of articles to process
- `--duration, -d`: Duration per video in seconds
- `--language, -l`: Audio language code
- `--model, -m`: Video generation model (veo or sora)
- `--no-overlay`: Disable text overlay on videos
- `--query, -q`: Search query to filter headlines

**Examples:**

```bash
# Generate 5 technology news videos from the US
python cli.py news-videos -c us --category technology -n 5

# Generate business news in Spanish from Mexico
python cli.py news-videos -c mx --category business -l es

# Filter headlines about AI
python cli.py news-videos -c us --query "artificial intelligence" -n 3
```

### Create News Compilation

Generate videos and merge them into a single compilation:

```bash
python cli.py news-compilation --country us --category sports --max-articles 5
```

**Options:**
- Same as `news-videos` plus:
- `--output, -o`: Custom output file path for the compilation

**Examples:**

```bash
# Create sports news compilation
python cli.py news-compilation -c us --category sports -n 5 -o output/sports_today.mp4

# Create multilingual news compilation
python cli.py news-compilation -c fr --category general -l fr -n 3
```

### Upload News Compilation to YouTube

Create a compilation and automatically upload it:

```bash
python cli.py news-upload --country us --category technology --title "Tech News Today"
```

**Options:**
- All `news-compilation` options plus:
- `--title, -t`: YouTube video title
- `--description`: YouTube video description
- `--tags`: Comma-separated tags
- `--privacy`: Privacy status (public, private, unlisted)

**Examples:**

```bash
# Upload technology news
python cli.py news-upload \
  --country us \
  --category technology \
  --title "Tech News Highlights - Today" \
  --description "Daily technology news roundup" \
  --tags "technology,news,tech,AI" \
  --privacy private

# Upload international business news
python cli.py news-upload \
  --country gb \
  --category business \
  --title "UK Business News" \
  --language en \
  --privacy public
```

### Search News and Generate Videos

Search for specific topics and create videos:

```bash
python cli.py news-search "artificial intelligence" --merge
```

**Options:**
- `query`: Search query (required)
- `--max-articles, -n`: Maximum articles
- `--duration, -d`: Duration per video
- `--language, -l`: Audio language
- `--model, -m`: Video model
- `--merge`: Merge into single compilation
- `--output, -o`: Output file path

**Examples:**

```bash
# Search for AI news and create individual videos
python cli.py news-search "artificial intelligence" -n 5

# Search and merge into compilation
python cli.py news-search "climate change" -n 5 --merge -o output/climate_news.mp4

# Search in Spanish
python cli.py news-search "inteligencia artificial" -l es --merge
```

### List Available News Sources

View available news sources:

```bash
python cli.py news-sources
```

**Options:**
- `--category`: Filter by category
- `--country`: Filter by country
- `--language`: Filter by language

**Examples:**

```bash
# List all technology sources
python cli.py news-sources --category technology

# List US news sources
python cli.py news-sources --country us

# List Spanish language sources
python cli.py news-sources --language es
```

## Available Categories

- `business` - Business and finance news
- `technology` - Technology and gadgets
- `sports` - Sports news and updates
- `entertainment` - Entertainment and celebrity news
- `health` - Health and medical news
- `science` - Science and research
- `general` - General news

## Supported Countries

The system supports 50+ countries. Common ones include:

- `us` - United States
- `gb` - United Kingdom
- `ca` - Canada
- `au` - Australia
- `de` - Germany
- `fr` - France
- `es` - Spain
- `it` - Italy
- `jp` - Japan
- `kr` - South Korea
- `in` - India
- `mx` - Mexico
- `br` - Brazil
- `ar` - Argentina

See [NewsAPI Countries](https://newsapi.org/docs/endpoints/sources) for full list.

## Python API Examples

### Basic Usage

```python
import asyncio
from news_video_generator import NewsVideoGenerator

async def main():
    generator = NewsVideoGenerator()
    generator.initialize(video_model="veo")

    # Generate videos from headlines
    video_paths = await generator.generate_videos_from_headlines(
        country="us",
        category="technology",
        max_articles=5
    )

    print(f"Generated {len(video_paths)} videos")

asyncio.run(main())
```

### Create Compilation

```python
async def create_compilation():
    generator = NewsVideoGenerator()
    generator.initialize(video_model="veo")

    # Generate videos
    videos = await generator.generate_videos_from_headlines(
        country="us",
        category="business",
        max_articles=5
    )

    # Merge into compilation
    compilation = await generator.create_news_compilation(
        video_paths=videos,
        output_path=Path("output/business_news.mp4")
    )

    print(f"Compilation: {compilation}")
```

### Search and Generate

```python
async def search_news():
    generator = NewsVideoGenerator()
    generator.initialize(video_model="veo")

    videos = await generator.generate_videos_from_search(
        query="climate change",
        max_articles=5,
        language="en"
    )

    print(f"Generated {len(videos)} videos about climate change")
```

### Upload to YouTube

```python
async def upload_news():
    generator = NewsVideoGenerator()
    generator.initialize(video_model="veo")

    upload_info = await generator.create_and_upload_news_compilation(
        country="us",
        category="technology",
        max_articles=5,
        title="Tech News Today",
        tags=["technology", "news", "tech"],
        privacy_status="private"
    )

    print(f"Video URL: {upload_info['url']}")
```

## Workflow Examples

### Daily News Automation

Automate daily news video creation:

```bash
# Morning: Technology news
python cli.py news-upload \
  --category technology \
  --title "Tech News - $(date +%Y-%m-%d)" \
  --max-articles 5 \
  --privacy private

# Afternoon: Business news
python cli.py news-upload \
  --category business \
  --title "Business News - $(date +%Y-%m-%d)" \
  --max-articles 5 \
  --privacy private
```

### Multi-Category Compilation

Create a multi-category news show:

```python
async def multi_category_news():
    generator = NewsVideoGenerator()
    generator.initialize(video_model="veo")

    all_videos = []

    # Technology news
    tech_videos = await generator.generate_videos_from_headlines(
        category="technology",
        max_articles=3
    )
    all_videos.extend(tech_videos)

    # Business news
    business_videos = await generator.generate_videos_from_headlines(
        category="business",
        max_articles=3
    )
    all_videos.extend(business_videos)

    # Sports news
    sports_videos = await generator.generate_videos_from_headlines(
        category="sports",
        max_articles=2
    )
    all_videos.extend(sports_videos)

    # Create compilation
    compilation = await generator.create_news_compilation(
        video_paths=all_videos,
        output_path=Path("output/daily_news_show.mp4")
    )

    return compilation
```

### International News

Create news videos in multiple languages:

```bash
# English (US)
python cli.py news-compilation -c us -l en -n 3 -o output/news_en.mp4

# Spanish (Mexico)
python cli.py news-compilation -c mx -l es -n 3 -o output/news_es.mp4

# French (France)
python cli.py news-compilation -c fr -l fr -n 3 -o output/news_fr.mp4

# German (Germany)
python cli.py news-compilation -c de -l de -n 3 -o output/news_de.mp4
```

## Best Practices

### Video Duration
- Keep individual segments 8-15 seconds for better engagement
- Total compilation should be 2-5 minutes for YouTube Shorts
- Longer compilations (5-10 minutes) work better for full videos

### Content Selection
- Use specific categories for focused content
- Filter with queries for niche topics
- Mix categories for variety shows

### YouTube Optimization
- Include relevant keywords in titles
- Add comprehensive descriptions
- Use category-specific tags
- Start with private uploads to review content

### Scheduling
- Post regularly (daily or weekly)
- Consider time zones for your audience
- Use YouTube's scheduling feature

## Limitations

### NewsAPI Free Tier
- 100 requests per day
- News up to 1 month old
- Some sources may be restricted

### Video Generation
- AI-generated visuals may not perfectly match content
- Video generation can take 30-60 seconds per segment
- Some models may have availability restrictions

### YouTube Quotas
- YouTube API has daily quotas (10,000 units default)
- Each upload costs ~1600 units
- Plan accordingly for daily uploads

## Troubleshooting

### "News API key not configured"
```bash
python cli.py setup
# Or edit .env and add NEWS_API_KEY
```

### "No articles found"
- Check your country code is valid
- Try without category filter
- Verify your NewsAPI key is active

### "Failed to generate video"
- Check your video generation API keys
- Verify you have sufficient API credits
- Try reducing max_articles

### YouTube upload fails
- Ensure client_secrets.json is configured
- Check YouTube API quota
- Verify OAuth consent is set up

## Advanced Features

### Custom News Prompts

Customize video generation prompts:

```python
from news_fetcher import NewsArticle

# Override get_video_prompt method
class CustomArticle(NewsArticle):
    def get_video_prompt(self) -> str:
        return f"Breaking news visualization: {self.title}"
```

### Custom Audio Scripts

Modify narration scripts:

```python
class CustomArticle(NewsArticle):
    def get_audio_script(self, include_source: bool = True) -> str:
        return f"This just in: {self.title}. {self.description}"
```

## Examples

Check `examples/news_examples.py` for complete working examples:

```bash
python examples/news_examples.py
```

## Support

For issues:
- Check NewsAPI status: https://newsapi.org/status
- Verify API keys in `.env`
- Review error messages for specific issues
- See main README.md for general troubleshooting

## Contributing

We welcome contributions! Potential improvements:
- Additional news sources
- Custom video templates
- Advanced filtering options
- Scheduling automation
- Multi-platform support

---

Happy news automation! 📰🎬
