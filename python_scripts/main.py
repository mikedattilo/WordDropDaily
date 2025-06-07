from generate_vocab_word import initialize_groq_client, generate_vocab_word, check_vocab_word
from utils import get_todays_date, check_api_key, load_api_key
from choose_background import get_background_video, video_resolution_check, trim_video_file
from choose_background import get_stock_media_files, get_stock_media_path
from create_video import overlay_text_on_video
from google_drive_upload import google_drive_upload, get_gdrive_folder_id
from utils import save_string_as_txt, save_background_video
from utils import check_create_dated_folder, check_create_components_folder
from datetime import datetime, timedelta

def main():
    # Establish all toggles
    date_toggle = 1 # 0: Use today's actual date / 1: Use a specific date entered below
    script_toggle = 0 # 0: Generate script (Groq API) / 1: Use existing script (stored .txt file)
    background_toggle = 0 # 0: Use Pexels API / 1: Random saved stock media video / 2: Specific video file
    loop_toggle = 0 # 0: Generate video for only specified date / 1: Iterate through a specific number of dates
    gdrive_toggle = 0 # 0: Google Drive upload DISABLED / 1: Google Drive upload ENABLED
    
    # Get date to use (see toggle above)
    match date_toggle:
        case 0:
            todays_date = get_todays_date()
        case 1:
            todays_date = '2025-07-01'
    print(f"Date being used: {todays_date}")

    # Check and/or create output directories for final video & video components
    output_dir_folder = r'video_projects'
    dated_output_dir = check_create_dated_folder(todays_date, output_dir_folder) # Finished video output directory
    final_output_path = f"{dated_output_dir}\\output_video.mp4"
    components_output_dir = check_create_components_folder(dated_output_dir, "video_components") # Components output directory
    
    # Get all API keys from the environment
    variables_file = "variables.env"
    env_var_names = ["GROQ_API_KEY", "PEXELS_API_KEY"]

    api_keys = {} # Create empty dictionary to store API keys

    for env_var_name in env_var_names:
        api_key = load_api_key(env_var_name, variables_file) # Load API key from variables.env
        check_api_key(api_key) # Check if the API key is set
    
        key_name = env_var_name.lower() 
        api_keys[key_name] = api_key

    # Initialize Groq client
    groq_client = initialize_groq_client(api_keys["groq_api_key"])

    # Set instructions for the script generation
    instructions = '''
    You are a script writer for a vocabulary word of the day video. Your task is to generate a script that includes
    a vocabulary word, its definition, and an example sentence. The script should be concise and suitable for a general audience.
    The word generated should be interesting and appropriate for a general audience. Should be a single word that is not too 
    common, but also not too obscure. Something that people could actually incorporate into their daily vocabulary.

    Restrictions:
    - Do NOT write "Here is your script:" or any other introductory phrases.
    - Each item (word, definition, sentence) must be on its own line
    - Absolutely NO additional commentary/formatting (no bullets, no extra explanation, no labels like "Word:" or "Definition:")
    - Do NOT include anything other than the three lines specified below. This includes ("Here's your script:" and "Let me know if...")
    - Do NOT add any extra empty lines or spaces between the lines. Script must be exactly three lines long.

    Have the script formatted as follows:
    - The first line should be a vocabulary word of the day (IN ALL CAPS).
    - The second line should be a clear, concise definition of the word
    - The third line should be this word used in a sentence.
    
    Example Output:
    SERENDIPITY
    the occurrence and development of events by chance in a happy or beneficial way
    Ex: A series of small serendipities.
    '''

    while True:
        # Creating folder for todays_date variable
        dated_output_dir = check_create_dated_folder(todays_date, output_dir_folder) # Finished video output directory
        final_output_path = f"{dated_output_dir}\\output_video.mp4"
        components_output_dir = check_create_components_folder(dated_output_dir, "video_components") # Components output directory
        
        # Generate a script (see toggle above)
        match script_toggle:
            case 0:
                while True:
                    script = generate_vocab_word(groq_client, instructions)
                    print(f"Script successfully generated.")
                    if check_vocab_word(script):
                        break
            case 1:
                print("Using existing script for the video...")
                filename = "script.txt"
                script_path = components_output_dir / filename

                with open(script_path, "r", encoding="utf-8") as f:
                    script = f.read()

        # Save the script background video to established file directory
        text_file_path = save_string_as_txt(script, "txt", components_output_dir)  # Path object (do not change this line)

        # Section to get background video
        media_dir = r'stock_media'  # Directory where stock media files are stored
        match background_toggle:
            case 0:
                while True:
                    raw_video_bytes = get_background_video(api_keys["pexels_api_key"])  # Get video bytes from API
                    if video_resolution_check(raw_video_bytes):
                        print("Video resolution is 1080x1920, proceeding with video.")
                        video_file_path = save_background_video(raw_video_bytes, "mp4", components_output_dir)  # Path object
                        trim_video_file(video_file_path, max_duration=15)  # Ensure video is no longer than 15 seconds
                        break
                    else:
                        print("Video resolution is not 1080x1920, trying again...")
            case 1: # Random .mp4 file from stock_media directory
                import random
                video_files = get_stock_media_files(media_dir)     # List of video filenames
                print(f"Selecting random background video from {media_dir}...")
                chosen_video = random.choice(video_files)              # Pick one at random
                video_file_path = get_stock_media_path(chosen_video)   # Get the correct Path object
                # Read the video as bytes
                with open(video_file_path, 'rb') as f:
                    background_video_bytes = f.read()
                save_background_video(background_video_bytes, "mp4", components_output_dir)
            case 2: # Specific .mp4 file from stock_media directory
                specific_background_video = "city_highway.mp4"  # Specify a specific video file
                video_file_path = get_stock_media_path(specific_background_video)   # Get the correct Path object
                print(f"Using specific background video {video_file_path} from {media_dir}")
                # Read the video as bytes
                with open(video_file_path, 'rb') as f:
                    background_video_bytes = f.read()
                save_background_video(background_video_bytes, "mp4", components_output_dir)

        # Merge contents and create the final video
        final_video_path = overlay_text_on_video(todays_date, text_file_path, video_file_path, final_output_path)

        # Upload the final video to Google Drive
        match gdrive_toggle:
            case 0:
                print("Google Drive upload DISABLED.")
                continue
            case 1: # NEEDS WORK, NOT FINISHED
                print("Google Drive upload ENABLED.")
                gdrive_folder_id = get_gdrive_folder_id('variables.env')
                google_drive_upload(final_video_path, gdrive_folder_id, todays_date)

        match loop_toggle:
            case 0:
                print('Loop toggle DISABLED.')
                quit()
            case 1:
                date_obj = datetime.strptime(todays_date, '%Y-%m-%d')
                next_day = date_obj + timedelta(days=1)
                next_day_str = next_day.strftime('%Y-%m-%d')
                print(f"Processing date: {todays_date} -> Next day: {next_day_str}")
                if next_day_str == '2025-07-01':
                    print("Reached the end date, exiting loop.")
                    break
                todays_date = next_day_str

if __name__ == "__main__":
    main()