from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create_user', views.create_user),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),
    path('login', views.login),
    path('wall', views.success),
    path('logout', views.logout),
]
