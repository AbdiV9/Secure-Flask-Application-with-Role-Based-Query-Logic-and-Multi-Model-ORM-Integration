# app.py
from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.secret_key = "supersecretkey"  # replace with secure key in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------------------------
# Logging Setup
# ---------------------------
handler = RotatingFileHandler("app.log", maxBytes=1_000_000, backupCount=3)
logging.basicConfig(level=logging.INFO, handlers=[handler],
                    format="%(asctime)s - %(levelname)s - %(message)s")

# ---------------------------
# Database Models
# ---------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, mod, user
    posts = db.relationship('Post', backref='author', lazy=True)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# ---------------------------
# Routes
# ---------------------------
@app.route('/')
def index():
    return redirect(url_for('login'))

# ---------------------------
# Login Route
# ---------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        ip = request.remote_addr

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['role'] = user.role
            session['username'] = user.username
            logging.info(f"SUCCESSFUL login by user: {username}, IP: {ip}")
            return redirect(url_for('dashboard'))
        else:
            logging.warning(f"FAILED login attempt: {username}, IP: {ip}")
            return "Login failed", 401

    return render_template('login.html')

# ---------------------------
# Dashboard / Search
# ---------------------------
@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    role = session['role']
    search_term = request.args.get('search', '')

    logging.info(f"{session['username']} searched for term: '{search_term}'")

    # Secure raw SQL search
    sql = """
        SELECT posts.id, posts.title, posts.content, users.username
        FROM posts
        JOIN users ON posts.author_id = users.id
        WHERE posts.title LIKE :term OR posts.content LIKE :term
    """
    term = f"%{search_term}%"
    results = db.session.execute(sql, {"term": term}).fetchall()
    logging.info(f"Search returned {len(results)} posts")

    # Apply role-based filtering
    if role == 'user':
        results = [r for r in results if r.username == session['username']]
    elif role == 'mod':
        results = [dict(id=r.id, title=r.title) for r in results]  # limited fields
    elif role == 'admin':
        results = [dict(id=r.id, title=r.title, content=r.content, author=r.username) for r in results]

    return render_template('dashboard.html', posts=results, role=role)

# ---------------------------
# Logout
# ---------------------------
@app.route('/logout')
def logout():
    logging.info(f"{session.get('username')} logged out")
    session.clear()
    return redirect(url_for('login'))

# ---------------------------
# Initialize Database with Sample Data
# ---------------------------
@app.before_first_request
def create_tables():
    db.create_all()
    if not User.query.first():
        # Create sample users
        users = [
            User(username="admin", password_hash=generate_password_hash("admin123"), role="admin"),
            User(username="mod1", password_hash=generate_password_hash("mod123"), role="mod"),
            User(username="user1", password_hash=generate_password_hash("user123"), role="user")
        ]
        db.session.add_all(users)
        db.session.commit()

        # Create sample posts
        posts = [
            Post(title="Admin Post", content="All details visible", author_id=1),
            Post(title="Mod Post", content="Limited details", author_id=2),
            Post(title="User Post", content="Only own visible", author_id=3)
        ]
        db.session.add_all(posts)
        db.session.commit()

# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
