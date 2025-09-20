from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.CreatePostView.as_view(), name='post-create'),
    path('like/', views.LikePostView.as_view(), name='post-like'),
    path('unlike/', views.UnlikePostView.as_view(), name='post-unlike'),
    path('feed/', views.FeedView.as_view(), name='feed'),

    # Events endpoints (plural path)
    path('events/', views.EventListAPIView.as_view(), name='events-list'),       # GET list
    path('events/create/', views.EventCreateAPIView.as_view(), name='events-create'),  # POST create
    path('events/<uuid:pk>/', views.EventDetailAPIView.as_view(), name='events-detail'),
    path('events/<uuid:pk>/update/', views.EventUpdateAPIView.as_view(), name='events-update'),
    path('events/<uuid:pk>/delete/', views.EventDeleteAPIView.as_view(), name='events-delete'),
]