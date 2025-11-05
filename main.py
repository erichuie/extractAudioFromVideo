from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.background import BackgroundTasks
from moviepy import VideoFileClip
from dotenv import load_dotenv
import uuid
import os
import boto3

app = FastAPI(
    version="1.0.0"
)

load_dotenv()

S3_ACCESS_KEY = os.environ['AWS_ACCESS_KEY_ID']
S3_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
S3_REGION = os.environ['AWS_DEFAULT_REGION']
S3_BUCKET = os.environ['S3_BUCKET_NAME']

# Create S3 client
s3 = boto3.client("s3", aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_ACCESS_KEY, region_name=S3_REGION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Hello, World!"}

def cleanup_file(file_path: str):
    """Deletes the specified file."""
    if os.path.exists(file_path):
        os.remove(file_path)

@app.post("/video/extract-audio")
async def extract_audio_from_video(video_file: UploadFile = File(...), start_time: int = 0,background_tasks: BackgroundTasks = None):
    """Accepts a video mp4 file and returns the audio"""
    input_filename = f"temp_{uuid.uuid4()}_{video_file.filename}"
    new_filename, extension = os.path.splitext(video_file.filename)
    output_mp3_filename = f"{new_filename}.mp3"

    with open(input_filename, "wb") as file:
        file.write(await video_file.read())

    clip = VideoFileClip(input_filename)
    # subclip = clip.subclip(start_time, clip.duration)
    # subclip.audio.write_audiofile(output_mp3_filename)
    clip.audio.write_audiofile(output_mp3_filename)
    clip.close()
    # subclip.close()

    s3.upload_file(output_mp3_filename, S3_BUCKET, f"audio/{output_mp3_filename}")
    cleanup_file(input_filename)
    cleanup_file(output_mp3_filename)

    return {
        "result": "success",
        "message": "Audio extracted successfully",
        "data": {
            "audio_path": f"https://{S3_BUCKET}.s3.amazonaws.com/audio/{output_mp3_filename}"
        }
    }