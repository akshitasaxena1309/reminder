from accounts.repositories.user_repository import UserRepository
from accounts.utils.password import hash_password, verify_password
from accounts.utils.jwt_handler import create_token
import random
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
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
    
    def forgetPassword(self, dto):
        user = self.repo.find_by_email(dto.email)
        if not user:
            raise AuthError("Invalid email or password.")
        otp = random.randint(100000, 999999)
        try:
            send_mail(
                subject="OTP for Email Verification",
                message=f"Hey,\n\nYour OTP is {otp}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[dto.email],
                fail_silently=False,   
            )
        except Exception as e:
            raise AuthError(f"Failed to send OTP: {str(e)}")
        
        cache.set(
            f"otp:{user.email}",
            otp,
            timeout=300, 
        )
        return {"success": "true"}
        
    def verifyOTP(self, dto):
        user = self.repo.find_by_email(dto.email)
        if not user:
            raise AuthError("Invalid email.")
        
        stored_otp = cache.get(f"otp:{user.email}")
        if stored_otp is None:
            raise AuthError("OTP has expired.")
        
        if str(stored_otp) != str(dto.otp):
            raise AuthError("Invalid OTP.")

        cache.delete(f"otp:{user.email}")
        return {
            "message": "OTP verified successfully."
        }

    def updatePassword(self, dto):
        user = self.repo.find_by_email(dto.email)
        if not user:
            raise AuthError("Invalid email.")
        hashed_password = hash_password(dto.password)
        self.repo.update_password(user.id, hashed_password)
        return {
            "message": "Password updated successfully."
        }
        

    def get_profile(self, user_id: str) -> dict:
        user = self.repo.find_by_id(user_id)
        if not user:
            raise AuthError("User not found.")
        return user.public_dict()