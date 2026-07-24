# services/chunking_service.py

class ChunkingService:
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, content: str) -> list[str]:
        words = content.split()
        if not words:
            return []

        chunks = []
        start = 0
        while start < len(words):
            end = start + self.chunk_size
            chunks.append(" ".join(words[start:end]))
            if end >= len(words):
                break
            start = end - self.chunk_overlap

        return chunks