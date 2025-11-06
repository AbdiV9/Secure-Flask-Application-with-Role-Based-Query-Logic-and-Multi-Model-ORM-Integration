from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func # Import func for seeding

# Models will be defined here during implementation.
# No fields or logic are included in starter code.
class User(db.Model):
    __tablename__ = 'users'
   # Initializes the max characters whether it is unique and whether it is null
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    # Defines the relationship between User and Post models
    posts = db.relationship('Post', backref='author', lazy='dynamic')

#  Method that sets the users password
def set_password(self, password):
    self.password_hash = generate_password_hash(password)

# Method to check if an input password matched the stored hash
# It compares the input password after being hashed with the stored hash
def check_password(self, password):
    return check_password_hash(self.password_hash, password)

# Representation method: Defines how a User object is displayed when printed
def __repr__(self):
    return f"<User {self.username} ({self.role})>"


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(120), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


def __repr__(self):
    return f"<Post {self.title} ({self.author_id})>"

def seed_data():

    if User.query.count() == 0:
        # Sample users with different roles
        admin = User(username='admin', email='admin@example.com', password='admin123', role='admin')
        moderator = User(username='mod1', email='mod1@example.com', password='mod123', role='moderator')
        user1 = User(username='user1', email='user1@example.com', password='user123', role='user')
        user2 = User(username='user2', email='user2@example.com', password='user456', role='user')

        db.session.add_all([admin, moderator, user1, user2])
        db.session.commit()

    if Post.query.count() == 0:
        # Sample posts authored by different users
        post1 = Post(title='Welcome Post', content='This is the first post.', author_id=1)
        post2 = Post(title='Moderator Update', content='Moderator insights here.', author_id=2)
        post3 = Post(title='User Thoughts', content='User1 shares ideas.', author_id=3)
        post4 = Post(title='Another User Post', content='User2 contributes.', author_id=4)

        db.session.add_all([post1, post2, post3, post4])
        db.session.commit()


