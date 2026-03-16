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
    # ——— CSV 파일 업로드 처리 (POST 요청) ———
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')

        # 파일 미선택 시 에러 메시지
        if not csv_file:
            messages.error(request, 'CSV 파일을 선택해주세요.')
        # CSV 확장자 검증
        elif not csv_file.name.lower().endswith('.csv'):
            messages.error(request, 'CSV 파일만 업로드 가능합니다.')
        else:
            # 기존 데이터 전체 삭제 후 새로 적재 (append 방식으로 변경 가능)
            WBSItem.objects.all().delete()
            count = load_wbs_from_csv(csv_file)
            print(f"[DEBUG] load_wbs_from_csv 반환값: {count}")
            print(f"[DEBUG] 실제 DB 건수: {WBSItem.objects.count()}")
            messages.success(request, f'{count}개 항목을 업로드했습니다.')

        # POST 처리 후 목록 페이지로 리다이렉트 (PRG 패턴)
        return redirect('wbs-board')

    # ——— 검색 & 필터 파라미터 파싱 (GET) ———
    q        = request.GET.get('q', '').strip()        # 제목 검색어
    progress = request.GET.get('progress', '').strip() # 진행 상태 필터
    owner    = request.GET.get('owner', '').strip()    # 담당자 필터

    # ——— 필터 조건에 따라 QuerySet 구성 ———
    qs = WBSItem.objects.all()
    if q:
        qs = qs.filter(task_title__icontains=q)   # 제목 부분 일치 검색
    if progress:
        qs = qs.filter(progress=progress)          # 진행 상태 일치
    if owner:
        qs = qs.filter(task_owner=owner)           # 담당자 일치

    # ——— 페이지네이션 (30개씩) ———
    all_items   = qs.order_by('-no')               # no 역순 정렬
    paginator   = Paginator(all_items, 30)
    page_number = request.GET.get('page', 1)
    page_obj    = paginator.get_page(page_number)

    # 담당자 셀렉트박스용 중복 제거 목록
    distinct_owners = (
        WBSItem.objects
               .values_list('task_owner', flat=True)
               .distinct()
               .order_by('task_owner')
    )

    return render(request, 'wbs_input_home.html', {
        'page_obj':       page_obj,
        'request':        request,
        'distinct_owners': distinct_owners,
    })


def wbs_edit(request, no):
    # no에 해당하는 WBSItem 조회, 없으면 404
    item = get_object_or_404(WBSItem, no=no)

    if request.method == 'POST':
        # 기존 인스턴스에 POST 데이터를 바인딩하여 수정
        form = WBSItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('wbs-board')  # 저장 후 목록으로 이동
    else:
        # GET 요청: 기존 데이터로 폼 초기화
        form = WBSItemForm(instance=item)

    return render(request, 'wbs_input_home.html', {
        'form':    form,
        'item_no': no,
    })


@require_POST
def wbs_create_api(request):
    form = WBSItemForm(request.POST)
    if form.is_valid():
        # DB 저장 전 인스턴스만 생성
        item = form.save(commit=False)

        # 현재 최댓값 no + 1로 고유 번호 부여
        max_no   = WBSItem.objects.aggregate(Max('no'))['no__max'] or 0
        item.no  = max_no + 1

        # 영업일 기준 duration 계산 후 저장
        item.duration = item.business_days
        
        item.save()
        return JsonResponse({'status': 'success'})

    # 유효성 검사 실패 시 에러 내용 반환
    return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)


@require_POST
def wbs_delete_api(request, no: int):
    # no에 해당하는 WBSItem 조회, 없으면 404
    item = get_object_or_404(WBSItem, no=no)
    try:
        item.delete()
        return JsonResponse({"status": "success"})
    except Exception as e:
        # 삭제 실패 시 에러 메시지 반환
        return JsonResponse({"status": "error", "message": str(e)}, status=400)