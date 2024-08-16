from flask import Flask, render_template, redirect, url_for, request, session
from application.services import UserService, PostService
from adapters.db_sqlite_adapter import SQLiteUserRepository, SQLitePostRepository

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Repositories and Services
user_repository = SQLiteUserRepository()
post_repository = SQLitePostRepository()
user_service = UserService(user_repository)
post_service = PostService(post_repository)

@app.route('/')
def index():
    posts = post_service.get_all_posts()
    return render_template('index.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_service.register_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = user_service.authenticate_user(username, password)
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
