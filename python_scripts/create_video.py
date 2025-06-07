# Function to save edited audio and video files to components directory
def save_edited_media(edited_video, save_dir):
    import os

    video_output_path = os.path.join(save_dir, "edited_background.mp4")

    print(f"Saving edited video to {video_output_path} ...")
    edited_video.write_videofile(video_output_path, codec='libx264', audio_codec='aac')

    print("Save complete.")

    return video_output_path

# Function to merge text, audio, and video into a final video
def split_words(text_file_path):
    # Example: splitting the text file
    with text_file_path.open("r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]

    return lines[0], lines[1], lines[2]

def make_rounded_bar(width, height, radius, color, opacity=255):
    from PIL import Image, ImageDraw
    
    # Create transparent image
    img = Image.new("RGBA", (width, height), (0,0,0,0))
    draw = ImageDraw.Draw(img)
    # Draw rounded rectangle
    draw.rounded_rectangle((0, 0, width, height), radius=radius, fill=color + (opacity,))
    return img

def overlay_text_on_video(todays_date, text_file_path, video_file_path, final_output_path):
    from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ImageClip
    import numpy as np
    from moviepy.config import change_settings as mpy_change_settings
    from pathlib import Path
    import subprocess

    # --- ImageMagick Path Setup (safe and efficient) ---
    project_root = Path(__file__).parent
    imagemagick_dirs = [d for d in project_root.iterdir() if d.is_dir() and d.name.startswith("ImageMagick-")]
    if not imagemagick_dirs:
        raise FileNotFoundError("No ImageMagick portable folder found in the project directory.")
    magick_path = imagemagick_dirs[0] / "magick.exe"
    if not magick_path.exists():
        raise FileNotFoundError(f"'magick.exe' not found in {imagemagick_dirs[0]}.")

    # Test ImageMagick is working
    try:
        subprocess.run([str(magick_path), "-version"], check=True, capture_output=True)
    except Exception as e:
        raise RuntimeError("ImageMagick executable is not working. Cannot proceed.") from e
    mpy_change_settings({"IMAGEMAGICK_BINARY": str(magick_path)})

    # --- Parse Script Content ---
    word, definition, sentence = split_words(text_file_path)

    # --- Load Video (always 1080x1920) ---
    video = VideoFileClip(str(video_file_path))
    w, h = video.size  # Should always be 1080x1920

    font_color = 'white'
    font = 'Arial-Bold'

    # --- Helper for Text Bar with Rounded Background ---
    def highlighted_text_clip(text, fontsize, bar_margin_x, bar_margin_y, bar_radius, max_width):
        from moviepy.editor import TextClip, ImageClip, CompositeVideoClip

        # Use 'caption' method and center align for automatic wrapping
        txt_clip = TextClip(
            text,
            fontsize=fontsize,
            color=font_color,
            font=font,
            size=(max_width, None),
            method='caption',
            align='center'
        )
        # Calculate bar size
        bar_width = txt_clip.w + 2 * bar_margin_x
        bar_height = txt_clip.h + 2 * bar_margin_y

        # Create rounded bar image
        bar_img = make_rounded_bar(bar_width, bar_height, bar_radius, (0,0,0), opacity=220)
        bar_clip = ImageClip(np.array(bar_img)).set_duration(video.duration)

        # Composite text onto bar
        txt_clip = txt_clip.set_position(("center", bar_margin_y))
        return CompositeVideoClip([bar_clip, txt_clip], size=(bar_width, bar_height)).set_duration(video.duration)

    # --- Bar Layout Parameters (based on 1080x1920) ---
    bar_params = [
        (todays_date,   75, 30, 10, 25, int(w * 0.7)),
        (word,          90, 30, 10, 25, int(w * 0.7)),
        (definition,    80, 30, 10, 25, int(w * 0.7)),
        (sentence,      50, 30, 10, 25, int(w * 0.65)),
        ("Instagram: @worddropdaily\nYouTube: @worddrop_daily", 24, 18, 4, 14, int(w * 0.5))
    ]
    bars_and_texts = [
        highlighted_text_clip(*args)
        for args in bar_params
    ]

    # --- Compose All Bars Vertically, Centered ---
    spacing = 30
    total_height = sum(clip.h for clip in bars_and_texts) + spacing * (len(bars_and_texts) - 1)
    y_start = (h - total_height) // 2

    overlay_clips = [video]
    y = y_start
    for clip in bars_and_texts:
        overlay_clips.append(clip.set_position(("center", y)))
        y += clip.h + spacing

    # --- Final Composite and Export ---
    final = CompositeVideoClip(overlay_clips)
    final.write_videofile(str(final_output_path), codec="libx264", audio_codec="aac", threads=4, preset='ultrafast')

    return Path(final_output_path)

