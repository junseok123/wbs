import os
from django.conf import settings
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import WBSItem
from .wbs_info import load_wbs_from_csv

def wbs_list_view(request):
    if not WBSItem.objects.exists():
        csv_path = os.path.join(settings.BASE_DIR, 'templates', '_WBS_.csv')  # 혹은 실제 위치
        print(f"DEBUG: CSV 경로 → {csv_path}, exists? {os.path.exists(csv_path)}")
        count = load_wbs_from_csv(csv_path)
        print(f"[INFO] CSV에서 {count}개 항목 로드")

    all_items = WBSItem.objects.all().order_by('-no')
    paginator = Paginator(all_items, 30)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'wbs_input_home.html', {
        'page_obj': page_obj,
        # 템플릿에서 아직 wbs_items로 쓰고 있다면 아래 추가:
        'wbs_items': page_obj,
    })
