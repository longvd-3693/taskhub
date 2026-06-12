from app.repositories.user import UserRepository
from app.services.user import UserService


user_repository = UserRepository()


def get_user_service():
    return UserService(user_repository)