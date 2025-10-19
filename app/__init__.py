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
    """

    import os
    print(f"[DEBUG] Flask app created. TESTING={os.getenv('TESTING')}")
    Sprint 4: Database-wired Flask application
    """
    app = Flask(__name__)

    # 🔧 Database Setup (only if no service provided via dependency injection)
    if service is None:
        # Use file-based database for CI/testing and development/production
        import os
        is_testing = os.getenv("TESTING") == "true" or os.getenv("CI") == "true"
        db_path = "/tmp/tasks.db" if is_testing else "./tasks.db"
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

    # Import and register UI Blueprint (imported here to avoid circular imports)
    from app.routes.ui import ui_bp
    app.register_blueprint(ui_bp)  # ✅ Enables /tasks/new route for web form

    # Global error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad Request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found"}), 404

    return app