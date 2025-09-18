from django.urls import path
from . import views

urlpatterns = [
    path('post', views.CreatePostView.as_view()),
    path('toggle-like', views.toggle_post_like()),
    path('feed', views.FeedView.as_view())
   
]
