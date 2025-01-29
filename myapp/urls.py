from django.urls import path
from .views import index_view, home_view, login_view, logout_view, register_view

urlpatterns = [
    path("", index_view, name="index"),
    path("home/", home_view, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
]
