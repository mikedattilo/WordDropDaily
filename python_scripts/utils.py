# Function to load API key from variables.evv
def load_api_key(env_var_name, variables_file):
    from pathlib import Path
    from dotenv import load_dotenv
    import os
    print(f"Loading {env_var_name}...")
    env_path = Path(__file__).parent / variables_file
    if not env_path.exists():
        raise FileNotFoundError(f"Environment file {variables_file} not found.")
    load_dotenv(dotenv_path=env_path)
    return os.getenv(env_var_name)

# Function to check if an API key is set
def check_api_key(api_key):
    if not api_key:
        raise ValueError("API key is missing. Please provide a valid API key.")
    print("API key is set.")

# Function to get todays date
def get_todays_date():
    import datetime
    return str(datetime.date.today().strftime("%Y-%m-%d"))

def check_create_dated_folder(todays_date: str, output_dir_path: str):
    from pathlib import Path

    output_dir = Path(output_dir_path)
    dated_folder_path = output_dir / todays_date

    print(f"Checking for folder: {dated_folder_path}")
    if not dated_folder_path.exists():
        print(f"Folder '{todays_date}' does not exist in '{output_dir}'. Creating '{dated_folder_path}'")
        dated_folder_path.mkdir(parents=True, exist_ok=True)
    else:
        print(f"Folder {dated_folder_path} already exists.")

    return dated_folder_path

def check_create_components_folder(dated_output_dir, components_folder: str):
    from pathlib import Path

    base_path = Path(dated_output_dir)
    components_path = base_path / components_folder

    print(f"Checking for folder: {components_path}")
    if not components_path.exists():
        print(f"Folder '{components_folder}' does not exist in '{base_path}'. Creating '{components_path}'")
        components_path.mkdir(parents=True, exist_ok=True)
    else:
        print(f"Folder {components_path} already exists.")
    
    return components_path

def save_string_as_txt(content, filetype="txt", file_dir=None):
    file_path = file_dir / f"script.{filetype}"
    with file_path.open("w", encoding="utf-8") as file:
        file.write(content)
    print(f"Script successfully saved to {file_path}")
    return file_path # Path object

def save_background_video(video_bytes, filetype="mp4", file_dir=None):
    file_path = file_dir / f"background.{filetype}"
    with file_path.open("wb") as file:
        file.write(video_bytes)
    print(f"Background video successfully saved to {file_path}")
    return file_path # Path object
