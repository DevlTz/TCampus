from django.urls import path
from . import views

urlpatterns = [
    path('login', views.MyTokenObtainPairView.as_view()),
    path('user/create', views.CreateUserView.as_view()),
    path('user/ops', views.UsersOperationsView.as_view()),
    path('search', views.ListAllUsersView.as_view()),
    path('follow-toggle', views.ToggleFollowUserView.as_view()),
]
