from email import message
from schemas.video import Video
from config.app_config import get_config
from googleapiclient.discovery import build
from isodate import parse_duration
from typing import Optional
from youtube_transcript_api import YouTubeTranscriptApi

class VideoService:
    def __init__(self):
        
        config = get_config()
        self.youtube = build('youtube', 'v3', developerKey=config.youtube_api_key)
    
    def _parse_video_data(self, item: dict, include_content_details: bool = True) -> Video:
       
        snippet = item.get('snippet', {})
        statistics = item.get('statistics', {})
        content_details = item.get('contentDetails', {})
        
        
        duration_seconds = 0
        if include_content_details and 'duration' in content_details:
            duration_iso = content_details['duration']
            try:
                duration_seconds = int(parse_duration(duration_iso).total_seconds())
            except:
                duration_seconds = 1 
        else:
            duration_seconds = 1  
        
        
        thumbnails = snippet.get('thumbnails', {})
        thumbnail_url = None
        for quality in ['maxres', 'high', 'medium', 'default']:
            if quality in thumbnails:
                thumbnail_url = thumbnails[quality].get('url')
                break

        video_id = item.get('id') or (item.get('id', {}).get('videoId') if isinstance(item.get('id'), dict) else '')
        text = ""
        if video_id:
            try:
                transcript = YouTubeTranscriptApi().fetch(str(video_id))
                text = " ".join(snippet.text for snippet in transcript)
            except Exception:
                raise Exception({
                    message: "Video transcript not found."
                })
        
        return Video(
            video_id=item.get('id', {}).get('videoId') if 'id' in item and isinstance(item['id'], dict) else item.get('id', ''),
            name=snippet.get('title', 'Untitled'),
            description=snippet.get('description', ''),
            channel_name=snippet.get('channelTitle', 'Unknown Channel'),
            channel_id=snippet.get('channelId', ''),
            duration=duration_seconds if duration_seconds > 0 else 1,
            video_transcript=text,  
            thumbnail_url=thumbnail_url,
            published_at=snippet.get('publishedAt'),
            view_count=int(statistics.get('viewCount', 0)),
            like_count=int(statistics.get('likeCount', 0)),
            tags=snippet.get('tags', [])
        )
    
    def get_videos_with_topics(self, topics: list[str]) -> list[Video]:
        
        if not topics:
            return []
        
        
        search_query = ' '.join(topics)
        
        try:
            
            search_response = self.youtube.search().list(
                q=search_query,
                part='snippet',
                type='video',
                maxResults=10,
                order='relevance'
            ).execute()
            
            videos = []
            video_ids = []
            
            
            for item in search_response.get('items', []):
                video_id = item['id'].get('videoId')
                if video_id:
                    video_ids.append(video_id)
            
           
            if video_ids:
                videos_response = self.youtube.videos().list(
                    part='snippet,contentDetails,statistics',
                    id=','.join(video_ids)
                ).execute()
                
                for item in videos_response.get('items', []):
                    print("*****************")
                    print(item)
                    print("*****************")
                    video = self._parse_video_data(item, include_content_details=True)
                    videos.append(video)
            
            return videos
            
        except Exception as e:
            print(f"Error fetching videos with topics: {e}")
            return []
    
    def get_video_from_id(self, id: str) -> Optional[Video]:
        
        try:
            response = self.youtube.videos().list(
                part='snippet,contentDetails,statistics',
                id=id
            ).execute()
            
            items = response.get('items', [])
            if not items:
                
                return Video(
                    video_id=id,
                    name="Video not found",
                    description="",
                    channel_name="Unknown",
                    channel_id="",
                    duration=1,
                    video_transcript="",
                    thumbnail_url=None,
                    published_at=None,
                    view_count=0,
                    like_count=0,
                    tags=[]
                )
            
            return self._parse_video_data(items[0], include_content_details=True)
            
        except Exception as e:
            print(f"Error fetching video {id}: {e}")
            
            return Video(
                video_id=id,
                name="Error fetching video",
                description="",
                channel_name="Unknown",
                channel_id="",
                duration=1,
                video_transcript="",
                thumbnail_url=None,
                published_at=None,
                view_count=0,
                like_count=0,
                tags=[]
            )
    
    def get_related_videos_from_id(self, id: str) -> list[Video]:
        
        try:
           
            search_response = self.youtube.search().list(
                part='snippet',
                relatedToVideoId=id,
                type='video',
                maxResults=10
            ).execute()
            
            videos = []
            video_ids = []
            
            
            for item in search_response.get('items', []):
                video_id = item['id'].get('videoId')
                if video_id:
                    video_ids.append(video_id)
            
           
            if video_ids:
                videos_response = self.youtube.videos().list(
                    part='snippet,contentDetails,statistics',
                    id=','.join(video_ids)
                ).execute()
                
                for item in videos_response.get('items', []):
                    video = self._parse_video_data(item, include_content_details=True)
                    videos.append(video)
            
            return videos
            
        except Exception as e:
            print(f"Error fetching related videos for {id}: {e}")
            return []