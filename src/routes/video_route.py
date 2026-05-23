from fastapi import APIRouter, Query

from schemas.video import Video
from services.video_service import VideoService


router = APIRouter()
video_service = VideoService()

@router.get("")
def fetch_videos(topics: list[str] = Query(...)) -> list[Video]:
    videos = video_service.get_videos_with_topics(topics)
    return videos

@router.get("/{video_id}")
def fetch_video(video_id: str) -> Video:
    video = video_service.get_video_from_id(video_id)
    return video

@router.get("/related_videos/{video_id}")
def fetch_related_videos(video_id: str) -> list[Video]:
    videos = video_service.get_related_videos_from_id(video_id)
    return videos