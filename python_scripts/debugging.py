from moviepy.editor import TextClip
from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": r"c:\Users\miked\OneDrive\Documents\GitHub\WordDrop_Daily\python_scripts\ImageMagick-7.1.1-47-portable-Q16-x64\magick.exe"})

try:
    clip = TextClip(
        "Wide test: The quick brown fox jumps over the lazy dog.",
        fontsize=60,
        color='white',
        font="Arial",    # Try 'None' if this fails
        size=(800, None),
        method='caption'
    )
    clip.save_frame("test_frame.png")
    print("Clip size:", clip.size)
except Exception as e:
    print("Standalone TextClip error:", e)
