import sqlite3
from domain.entities import User, Post
from application.ports import UserRepositoryPort, PostRepositoryPort

DATABASE = 'database.db'

def get_db():
    db = sqlite3.connect(DATABASE)
    return db

class SQLiteUserRepository(UserRepositoryPort):
    def get_user_by_username(self, username):
        db = get_db()
        cur = db.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cur.fetchone()
        if row:
            return User(id=row[0], username=row[1], password=row[2])
        return None

    def save_user(self, user):
        db = get_db()
        db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (user.username, user.password))
        db.commit()

class SQLitePostRepository(PostRepositoryPort):
    def get_post_by_id(self, post_id):
        pass

    def get_all_posts(self):
        db = get_db()
        cur = db.execute('SELECT * FROM posts')
        rows = cur.fetchall()
        return [Post(id=row[0], title=row[1], content=row[2], user_id=row[3]) for row in rows]

    def save_post(self, post):
        db = get_db()
        db.execute('INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)', (post.title, post.content, post.user_id))
        db.commit()
