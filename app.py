from flask import Flask, render_template, redirect, url_for, request, session, g
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def index():
    db = get_db()
    cur = db.execute('SELECT p.id, p.title, p.content, u.username FROM posts p JOIN users u ON p.user_id = u.id')
    posts = cur.fetchall()
    return render_template('index.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        db = get_db()
        db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        db.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cur = db.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cur.fetchone()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('index'))
        else:
            return 'Invalid credentials'

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user_id = session['user_id']

        db = get_db()
        db.execute('INSERT INTO posts (title, content, user_id) VALUES (?, ?, ?)', (title, content, user_id))
        db.commit()
        return redirect(url_for('index'))
    return render_template('create_post.html')

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    db = get_db()
    cur = db.execute('SELECT p.id, p.title, p.content, u.username FROM posts p JOIN users u ON p.user_id = u.id WHERE p.id = ?', (post_id,))
    post = cur.fetchone()

    cur = db.execute('SELECT c.content, u.username FROM comments c JOIN users u ON c.user_id = u.id WHERE c.post_id = ?', (post_id,))
    comments = cur.fetchall()

    if request.method == 'POST':
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        content = request.form['content']
        user_id = session['user_id']
        db.execute('INSERT INTO comments (content, user_id, post_id) VALUES (?, ?, ?)', (content, user_id, post_id))
        db.commit()
        return redirect(url_for('post', post_id=post_id))

    return render_template('post.html', post=post, comments=comments)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
