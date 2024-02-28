from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('', views.home, name='home'),
    path('room/<str:pk>', views.room_page, name='room'),
    path('profile/<str:pk>', views.profile_page, name='user-profile'),

    path('create-room/', views.creat_room, name='create-room'),
    path('register/', views.register_page, name='register'),
    path('edit-user', views.edit_user, name='edit-user'),
    path('delete-message/<str:pk>', views.delete_message, name='delete-message'),

    path('topics/', views.topics_page, name='topics'),
    path('activity/', views.activity_page, name='activity'),
]

