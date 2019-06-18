from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path(r'register/', views.register, name='register'),
    path(r'user_info/', views.user_info, name='user_info'),
    path(r'user_info_edit/', views.myself_edit, name='user_info_edit'),
    path(r'upload_image/', views.my_image, name='upload_image'),
    path(r'others_info/<int:id>/', views.others_info, name='others_info'),
    path(r'follow_on/<int:id>/', views.follow_on, name='follow_on'),
    path(r'follow_cancel/<int:id>/', views.follow_cancel, name='follow_cancel'),
    path(r'user_follow/', views.user_follow, name='user_follow'),
    path(r'user_fan/', views.user_fan, name='user_fan'),
    path(r'my_collect/', views.my_collect, name='my_collect'),
]
