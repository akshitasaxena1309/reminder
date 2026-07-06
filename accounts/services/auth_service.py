from accounts.repositories.user_repository import UserRepository
from accounts.utils.password import hash_password, verify_password
from accounts.utils.jwt_handler import create_token

class AuthError(Exception):
    pass

class AuthService:
    def __init__(self):
        self.repo = UserRepository()

    def register(self, dto) -> dict:
        if self.repo.exists_by_email(dto.email):
            raise AuthError("An account with this email already exists.")

        hashed = hash_password(dto.password)
        user = self.repo.create(dto.name, dto.email, hashed)

        token = create_token(user.id, user.email)
        return {"token": token, "user": user.public_dict()}

    def login(self, dto) -> dict:
        user = self.repo.find_by_email(dto.email)
        if not user or not verify_password(dto.password, user.password):
            raise AuthError("Invalid email or password.")

        token = create_token(user.id, user.email)
        return {"token": token, "user": user.public_dict()}

    def get_profile(self, user_id: str) -> dict:
        user = self.repo.find_by_id(user_id)
        if not user:
            raise AuthError("User not found.")
        return user.public_dict()