# home/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count
from board.models import WBSItem

@login_required
def home(request):

    # ——— In Progress 항목 최근 10개 조회 ———
    in_progress_items = (
        WBSItem.objects
               .filter(progress='In progress')
               .order_by('-no')[:10]
    )

    # 전체 WBSItem QuerySet (이하 집계에 공통 사용)
    wbs_qs = WBSItem.objects.all()

    # ——— 전체 항목 수 ———
    wbs_total = wbs_qs.count()

    # ——— 상태별 항목 수 집계 ———
    # DB의 progress 값 → 템플릿용 키 매핑
    key_map = {
        'In progress': 'in_progress',
        'COMPLETE':    'complete',
        'Wait':        'wait',
        'Hold':        'hold',
    }
    # 기본값 0으로 초기화 후 실제 값 채움
    progress_counts = {'in_progress': 0, 'complete': 0, 'wait': 0, 'hold': 0}
    for row in wbs_qs.values('progress').annotate(cnt=Count('id')):
        k = (row['progress'] or '').strip()
        if k in key_map:
            progress_counts[key_map[k]] = row['cnt']

    # ——— Task Owner TOP 5 ———
    # null, 빈 문자열, 'nan' 값 제외 후 항목 수 기준 내림차순 상위 5명
    owner_top5 = (
        wbs_qs.exclude(task_owner__isnull=True)
              .exclude(task_owner__in=['', 'nan', 'NaN'])
              .values('task_owner')
              .annotate(cnt=Count('id'))
              .order_by('-cnt')[:5]
    )

    # ——— 템플릿 컨텍스트 구성 ———
    ctx = {
        'wbs_total':         wbs_total,
        'progress_counts':   progress_counts,
        'owner_top5':        owner_top5,
        'in_progress_items': in_progress_items,
    }
    return render(request, 'home.html', ctx)
