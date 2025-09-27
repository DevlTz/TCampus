from . import views

urlpatterns = [
    path('professor/evaluate', views.ReviewCreateAPIView.as_view()),
    path('professor/<uuid:pk>/reviews', views.ReviewListUniqueAPIView.as_view()),
]