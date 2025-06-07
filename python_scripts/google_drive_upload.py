# Function to load google drive folder id from certain file
def get_gdrive_folder_id(env_file):
    from dotenv import load_dotenv
    import os

    load_dotenv(env_file)
    return os.getenv('GDRIVE_FOLDER_ID')

# Function to upload only the output file to Google Drive
def google_drive_upload(output_path, gdrive_folder_id, todays_date):
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from pathlib import Path
    
    SERVICE_ACCOUNT_FILE = Path(__file__).parent.parent / 'credentials' / 'service_account.json'
    SCOPES = ['https://www.googleapis.com/auth/drive.file']

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {
        'name': f"{todays_date}_{Path(output_path).name}",
        'parents': [gdrive_folder_id]
    }
    media = MediaFileUpload(output_path, resumable=True)

    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink'
    ).execute()

    print(f"Uploaded file with ID: {file.get('id')}")
    print(f"View it at: {file.get('webViewLink')}")