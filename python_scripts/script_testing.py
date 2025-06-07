from utils import check_create_dated_folder
from google_drive_upload import google_drive_upload, get_gdrive_folder_id
from choose_background import trim_video_file
from create_video import overlay_text_on_video
from pathlib import Path

# output_dir_folder = r'video_projects'
# dates = ["2025-06-30"]  # List of dates. Done so that you can edit all components beforehand, and then loop through and have them
#                         # redone all at once

# for date in dates:
#     dated_output_dir = check_create_dated_folder(date, output_dir_folder) # Finished video output directory
#     final_output_path = f"{dated_output_dir}\\output_video.mp4"

#     video_file_path = Path(rf'C:\Users\miked\OneDrive\Documents\GitHub\WordDrop_Daily\video_projects\{date}\video_components\background.mp4')
#     text_file_path = Path(rf'C:\Users\miked\OneDrive\Documents\GitHub\WordDrop_Daily\video_projects\{date}\video_components\script.txt')

#     trim_video_file(video_file_path, max_duration=15)
#     final_video_path = overlay_text_on_video(date, text_file_path, video_file_path, final_output_path)

#     # Upload the final video to Google Drive
#     gdrive_folder = Path(__file__).parent.parent / output_dir_folder / 'GoogleDriveOutputs'
#     google_drive_upload(final_video_path, gdrive_folder, date)

todays_date = '2025-07-01'
final_video_path = Path(r'C:\Users\miked\OneDrive\Documents\GitHub\WordDrop_Daily\video_projects\2025-07-01\output_video.mp4')

gdrive_folder_id = get_gdrive_folder_id('variables.env')
google_drive_upload(final_video_path, gdrive_folder_id, todays_date)