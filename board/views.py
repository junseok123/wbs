import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import WBSItem
from django.contrib import messages
from .wbs_info import load_wbs_from_csv
from .forms import WBSItemForm
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Max 

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

def wbs_edit(request, no):
    item = get_object_or_404(WBSItem, no=no)
    if request.method == 'POST':
        form = WBSItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('wbs-board')
    else:
        form = WBSItemForm(instance=item)
    return render(request, 'wbs_edit.html', {
        'form': form,
        'item_no': no,
    })

@require_POST
def wbs_create_api(request):
    form = WBSItemForm(request.POST)
    if form.is_valid():
        # commit=False 로 인스턴스만 만들고
        item = form.save(commit=False)
        # 현재 최고 no 값을 가져와 +1
        max_no = WBSItem.objects.aggregate(Max('no'))['no__max'] or 0
        item.no       = max_no + 1

        # 3) duration (영업일) 계산
        item.duration = item.business_days

        # 4) 최종 저장
        item.save()
        return JsonResponse({'status':'success'})
    
    # 유효성 검사 실패 시
    return JsonResponse({'status':'error','errors':form.errors}, status=400)