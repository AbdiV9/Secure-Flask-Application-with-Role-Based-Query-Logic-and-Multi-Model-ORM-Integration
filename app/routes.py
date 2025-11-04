from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from sqlalchemy import text
from datetime import datetime
import logging

from . import db
from .models import User, Post

main = Blueprint('main',__name__)

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def get_current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None

@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        ip = request.remote_addr

        if not username or not password:
            flash("Please enter both username and password.")
            return render_template('login.html')

        user = User.query.filter_by(username = username, password=password).first()

        if user:
            # Successful login
            session['user_id'] = user.id
            session['role'] = user.role
            flash(f"Welcome, {user.username} ({user.role})!")
            logging.info(f"Successful login: username={username}, role={user.role}, ip={ip}")
            return redirect(url_for('main.dashboard'))
        else:
            # Failed login
            flash("Invalid username or password.")
            logging.warning(f"Failed login attempt: username={username}, ip={ip}, time={datetime.utcnow()}")
            return render_template('login.html')

    return render_template('login.html')

@main.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    user = get_current_user()
    if not user:
        flash("Please log in first.")
        return redirect(url_for('main.login'))

    role = user.role

    # --- Role-based Query Logic ---
    if role == 'admin':
        # Admin sees all posts
        posts = Post.query.join(User, Post.author_id == User.id)\
                          .add_columns(Post.id, Post.title, Post.content, User.username, User.role)\
                          .all()

    elif role == 'moderator':
        # Moderator sees all posts but limited fields
        posts = Post.query.join(User, Post.author_id == User.id)\
                          .add_columns(Post.id, Post.title, User.username)\
                          .all()

    else:  # Regular user
        # User sees only their own posts
        posts = Post.query.filter_by(author_id=user.id).all()

    return render_template('dashboard.html', posts=posts, user=user)

