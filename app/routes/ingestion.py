import os
import uuid
from flask import Blueprint, request, jsonify
from ..services.audio_service import AudioService
from ..services.ocr_service import OCRService
from ..services.video_service import VideoService
from ..services.rag_service import RagService
from ..repositories.vector_repo import VectorRepo

ingestion = Blueprint("ingestion", __name__)


repo = VectorRepo()
rag = RagService(repo=repo)  
audio = AudioService()
ocr = OCRService()
video = VideoService()

AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi"}

@ingestion.route("/ingest", methods=["POST"])
def ingest_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    # 1. Validation
    if not file.filename:
        return jsonify({"error": "Empty filename"}), 400
    
# 2. Extract extension and generate a secure temporary file path
    file_extension = os.path.splitext(file.filename)[1].lower()
    unique_id = uuid.uuid4().hex
    temp_path = f"instance/temp_{unique_id}{file_extension}"

    # 3. Save file to storage disk
    os.makedirs("instance", exist_ok=True)
    file.save(temp_path)

    try:
        
        if file_extension in AUDIO_EXTENSIONS:
            content = audio.transcribe_audio(temp_path)
            media_type = "audio"

        elif file_extension in IMAGE_EXTENSIONS:
            content = ocr.extract_text_from_image(temp_path)
            media_type = "image"

        elif file_extension in VIDEO_EXTENSIONS:
            content = video.analyze_frame(temp_path)
            media_type = "video"

        else:
            return jsonify({"error": f"Unsupported file type: {file_extension}"}), 415

        
        rag.add_extracted_content(  
            source_file=file.filename,
            content=content,
            media_type=media_type
        )

        return jsonify({
            "message": "File ingested successfully",
            "filename": file.filename,
            "media_type": media_type
        }), 200

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)