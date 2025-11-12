"""Video processing utilities."""
import asyncio
from pathlib import Path
from typing import Optional
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip, concatenate_videoclips
from moviepy.video.fx import resize, speedx


class VideoProcessor:
    """Video processing and editing utilities."""

    @staticmethod
    async def merge_audio_video(
        video_path: Path,
        audio_path: Path,
        output_path: Optional[Path] = None,
        adjust_duration: bool = True
    ) -> Path:
        """Merge audio and video files.

        Args:
            video_path: Path to video file
            audio_path: Path to audio file
            output_path: Path to save the merged video
            adjust_duration: If True, adjust video duration to match audio

        Returns:
            Path to the merged video file
        """
        if output_path is None:
            import time
            output_path = Path(f"merged_video_{int(time.time())}.mp4")

        print(f"Merging video and audio...")
        print(f"Video: {video_path}")
        print(f"Audio: {audio_path}")

        try:
            # Load video and audio
            video = await asyncio.to_thread(VideoFileClip, str(video_path))
            audio = await asyncio.to_thread(AudioFileClip, str(audio_path))

            # Adjust video duration to match audio if needed
            if adjust_duration and video.duration != audio.duration:
                print(f"Adjusting video duration from {video.duration}s to {audio.duration}s")
                if video.duration > audio.duration:
                    # Trim video
                    video = video.subclip(0, audio.duration)
                else:
                    # Speed up or loop video
                    speed_factor = video.duration / audio.duration
                    if speed_factor > 0.5:  # Speed up
                        video = speedx(video, speed_factor)
                    else:  # Loop
                        loops_needed = int(audio.duration / video.duration) + 1
                        video = concatenate_videoclips([video] * loops_needed)
                        video = video.subclip(0, audio.duration)

            # Set audio
            final_video = video.set_audio(audio)

            # Write output
            await asyncio.to_thread(
                final_video.write_videofile,
                str(output_path),
                codec='libx264',
                audio_codec='aac',
                temp_audiofile=str(output_path.parent / 'temp-audio.m4a'),
                remove_temp=True,
                logger=None
            )

            # Close clips
            video.close()
            audio.close()
            final_video.close()

            print(f"Video merged successfully: {output_path}")
            return output_path

        except Exception as e:
            raise RuntimeError(f"Failed to merge video and audio: {str(e)}")

    @staticmethod
    async def add_text_overlay(
        video_path: Path,
        text: str,
        output_path: Optional[Path] = None,
        position: tuple[str, str] = ('center', 'bottom'),
        fontsize: int = 50,
        color: str = 'white',
        duration: Optional[float] = None
    ) -> Path:
        """Add text overlay to video.

        Args:
            video_path: Path to video file
            text: Text to overlay
            output_path: Path to save the video with overlay
            position: Text position (e.g., ('center', 'bottom'))
            fontsize: Font size
            color: Text color
            duration: Text duration (None = entire video)

        Returns:
            Path to the video with text overlay
        """
        if output_path is None:
            import time
            output_path = Path(f"video_with_text_{int(time.time())}.mp4")

        print(f"Adding text overlay: {text}")

        try:
            # Load video
            video = await asyncio.to_thread(VideoFileClip, str(video_path))

            # Create text clip
            txt_clip = TextClip(
                text,
                fontsize=fontsize,
                color=color,
                font='Arial'
            )
            txt_clip = txt_clip.set_position(position)
            txt_clip = txt_clip.set_duration(duration or video.duration)

            # Composite video
            final_video = CompositeVideoClip([video, txt_clip])

            # Write output
            await asyncio.to_thread(
                final_video.write_videofile,
                str(output_path),
                codec='libx264',
                audio_codec='aac',
                logger=None
            )

            # Close clips
            video.close()
            txt_clip.close()
            final_video.close()

            print(f"Text overlay added successfully: {output_path}")
            return output_path

        except Exception as e:
            raise RuntimeError(f"Failed to add text overlay: {str(e)}")

    @staticmethod
    async def resize_video(
        video_path: Path,
        resolution: tuple[int, int],
        output_path: Optional[Path] = None
    ) -> Path:
        """Resize video to specified resolution.

        Args:
            video_path: Path to video file
            resolution: Target resolution (width, height)
            output_path: Path to save the resized video

        Returns:
            Path to the resized video
        """
        if output_path is None:
            import time
            output_path = Path(f"resized_video_{int(time.time())}.mp4")

        print(f"Resizing video to {resolution[0]}x{resolution[1]}")

        try:
            # Load video
            video = await asyncio.to_thread(VideoFileClip, str(video_path))

            # Resize
            resized_video = resize(video, newsize=resolution)

            # Write output
            await asyncio.to_thread(
                resized_video.write_videofile,
                str(output_path),
                codec='libx264',
                audio_codec='aac',
                logger=None
            )

            # Close clips
            video.close()
            resized_video.close()

            print(f"Video resized successfully: {output_path}")
            return output_path

        except Exception as e:
            raise RuntimeError(f"Failed to resize video: {str(e)}")

    @staticmethod
    async def concatenate_videos(
        video_paths: list[Path],
        output_path: Optional[Path] = None
    ) -> Path:
        """Concatenate multiple videos.

        Args:
            video_paths: List of video file paths
            output_path: Path to save the concatenated video

        Returns:
            Path to the concatenated video
        """
        if output_path is None:
            import time
            output_path = Path(f"concatenated_video_{int(time.time())}.mp4")

        print(f"Concatenating {len(video_paths)} videos")

        try:
            # Load videos
            clips = []
            for path in video_paths:
                clip = await asyncio.to_thread(VideoFileClip, str(path))
                clips.append(clip)

            # Concatenate
            final_video = concatenate_videoclips(clips, method="compose")

            # Write output
            await asyncio.to_thread(
                final_video.write_videofile,
                str(output_path),
                codec='libx264',
                audio_codec='aac',
                logger=None
            )

            # Close clips
            for clip in clips:
                clip.close()
            final_video.close()

            print(f"Videos concatenated successfully: {output_path}")
            return output_path

        except Exception as e:
            raise RuntimeError(f"Failed to concatenate videos: {str(e)}")
