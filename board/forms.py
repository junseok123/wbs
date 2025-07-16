from django import forms
from .models import WBSItem

class WBSItemForm(forms.ModelForm):
    class Meta:
        model = WBSItem
        fields = ['task_title','task_content','task_owner','device',
                  'start_date','due_date','tester','progress','comment']