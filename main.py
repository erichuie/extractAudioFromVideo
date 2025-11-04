from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.background import BackgroundTasks
from moviepy import VideoFileClip
import uuid
import os

app = FastAPI(
    version="1.0.0"
)

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
async def extract_audio_from_video(video_file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    """Accepts a video mp4 file and returns the audio"""
    input_filename = f"temp_{uuid.uuid4()}_{video_file.filename}"
    output_mp3_filename = f"{os.path.splitext(input_filename)[0]}.mp3"

    with open(input_filename, "wb") as file:
        file.write(await video_file.read())

    clip = VideoFileClip(input_filename)
    clip.audio.write_audiofile(output_mp3_filename)
    clip.close()

    background_tasks.add_task(cleanup_file, input_filename)
    background_tasks.add_task(cleanup_file, output_mp3_filename)

    return FileResponse(
        output_mp3_filename,
        media_type="audio/mpeg",
        filename=os.path.basename(output_mp3_filename),
        background=background_tasks
    )