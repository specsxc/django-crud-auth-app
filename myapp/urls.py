from django.urls import path
from .views import (
    delete_post_view,
    edit_post_view,
    index_view,
    login_view,
    register_view,
    add_post_view,
)

urlpatterns = [
    path("", index_view, name="index"),
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("add_post/", add_post_view, name="add_post"),
    path("edit_post/<int:post_id>/", edit_post_view, name="edit_post"),
    path("delete_post/<int:post_id>/", delete_post_view, name="delete_post"),
]
