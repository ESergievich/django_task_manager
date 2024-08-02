from django.urls import path
from .views import RegisterUser, ListUsers, UpdateUser, DeleteUser

urlpatterns = [
    path('', ListUsers.as_view(), name='users'),
    path('create/', RegisterUser.as_view(), name='register'),
    path('<int:pk>/update/', UpdateUser.as_view(), name='user_update'),
    path('<int:pk>/delete/', DeleteUser.as_view(), name='user_delete'),
]
