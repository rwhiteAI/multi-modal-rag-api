import os
import chromadb
from chromadb.api.types import Metadata


class VectorRepo:
    def __init__(self, db_path: str = "instance/chromadb"):
        os.makedirs(db_path, exist_ok=True)
        self.client = chromadb.PersistentClient(path=db_path)

    def _get_collection(self, media_type: str):
        return self.client.get_or_create_collection(name=media_type)

    def insert_document(self, doc_id: str, chunks: list[str], metadata: dict, media_type: str):
        if not chunks:
            return

        collection = self._get_collection(media_type)

        chunk_ids = [f"{doc_id}_chunk{i}" for i in range(len(chunks))]
        chunk_metadatas: list[Metadata] = [{**metadata, "chunk_index": i} for i in range(len(chunks))]

        collection.add(
            documents=chunks,
            ids=chunk_ids,
            metadatas=chunk_metadatas
        )

    def search_similar(self, query: str, media_type: str, n_results: int = 3):
        collection = self._get_collection(media_type)
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results