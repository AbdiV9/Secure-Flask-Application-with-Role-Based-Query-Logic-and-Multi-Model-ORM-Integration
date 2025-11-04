from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from sqlalchemy import text
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from sqlalchemy import text
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Temporary feedback for testing form submission
        if username and password:
            current_app.logger.info(
                f"[LOGIN SUCCESS] Username: {username}, IP: {request.remote_addr}, "
                f"Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            flash(f"Form submitted with username: {username}")
            return redirect(url_for('main.dashboard'))
        else:
            current_app.logger.warning(
                f"[LOGIN FAILED] Username: {username}, IP: {request.remote_addr}, "
                f"Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            flash("Please enter both username and password.")

    return render_template('login.html')

@main.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

@main.route('/search', methods=['POST'])
def search():
    search_term = request.form.get('search', '').strip()
    results = []

    if not search_term:
        flash("Please enter a search term.", "warning")
        return render_template('dashboard.html', results=results)

    sql = text("""
        SELECT * FROM posts
        WHERE title LIKE :term OR content LIKE :term
    """)

    params = {"term": f"%{search_term}%"}

    try:
        from . import db
        results = db.session.execute(sql, params).fetchall()

        # Log successful query execution
        current_app.logger.info(
            f"[SEARCH QUERY] User: test_user | SQL: {sql.text} | Params: {params} | "
            f"IP: {request.remote_addr} | Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}"
        )

    except Exception as e:
        current_app.logger.warning(
            f"[SEARCH ERROR] SQL: {sql.text} | Params: {params} | Error: {str(e)} | "
            f"IP: {request.remote_addr} | Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        flash("Error processing search query.", "danger")

    return render_template('dashboard.html', results=results)


