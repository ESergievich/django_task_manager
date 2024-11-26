from django.urls import path
from .views import UsersListView, UserRegisterView, UserUpdateView, UserDeleteView, UserLoginView, CustomLogoutView

urlpatterns = [
    path('', UsersListView.as_view(), name='users'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('create/', UserRegisterView.as_view(), name='register'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
]
