from django.shortcuts import render
from .models import WBSItem

def wbs_list_view(request):
    wbs_items = WBSItem.objects.all().order_by('no')
    return render(request, 'wbs_input_home.html', {'wbs_items': wbs_items})  # ✅ 이름 일치시킴
