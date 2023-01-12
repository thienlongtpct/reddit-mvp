from django.urls import path

from backend import views


urlpatterns = [
    path('', views.TestView.as_view()),
    path('posts', views.PostsView.as_view()),
    path('posts/<int:post_id>', views.PostView.as_view()),
    path('posts/<int:post_id>/comments', views.CommentsView.as_view()),
]