# home/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count
from board.models import WBSItem

@login_required
def home(request):
    # In progress 최근 10개
    in_progress_items = (
        WBSItem.objects
               .filter(progress='In progress')
               .order_by('-no')[:10]
    )

    wbs_qs = WBSItem.objects.all()

    # 전체 개수
    wbs_total = wbs_qs.count()

    # 상태별 개수 (기본값 0으로 세팅 후 채움)
    key_map = {
        'In progress': 'in_progress',
        'COMPLETE': 'complete',
        'Wait': 'wait',
        'Hold': 'hold',
    }
    progress_counts = {'in_progress': 0, 'complete': 0, 'wait': 0, 'hold': 0}
    for row in wbs_qs.values('progress').annotate(cnt=Count('id')):
        k = (row['progress'] or '').strip()
        if k in key_map:
            progress_counts[key_map[k]] = row['cnt']

    # Task Owner TOP 5 (빈값/’nan’ 제외)
    owner_top5 = (
        wbs_qs.exclude(task_owner__isnull=True)
              .exclude(task_owner__in=['', 'nan', 'NaN'])
              .values('task_owner')
              .annotate(cnt=Count('id'))
              .order_by('-cnt')[:5]
    )

    ctx = {
        'wbs_total': wbs_total,
        'progress_counts': progress_counts,
        'owner_top5': owner_top5,
        'in_progress_items': in_progress_items,
    }
    return render(request, 'home.html', ctx)
