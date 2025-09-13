from django.urls import path
from . import views

urlpatterns = [
    path('post', views.CreatePostView.as_view()),
    path('like', views.LikePostView.as_view()),
    path('unlike', views.UnlikePostView.as_view()),
    path('feed', views.FeedView.as_view())
   
]
