import os
import whisper
from typing import Any

class AudioService:
    def __init__(self, model_name: str = "base"):
        
        self.model = whisper.load_model(model_name)

    def transcribe_audio(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found at: {file_path}")
            
        print(f"[AudioService] Transcribing file: {file_path}...")
        
        try:
            
            result: Any = self.model.transcribe(file_path)
            
            
            return str(result.get("text", "")).strip() if isinstance(result, dict) else ""
            
        except Exception as e:
            print(f"[AudioService] Error during processing or decoding: {e}")
            raise RuntimeError(f"Audio processing failed: Core transcriber error.")