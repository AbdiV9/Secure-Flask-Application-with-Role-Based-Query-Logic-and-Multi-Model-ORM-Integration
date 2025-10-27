from datetime import datetime
from . import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(220), nullable=False)
    role = db.Column(db.String(100), unique=True, nullable=False)

    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return f"<User ID={self.id} Username={self.username} Role = {self.role}>"

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Post id={self.id} title={self.title[:20]}>"

    def seed_data(self):

        if User.query.count() == 0:
            admin = User(username = 'admin ' , email = 'admin@example.ac.uk' , password = '<admin12>' ,  role = 'admin')
            moderator = User(username = 'moderator' , email ='moderator@example.ac.uk' , password = '<Moderator12>' , role = 'moderator')
            test1 = User(username = 'Test1',email = 'Test1@exapmle.ac.uk',password = '<tester123>', role = 'test')
            test2 = User(username = 'Test2', email = 'Test2@exapmle.ac.uk',password = '<tester456>', role = 'test')

            db.session.add([admin, moderator, test1, test2])
            db.session.commit()

        if Post.query.count() == 0:
            post1 = Post(title = 'Welcome', content = 'Post 1 content', author_id = 1)
            post2 = Post(title = 'Moderator', content = 'Post 2 content', author_id = 2)
            post3 = Post(title = 'Thoughts', content = 'Post 3 content', author_id = 3)
            post4 = Post(title = 'User Post', content = 'Post 4 content', author_id = 4)

            db.session.add([post1, post2, post3, post4])
            db.session.commit()

        def seed_data():
            return None


