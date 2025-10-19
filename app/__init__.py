# app/__init__.py
from flask import Flask, jsonify
from app.routes.tasks import tasks_bp
from app.routes.health import health_bp
# ✅ Phase 2: Import services for dependency injection
from app.services.task_service import TaskService
from app.services.task_storage import task_storage


def create_app(service=None):
    """
    US015 - `tests/error/test_error_handling.py`
    """
    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(tasks_bp)
    app.register_blueprint(health_bp)

    # Dependency Injection: use provided service or default TaskService
    if service is None:
        service = TaskService(task_storage)
    app.task_service = service


    # NOTE FOR STUDENTS:
    # These error handlers are registered globally when the Flask app is created.
    # This is a feature of Flask: once registered, they automatically apply to all routes in the app.
    # You do NOT need to reference or call them in your route files—they are always active.

    # Global error handler for 400 Bad Request
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad Request"}), 400

    # Global error handler for 404 Not Found
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found"}), 404

    return app