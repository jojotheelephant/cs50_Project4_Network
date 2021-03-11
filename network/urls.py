
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),    
    path("posts/like/<int:id>",views.like, name="like"),
    path("posts/edit/<int:id>", views.editbody, name="editbody"),
    path("posts/<str:username>", views.posts, name="posts"),
    path("posts/<str:username>/<int:page>", views.posts, name="posts"),
    path("profile/<str:username>", views.profile, name="profile"),
    path('currentuser', views.getCurrentUser, name="currentUser"),
    path("follow/<str:username>", views.follow, name="follow"),
]
