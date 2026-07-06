from django.urls import path
from accounts.controllers import auth_controller as AuthController

urlpatterns = [
    # Pages
    path("", AuthController.login_page, name="login_page"),
    path("register/", AuthController.register_page, name="register_page"),
    path("dashboard/", AuthController.dashboard_page, name="dashboard_page"),
    path("forget-password/", AuthController.forget_passowrd_page, name="forget_password_page"),

    # API
    path("auth/register/", AuthController.register, name="api_register"),
    path("auth/login/", AuthController.login, name="api_login"),
    path("auth/me/", AuthController.me, name="api_me"),
    path("auth/forget-password", AuthController.forgetPassword, name="forget_password"),
    path("auth/verify-otp", AuthController.verifyOTP, name="verify_otp"),
    path("auth/update-password", AuthController.updatePassword, name="update_password"),
]