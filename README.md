# WordDropDaily

WordDropDaily generates daily short-form vocabulary videos using Python scripts.

## Directory overview

```
branding/           image assets used in videos
python_scripts/     main scripts and utilities
stock_media/        example background videos
video_projects/     generated output videos
used_words.txt      record of previously used words
```

The optional `documentation` folder contains a business plan document.

## Setup

1. **Install Python dependencies**
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install moviepy==1.0.3 python-dotenv requests "Pillow<10" groq pydrive \
       google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```
   These packages mirror the commands in `python_scripts/requirements.txt`.

2. **Environment variables**

   Create a file named `variables.env` inside `python_scripts/` containing your
   API keys:

   ```env
   GROQ_API_KEY=your_groq_key
   PEXELS_API_KEY=your_pexels_key
   # Optional: required only if you enable Google Drive uploads
   GDRIVE_FOLDER_ID=your_drive_folder_id
   ```

   If Google Drive uploads are enabled, place a service account JSON credential
   file at `credentials/service_account.json`.

## Running

Execute the main script from the repository root:

```bash
python python_scripts/main.py
```

Edit the toggles at the beginning of `main.py` to control the behavior, such as
whether scripts are generated or loaded from file, which background source is
used, date handling, looping over multiple days, and Google Drive upload.

When the script finishes, the final video and its components are saved inside a
`video_projects/<YYYY-MM-DD>` folder. If enabled, the video is also uploaded to
the configured Google Drive folder.

## Notes

The repository includes a portable Windows build of ImageMagick in
`python_scripts/ImageMagick-*` for rendering text. The code relies on this copy
and will fail if it is missing.

Enjoy creating vocabulary videos!
