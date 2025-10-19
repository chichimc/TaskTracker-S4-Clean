# app/routes/ui.py
from flask import Blueprint, render_template, request, redirect, url_for, current_app

"""
📚 UI ROUTES - WEB INTERFACE FOR TASK MANAGEMENT:

🎯 BLUEPRINT PATTERN:
This file uses Flask's Blueprint pattern to organize related routes.
Blueprints allow modular application structure and URL prefixing.

🔄 ROUTE PATTERNS THAT WILL BE DEMONSTRATED SPRINT 4:
- GET routes: Display forms and data (task_form, show_tasks, task_report)
- POST routes: Process form submissions (create_task, delete_task, complete_task)
- Redirects: Post-Redirect-Get pattern for form handling
- URL parameters: Dynamic routes with <int:task_id>

🔗 BACKEND INTEGRATION:
All routes use current_app.task_service for business logic,
maintaining separation between web layer and business layer.
"""

ui_bp = Blueprint("ui", __name__)


@ui_bp.route("/tasks/new", methods=["GET"])
def task_form():
    return render_template("add_task.html")


@ui_bp.route("/tasks/new", methods=["POST"])
def task_submit():
    title = request.form.get("title")
    description = request.form.get("description")
    current_app.task_service.add_task(title, description)
    return redirect(url_for("ui.task_form"))