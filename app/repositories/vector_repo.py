import os
import chromadb


class VectorRepo:
    def __init__(self, db_path: str = "instance/chromadb"):
        os.makedirs(db_path, exist_ok=True)
        self.client = chromadb.PersistentClient(path=db_path)

    def _get_collection(self, media_type: str):
        return self.client.get_or_create_collection(name=media_type)

    def insert_document(self, doc_id: str, content: str, metadata: dict, media_type: str):
        collection = self._get_collection(media_type)
        collection.add(
            documents=[content],
            ids=[doc_id],
            metadatas=[metadata]
        )

    def search_similar(self, query: str, media_type: str, n_results: int = 3):
        collection = self._get_collection(media_type)
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results