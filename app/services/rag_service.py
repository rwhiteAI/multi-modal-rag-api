import os
from app.repositories.vector_repo import VectorRepo
import requests

class RagService:
    
    def __init__(self, repo: VectorRepo, llm="llama3", ollama_url="http://localhost:11434"):
        self.repo = repo
        self.llm = llm
        self.api_url = f"{ollama_url}/api/generate"

    def add_extracted_content(self, source_file: str, content: str, media_type: str):
        if not content.strip():
            return
        
        base_name = os.path.basename(source_file)
        doc_id = f"{base_name}_{media_type}"
        metadata = {"source_file": source_file, "media_type": media_type}

        self.repo.insert_document(doc_id=doc_id, content=content, metadata=metadata, media_type=media_type)


    
    
    
    
    def answer_query(self, user_query: str, media_type: str | None = None):
        collections_to_search = [media_type] if media_type else ["audio", "image", "video"]
        combined_documents = []

        for target_type in collections_to_search:
            try:
                search_results = self.repo.search_similar(user_query, media_type=target_type, n_results=3)
                if search_results:
                    docs_list = search_results.get("documents") or []
                    if docs_list and docs_list[0]:
                        combined_documents.extend([doc for doc in docs_list[0] if doc])
            except Exception:
                continue

        context_str = "\n---\n".join(combined_documents) if combined_documents else "No context found."
        
        prompt = f"""You are a helpful, local assistant. Answer the user's question accurately 
using ONLY the provided local context retrieved from multi-modal files. If the context 
doesn't contain the answer, state that you don't know.

### CONTEXT:
{context_str}

### QUESTION:
{user_query}

### ANSWER:"""

        payload = {"model": self.llm, "prompt": prompt, "stream": False}

        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Could not connect to Ollama: {e}")