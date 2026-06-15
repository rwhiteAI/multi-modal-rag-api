import os
import easyocr
from typing import Any

class OCRService:
    def __init__(self, languages: list[str] | None = None):
    
        self.reader = easyocr.Reader(languages or ['en'], gpu=False)

    def extract_text_from_image(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Image file not found at: {file_path}")
            
        print(f"[OCRService] Extracting text from: {file_path}...")
        results: Any = self.reader.readtext(file_path, detail=0)
        
        
        if isinstance(results, list):
            cleaned = [str(text) for text in results]
            return " ".join(cleaned).strip()
        else:
            return ""