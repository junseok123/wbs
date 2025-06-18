#tasks/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('join/', views.join, name='join'),
    path('join/do_duplicate_check/', views.check_duplicate_user_id, name='check_duplicate_user_id'),
    path('login/', views.custom_login, name='custom_login'),
    path('', views.login_page, name='login_page'),  # ✅ Ajax용 로그인
]