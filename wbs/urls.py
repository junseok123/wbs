#wbs/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),  # tasks.urls에서 로그인, 홈 모두 처리
    path('home/', include('home.urls')),
    path('board/', include('board.urls')),
]
