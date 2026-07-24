import os
import uuid
from flask import Blueprint, request, jsonify
from ..services.audio_service import AudioService
from ..services.ocr_service import OCRService
from ..services.video_service import VideoService
from ..services.pdf_service import PdfService
from ..services.rag_service import RagService
from ..services.chunking_service import ChunkingService
from ..services.reranking_service import RerankingService
from ..repositories.vector_repo import VectorRepo

ingestion = Blueprint("ingestion", __name__)


repo = VectorRepo()
chunker = ChunkingService()
reranker = RerankingService()
rag = RagService(repo=repo, chunker=chunker, reranker=reranker)
audio = AudioService()
ocr = OCRService()
video = VideoService()
pdf = PdfService()

AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi"}
PDF_EXTENSIONS = {".pdf"}

@ingestion.route("/ingest", methods=["POST"])
def ingest_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if not file.filename:
        return jsonify({"error": "Empty filename"}), 400

    file_extension = os.path.splitext(file.filename)[1].lower()
    unique_id = uuid.uuid4().hex
    temp_path = f"instance/temp_{unique_id}{file_extension}"

    os.makedirs("instance", exist_ok=True)
    file.save(temp_path)

    try:

        if file_extension in AUDIO_EXTENSIONS:
            content = audio.transcribe_audio(temp_path)
            media_type = "audio"

        elif file_extension in IMAGE_EXTENSIONS:
            ocr_text = ocr.extract_text_from_image(temp_path)
            caption = video.analyze_frame(temp_path, prompt="Describe what is shown in this image in detail.")
            content = f"{caption}\n{ocr_text}".strip()
            media_type = "image"

        elif file_extension in VIDEO_EXTENSIONS:
            content = video.analyze_frame(temp_path)
            media_type = "video"

        elif file_extension in PDF_EXTENSIONS:
            content = pdf.extract_text_from_pdf(temp_path)
            media_type = "document"

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
