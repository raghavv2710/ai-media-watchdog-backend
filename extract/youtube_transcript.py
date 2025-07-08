import re

def get_youtube_transcript(url: str) -> str:
    """
    Extracts transcript text from a YouTube video URL.
    """
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except ImportError:
        raise ImportError("youtube-transcript-api is required. Install with 'pip install youtube-transcript-api'")

    # Extract video ID from URL
    match = re.search(r"(?:v=|youtu\\.be/)([a-zA-Z0-9_-]{11})", url)
    if not match:
        raise ValueError("Invalid YouTube URL")
    video_id = match.group(1)

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([entry["text"] for entry in transcript])
        return text
    except Exception as e:
        raise RuntimeError(f"Failed to fetch YouTube transcript: {e}")
