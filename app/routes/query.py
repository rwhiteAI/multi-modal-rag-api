from flask import Blueprint, request, jsonify
from app.services.rag_service import RagService
from app.repositories.vector_repo import VectorRepo

query = Blueprint("query", __name__)

repo = VectorRepo()
rag = RagService(repo=repo)

@query.route("/query", methods=["POST"])
def query_knowledge_base():
    data = request.get_json()

    if not data or "question" not in data:
        return jsonify({"error": "No question provided"}), 400

    question = data["question"].strip()
    if not question:
        return jsonify({"error": "Question cannot be empty"}), 400

    media_type = data.get("media_type")
    if media_type:
        media_type = media_type.strip().lower()

    answer = rag.answer_query(user_query=question, media_type=media_type)

    return jsonify({
        "question": question,
        "media_type_filtered": media_type or "all",
        "answer": answer
    }), 200