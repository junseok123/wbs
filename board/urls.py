# board/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # WBS 보드 메인 페이지
    path('', views.wbs_list_view, name='wbs-board'), 

    # 편집 뷰
    path('edit/<int:no>/', views.wbs_edit, name='wbs_edit'),
    
    # WBS 항목 생성 API
    path('api/create/', views.wbs_create_api, name='wbs_create_api'),
    # WBS 항목 삭제 API (no: 삭제할 항목 고유 번호)
    path('api/delete/<int:no>/', views.wbs_delete_api, name='wbs_delete_api'),
    
]