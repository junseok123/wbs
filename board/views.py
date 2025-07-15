import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import WBSItem
from django.contrib import messages
from .wbs_info import load_wbs_from_csv

def wbs_list_view(request):
    # --- 파일 업로드 처리 ---
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if not csv_file:
            messages.error(request, 'CSV 파일을 선택해주세요.')
        elif not csv_file.name.lower().endswith('.csv'):
            messages.error(request, 'CSV 파일만 업로드 가능합니다.')
        else:
            # 기존 데이터 클리어 (원한다면 append 로직으로 바꿀 수 있습니다)
            WBSItem.objects.all().delete()
            count = load_wbs_from_csv(csv_file)
            print(f"[DEBUG] load_wbs_from_csv 반환값: {count}")
            print(f"[DEBUG] 실제 DB 건수: {WBSItem.objects.count()}")
            messages.success(request, f'{count}개 항목을 업로드했습니다.')
        return redirect('wbs-board')

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
        'wbs_items': page_obj,     # 기존 루프 변수 유지
    })
