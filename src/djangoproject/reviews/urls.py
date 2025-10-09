from . import views
from django.urls import path

urlpatterns = [
    path("professor/<uuid:pk>/evaluate/", views.ReviewCreateAPIView.as_view(), name="review-create"),
    path("professor/<uuid:pk>/reviews/", views.ReviewListUniqueAPIView.as_view(), name="review-list"),
    path("reviews/<uuid:pk>/update/", views.ReviewUpdateAPIView.as_view(), name="review-update"),
    path("reviews/<uuid:pk>/delete/", views.ReviewDeleteAPIView.as_view(), name="review-delete"),
]
