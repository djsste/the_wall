from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create_user', views.create_user),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),
    path('login', views.login),
    path('wall', views.success),
    path('logout', views.logout),
    path('create_message', views.create_message),
    path('create_comment/<int:id>', views.create_comment, name='create_comment'),
    path('delete_messsage/<int:id>', views.delete_message, name='delete_message'),
    
]
