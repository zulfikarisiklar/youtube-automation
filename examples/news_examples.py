#!/usr/bin/env python3
"""Examples for news video generation features."""
import asyncio
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from news_video_generator import NewsVideoGenerator


async def example_generate_tech_news():
    """Generate videos from technology news."""
    print("Example 1: Generating videos from technology news\n")

    generator = NewsVideoGenerator()
    generator.initialize(video_model="veo")

    video_paths = await generator.generate_videos_from_headlines(
        country="us",
        category="technology",
        max_articles=3,
        video_duration=10,
        language="en"
    )

    print(f"\nGenerated {len(video_paths)} technology news videos")
    for path in video_paths:
        print(f"  - {path}")


async def example_create_news_compilation():
    """Create a news compilation from headlines."""
    print("Example 2: Creating news compilation\n")

    generator = NewsVideoGenerator()
    generator.initialize(video_model="veo")

    # Generate videos
    video_paths = await generator.generate_videos_from_headlines(
        country="us",
        category="business",
        max_articles=3,
        video_duration=8,
        language="en"
    )

    if not video_paths:
        print("No videos generated")
        return

    # Merge into compilation
    compilation_path = await generator.create_news_compilation(
        video_paths=video_paths,
        output_path=Path("output/business_news_compilation.mp4")
    )

    print(f"\nCompilation created: {compilation_path}")


async def example_search_and_generate():
    """Search for specific news topics and generate videos."""
    print("Example 3: Searching for AI news and generating videos\n")

    generator = NewsVideoGenerator()
    generator.initialize(video_model="veo")

    video_paths = await generator.generate_videos_from_search(
        query="artificial intelligence",
        max_articles=3,
        video_duration=10,
        language="en"
    )

    print(f"\nGenerated {len(video_paths)} videos about AI")


async def example_multilingual_news():
    """Generate news videos in different languages."""
    print("Example 4: Multilingual news videos\n")

    generator = NewsVideoGenerator()
    generator.initialize(video_model="veo")

    languages = {
        "en": "us",
        "es": "mx",
        "fr": "fr",
        "de": "de"
    }

    for lang, country in languages.items():
        print(f"\nGenerating news in {lang.upper()} from {country.upper()}...")

        video_paths = await generator.generate_videos_from_headlines(
            country=country,
            max_articles=2,
            video_duration=8,
            language=lang
        )

        print(f"Generated {len(video_paths)} videos in {lang}")


async def example_category_based_news():
    """Generate videos for different news categories."""
    print("Example 5: Different news categories\n")

    generator = NewsVideoGenerator()
    generator.initialize(video_model="veo")

    categories = ["business", "technology", "sports", "entertainment"]

    for category in categories:
        print(f"\n{'='*60}")
        print(f"Processing {category.upper()} news")
        print(f"{'='*60}\n")

        try:
            video_paths = await generator.generate_videos_from_headlines(
                country="us",
                category=category,
                max_articles=2,
                video_duration=8,
                language="en"
            )

            if video_paths:
                # Create category compilation
                compilation_path = await generator.create_news_compilation(
                    video_paths=video_paths,
                    output_path=Path(f"output/{category}_news.mp4")
                )
                print(f"Created compilation: {compilation_path}")

        except Exception as e:
            print(f"Error processing {category}: {e}")


async def example_upload_news_compilation():
    """Create and upload a news compilation to YouTube."""
    print("Example 6: Upload news compilation to YouTube\n")

    generator = NewsVideoGenerator()
    generator.initialize(video_model="veo")

    try:
        upload_info = await generator.create_and_upload_news_compilation(
            country="us",
            category="technology",
            max_articles=3,
            video_duration=10,
            language="en",
            title="Technology News Highlights - Today",
            description="Daily technology news compilation featuring the latest tech stories.",
            tags=["technology", "news", "tech", "daily news", "ai"],
            privacy_status="private"  # Use 'public' when ready to publish
        )

        print("\nUpload successful!")
        print(f"Video URL: {upload_info['url']}")
        print(f"Video ID: {upload_info['id']}")

    except Exception as e:
        print(f"Upload failed: {e}")


async def example_custom_workflow():
    """Custom workflow: Fetch, process, and upload."""
    print("Example 7: Custom workflow\n")

    generator = NewsVideoGenerator()
    generator.initialize(video_model="veo")

    # Step 1: Fetch technology news
    print("Step 1: Fetching technology news...")
    tech_videos = await generator.generate_videos_from_headlines(
        country="us",
        category="technology",
        max_articles=2,
        video_duration=8,
        language="en"
    )

    # Step 2: Fetch business news
    print("\nStep 2: Fetching business news...")
    business_videos = await generator.generate_videos_from_headlines(
        country="us",
        category="business",
        max_articles=2,
        video_duration=8,
        language="en"
    )

    # Step 3: Combine all videos
    all_videos = tech_videos + business_videos

    if not all_videos:
        print("No videos generated")
        return

    # Step 4: Create compilation
    print("\nStep 3: Creating compilation...")
    compilation_path = await generator.create_news_compilation(
        video_paths=all_videos,
        output_path=Path("output/tech_business_news.mp4")
    )

    print(f"\nCustom compilation created: {compilation_path}")
    print(f"Total videos: {len(all_videos)}")


async def main():
    """Main function to run examples."""
    print("\nNews Video Generation Examples")
    print("=" * 60)

    examples = {
        "1": ("Generate tech news videos", example_generate_tech_news),
        "2": ("Create news compilation", example_create_news_compilation),
        "3": ("Search and generate videos", example_search_and_generate),
        "4": ("Multilingual news videos", example_multilingual_news),
        "5": ("Category-based news", example_category_based_news),
        "6": ("Upload news compilation", example_upload_news_compilation),
        "7": ("Custom workflow", example_custom_workflow),
    }

    print("\nAvailable examples:")
    for key, (name, _) in examples.items():
        print(f"{key}. {name}")

    choice = input("\nEnter example number (or 'all' to run all): ").strip()

    if choice.lower() == "all":
        for name, func in examples.values():
            print(f"\n{'='*60}")
            print(f"Running: {name}")
            print(f"{'='*60}\n")
            try:
                await func()
            except Exception as e:
                print(f"Error: {e}")
            await asyncio.sleep(2)
    elif choice in examples:
        name, func = examples[choice]
        print(f"\nRunning: {name}\n")
        try:
            await func()
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Invalid choice")


if __name__ == "__main__":
    asyncio.run(main())
