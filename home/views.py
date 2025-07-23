from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from board.models import WBSItem

@login_required
def home(request):
    # 1) 로그인 유저의 할당된 WBS 개수
    #my_count = WBSItem.objects.filter(task_owner=request.user.name).count()

    # 2) 전체 WBS 개수 & 상태별 개수
    #total_count = WBSItem.objects.count()
    #progress_counts = (
    #    WBSItem.objects
    #           .values('progress')
    #           .order_by()
    #           .annotate(count=models.Count('progress'))
    #)
    # 편의상 dict 형태로
    #prog_dict = {d['progress']: d['count'] for d in progress_counts}

    # 3) In progress 상태의 최근 10개 항목
    in_progress_items = (
        WBSItem.objects
               .filter(progress='In progress')
               .order_by('-no')[:10]
    )

    return render(request, 'home.html', {
        #'my_count': my_count,
        #'total_count': total_count,
        #'prog_counts': prog_dict,
        'in_progress_items': in_progress_items,
    })
