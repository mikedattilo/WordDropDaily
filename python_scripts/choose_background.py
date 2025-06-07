
# Function that gets the background image for the video
def get_background_video(api_key):
    import requests

    def get_random_query():
        import random
        queries = ["city", "nature", "mountain", "forest", "lake", "ocean", "sunset", "night sky", "urban", "beach"]
        return random.choice(queries)
    
    query = get_random_query()
    headers = {"Authorization": api_key}
    params = {
        "query": query,
        "orientation": "portrait",
        "per_page": 15,    # Fetch more results per request
        "size": "medium"   # You can try "large" as well
    }

    response = requests.get("https://api.pexels.com/videos/search", headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    # Loop through returned videos and their video_files
    for video in data.get("videos", []):
        for file in video.get("video_files", []):
            width, height = file.get("width"), file.get("height")
            if (width, height) == (1080, 1920):
                video_url = file.get("link")
                vid_response = requests.get(video_url, stream=True)
                vid_response.raise_for_status()
                return vid_response.content

    raise ValueError(f"No 1080x1920 videos found for query: {query}")

# Function to check if a video is in the correct resolution (1080x1920)
def video_resolution_check(raw_bytes):
    import tempfile, os
    from moviepy.editor import VideoFileClip

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    try:
        temp_file.write(raw_bytes)
        temp_file.close()  # Close so MoviePy/FFmpeg can open it

        clip = VideoFileClip(temp_file.name)
        width, height = clip.size
        clip.close()

        return (width, height) == (1080, 1920)
    finally:
        os.remove(temp_file.name)  # Clean up manually

# Function to check if a video is longer than 15 seconds and trim it if necessary
def trim_video_file(video_file_path, max_duration=15):
    from moviepy.editor import VideoFileClip
    from pathlib import Path

    video_file_path = Path(video_file_path)
    
    with VideoFileClip(str(video_file_path)) as clip:
        duration = clip.duration

        if duration <= max_duration:
            print(f"Skipping trim: {video_file_path.name} ({duration:.2f}s)")
            return

        print(f"Trimming: {video_file_path.name} ({duration:.2f}s) -> {max_duration}s")
        # Trim and write to a temp file
        trimmed_clip = clip.subclip(0, max_duration)
        temp_path = video_file_path.with_suffix('.trimmed.mp4')
        trimmed_clip.write_videofile(str(temp_path), codec="libx264", audio_codec="aac")
        trimmed_clip.close()
        # Overwrite original with trimmed
        temp_path.replace(video_file_path)

# Function that retrieves stock media files from a specified directory
def get_stock_media_files(directory: str):
    from pathlib import Path
    import os

    # Get absolute path based on script's parent directory and the given directory
    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(script_dir)
    stock_media_dir = os.path.join(parent_dir, directory)

    folder = Path(stock_media_dir)
    return [f.name for f in folder.glob('*.mp4') if f.is_file()]

# Function to get the path of a specific stock media file
def get_stock_media_path(filename: str):
    from pathlib import Path
    import os

    # Get the parent directory of the current script
    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(script_dir)
    # Build the path to the file within 'stock_media'
    file_path = Path(parent_dir) / "stock_media" / filename
    return file_path
