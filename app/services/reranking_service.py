# services/reranking_service.py

from flashrank import Ranker, RerankRequest

class RerankingService:
    def __init__(self, model_name: str = "ms-marco-MiniLM-L-12-v2"):
        self.ranker = Ranker(model_name=model_name)

    def rerank(self, query: str, documents: list[str], top_n: int = 3) -> list[str]:
        if not documents:
            return []

        passages = [{"id": i, "text": doc} for i, doc in enumerate(documents)]
        rerank_request = RerankRequest(query=query, passages=passages)
        results = self.ranker.rerank(rerank_request)

        return [result["text"] for result in results[:top_n]]