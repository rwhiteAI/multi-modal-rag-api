import os
from flask import Flask
from app.routes.ingestion import ingestion
from app.routes.query import query

def create_app():
    app = Flask(__name__)

    os.makedirs("instance", exist_ok=True)

    # Register blueprints
    app.register_blueprint(ingestion)
    app.register_blueprint(query)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)