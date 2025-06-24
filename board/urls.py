# board/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.wbs_list_view, name='wbs-board'), 
]