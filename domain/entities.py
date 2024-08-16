class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

class Post:
    def __init__(self, id, title, content, user_id):
        self.id = id
        self.title = title
        self.content = content
        self.user_id = user_id

class Comment:
    def __init__(self, id, content, user_id, post_id):
        self.id = id
        self.content = content
        self.user_id = user_id
        self.post_id = post_id
