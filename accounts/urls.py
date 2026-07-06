from django.urls import path
from accounts.controllers import auth_controller as c

urlpatterns = [
    # Pages
    path("", c.login_page, name="login_page"),
    path("register/", c.register_page, name="register_page"),
    path("dashboard/", c.dashboard_page, name="dashboard_page"),

    # API
    path("api/auth/register/", c.register, name="api_register"),
    path("api/auth/login/", c.login, name="api_login"),
    path("api/auth/me/", c.me, name="api_me"),
]