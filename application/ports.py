from abc import ABC, abstractmethod

class UserRepositoryPort(ABC):
    @abstractmethod
    def get_user_by_username(self, username):
        pass

    @abstractmethod
    def save_user(self, user):
        pass

class PostRepositoryPort(ABC):
    @abstractmethod
    def get_all_posts(self):
        pass

    @abstractmethod
    def get_post_by_id(self, post_id):
        pass

    @abstractmethod
    def save_post(self, post):
        pass
