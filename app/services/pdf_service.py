# services/pdf_service.py

import os
from pypdf import PdfReader

class PdfService:
    def extract_text_from_pdf(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found at: {file_path}")

        print(f"[PdfService] Extracting text from: {file_path}...")
        reader = PdfReader(file_path)

        text_parts = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

        return "\n".join(text_parts).strip()