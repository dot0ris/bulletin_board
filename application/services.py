class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def register_user(self, username, password):
        user = self.user_repository.get_user_by_username(username)
        if user:
            raise Exception("User already exists")
        hashed_password = generate_password_hash(password)
        user = User(id=None, username=username, password=hashed_password)
        self.user_repository.save_user(user)

    def authenticate_user(self, username, password):
        user = self.user_repository.get_user_by_username(username)
        if user and check_password_hash(user.password, password):
            return user
        return None

class PostService:
    def __init__(self, post_repository):
        self.post_repository = post_repository

    def create_post(self, title, content, user_id):
        post = Post(id=None, title=title, content=content, user_id=user_id)
        self.post_repository.save_post(post)
        return post

    def get_all_posts(self):
        return self.post_repository.get_all_posts()
