"""YouTube video uploader."""
import asyncio
import pickle
from pathlib import Path
from typing import Optional
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

from models import YouTubeMetadata


class YouTubeUploader:
    """YouTube video uploader with OAuth2 authentication."""

    # YouTube API scopes
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

    # YouTube category IDs
    CATEGORIES = {
        "film_animation": "1",
        "autos_vehicles": "2",
        "music": "10",
        "pets_animals": "15",
        "sports": "17",
        "short_movies": "18",
        "travel_events": "19",
        "gaming": "20",
        "videoblogging": "21",
        "people_blogs": "22",
        "comedy": "23",
        "entertainment": "24",
        "news_politics": "25",
        "howto_style": "26",
        "education": "27",
        "science_technology": "28",
        "nonprofits_activism": "29"
    }

    def __init__(self, client_secrets_file: str = "client_secrets.json"):
        """Initialize YouTube uploader.

        Args:
            client_secrets_file: Path to OAuth2 client secrets JSON file
        """
        self.client_secrets_file = client_secrets_file
        self.credentials = None
        self.youtube = None

    def authenticate(self, token_file: str = "token.pickle") -> None:
        """Authenticate with YouTube API.

        Args:
            token_file: Path to save/load authentication token
        """
        print("Authenticating with YouTube...")

        # Load credentials from file if available
        if Path(token_file).exists():
            with open(token_file, 'rb') as token:
                self.credentials = pickle.load(token)

        # If credentials are invalid or don't exist, get new ones
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                print("Refreshing access token...")
                self.credentials.refresh(Request())
            else:
                if not Path(self.client_secrets_file).exists():
                    raise FileNotFoundError(
                        f"Client secrets file not found: {self.client_secrets_file}\n"
                        f"Please download it from Google Cloud Console:\n"
                        f"1. Go to https://console.cloud.google.com/\n"
                        f"2. Enable YouTube Data API v3\n"
                        f"3. Create OAuth2 credentials\n"
                        f"4. Download the JSON file and save as {self.client_secrets_file}"
                    )

                print("Starting OAuth2 flow...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_file,
                    self.SCOPES
                )
                self.credentials = flow.run_local_server(port=0)

            # Save credentials for next run
            with open(token_file, 'wb') as token:
                pickle.dump(self.credentials, token)

        # Build YouTube service
        self.youtube = build('youtube', 'v3', credentials=self.credentials)
        print("Authentication successful!")

    async def upload(
        self,
        video_path: Path,
        metadata: YouTubeMetadata,
        notify_subscribers: bool = False
    ) -> dict:
        """Upload video to YouTube.

        Args:
            video_path: Path to video file
            metadata: Video metadata
            notify_subscribers: Whether to notify subscribers

        Returns:
            Dictionary with video information (id, url, etc.)
        """
        if not self.youtube:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")

        print(f"Uploading video to YouTube: {metadata.title}")
        print(f"Privacy status: {metadata.privacy_status}")

        try:
            # Prepare request body
            body = {
                'snippet': {
                    'title': metadata.title,
                    'description': metadata.description,
                    'tags': metadata.tags,
                    'categoryId': metadata.category_id,
                    'defaultLanguage': metadata.language,
                    'defaultAudioLanguage': metadata.language
                },
                'status': {
                    'privacyStatus': metadata.privacy_status,
                    'selfDeclaredMadeForKids': False,
                    'notifySubscribers': notify_subscribers
                }
            }

            # Create media upload
            media = MediaFileUpload(
                str(video_path),
                chunksize=-1,  # Upload in a single request
                resumable=True,
                mimetype='video/*'
            )

            # Execute upload
            request = self.youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )

            response = await asyncio.to_thread(self._execute_upload, request)

            video_id = response['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            print("Upload successful!")
            print(f"Video ID: {video_id}")
            print(f"Video URL: {video_url}")

            return {
                'id': video_id,
                'url': video_url,
                'title': metadata.title,
                'privacy_status': metadata.privacy_status
            }

        except HttpError as e:
            raise RuntimeError(f"YouTube API error: {e.resp.status} - {e.content}")
        except Exception as e:
            raise RuntimeError(f"Failed to upload video: {str(e)}")

    def _execute_upload(self, request):
        """Execute upload request with progress tracking.

        Args:
            request: Upload request object

        Returns:
            Upload response
        """
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                progress = int(status.progress() * 100)
                print(f"Upload progress: {progress}%")

        return response

    async def update_video(
        self,
        video_id: str,
        metadata: Optional[YouTubeMetadata] = None,
        privacy_status: Optional[str] = None
    ) -> dict:
        """Update video metadata.

        Args:
            video_id: YouTube video ID
            metadata: New video metadata (optional)
            privacy_status: New privacy status (optional)

        Returns:
            Updated video information
        """
        if not self.youtube:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        print(f"Updating video: {video_id}")

        try:
            body = {}

            if metadata:
                body['snippet'] = {
                    'title': metadata.title,
                    'description': metadata.description,
                    'tags': metadata.tags,
                    'categoryId': metadata.category_id
                }

            if privacy_status:
                body['status'] = {
                    'privacyStatus': privacy_status
                }

            body['id'] = video_id

            request = self.youtube.videos().update(
                part=','.join([k for k in body.keys() if k != 'id']),
                body=body
            )

            response = await asyncio.to_thread(request.execute)

            print("Video updated successfully!")
            return response

        except HttpError as e:
            raise RuntimeError(f"YouTube API error: {e.resp.status} - {e.content}")
        except Exception as e:
            raise RuntimeError(f"Failed to update video: {str(e)}")

    def get_video_info(self, video_id: str) -> dict:
        """Get video information.

        Args:
            video_id: YouTube video ID

        Returns:
            Video information dictionary
        """
        if not self.youtube:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        try:
            request = self.youtube.videos().list(
                part='snippet,status,statistics',
                id=video_id
            )

            response = request.execute()

            if not response['items']:
                raise ValueError(f"Video not found: {video_id}")

            return response['items'][0]

        except HttpError as e:
            raise RuntimeError(f"YouTube API error: {e.resp.status} - {e.content}")
        except Exception as e:
            raise RuntimeError(f"Failed to get video info: {str(e)}")
