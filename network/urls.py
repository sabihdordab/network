
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following , name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_post, name="create"),
    path("<str:username>" , views.user_profile , name="profile"),
    path("follow/<str:username>" , views.follow_unfollow , name="follow"),
    path("edit/<int:id>",views.edit_post , name = "edit"),
    path("like/<int:id>",views.like_post , name = "like")
]
