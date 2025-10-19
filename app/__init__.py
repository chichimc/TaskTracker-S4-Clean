# app/__init__.py (Database-wired version)

from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.sqlalchemy_task import Base  # ✅ Correct import
from app.repositories.database_task_repository import DatabaseTaskRepository
from app.services.task_service import TaskService
from app.routes.tasks import tasks_bp
from app.routes.health import health_bp


# UI blueprint imported inside create_app to avoid circular imports

def create_app(service=None):
    """Create and configure the Flask application."""

    app = Flask(__name__)

    # 🔧 Database Setup (only if no service provided via dependency injection)
    if service is None:
        # Use file-based database for CI/testing and development/production
        import os
        import tempfile
        # Cross-platform database path for testing mode:
        # Uses tempfile.gettempdir() to ensure compatibility on Windows, Mac, and Linux.
        # Avoids hardcoded '/tmp/tasks.db' which only works on Linux/macOS.
        is_testing = os.getenv("TESTING") == "true" or os.getenv("CI") == "true"
        if is_testing:
            temp_dir = tempfile.gettempdir()
            db_path = os.path.join(temp_dir, "tasks.db")
        else:
            db_path = "./tasks.db"
        print(f"[DEBUG] TESTING={os.getenv('TESTING')}, CI={os.getenv('CI')}, db_path={db_path}")
        engine = create_engine(f"sqlite:///{db_path}")

        # Create session factory
        Session = sessionmaker(bind=engine)

        # Create database tables
        Base.metadata.create_all(engine)  # Creates database and tables
        print("✅ Database tables created by Base.metadata.create_all(engine)")

        # Wire up the repository and service
        repo = DatabaseTaskRepository(Session)
        service = TaskService(repo)

        # Store engine reference for cleanup
        app.database_engine = engine

        # Register cleanup function
        @app.teardown_appcontext
        def cleanup_db_connections(exception):
            """Ensure database connections are properly closed."""
            pass  # Sessions are closed in repository methods

        # Register app cleanup for engine disposal
        import atexit
        def dispose_engine():
            if hasattr(app, 'database_engine'):
                app.database_engine.dispose()

        atexit.register(dispose_engine)

    # Inject the service into the app
    app.task_service = service

    # Register Blueprints
    app.register_blueprint(tasks_bp)
    app.register_blueprint(health_bp)

    # Global error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad Request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found"}), 404

    return app