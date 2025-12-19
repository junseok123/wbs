# board/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.wbs_list_view, name='wbs-board'), 

    # 편집 뷰
    path('edit/<int:no>/', views.wbs_edit, name='wbs_edit'),

    path('api/create/', views.wbs_create_api, name='wbs_create_api'),
    path('api/delete/<int:no>/', views.wbs_delete_api, name='wbs_delete_api'),
    
]