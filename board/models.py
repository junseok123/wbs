import re
from django.db import models

class WBSItem(models.Model):
    no = models.PositiveIntegerField(unique=True)
    task_title = models.CharField(max_length=255)
    task_content = models.TextField(blank=True)
    task_owner = models.CharField(max_length=100)
    device = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    tester = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()
    progress = models.CharField(max_length=50)
    comment = models.TextField(blank=True)
    
    @property
    def short_title(self):
        """
        task_title을 줄바꿈(\n) 기준으로 잘라
        첫 줄만 리턴합니다.
        """
        return self.task_title.split('\n', 1)[0]
    def __str__(self):
        return self.task_title

    @property
    def short_devices(self):
        """
        device 필드에 ','나 '/'로 구분된 기기가 여러 개 있을 때,
        앞의 두 개만 취해서 반환합니다.
        """
        # 문자열이 아닌 경우 빈 문자열 처리
        devices = str(self.device)
        # , 또는 / 또는 + 로 분할
        parts = re.split(r'[\s,\/\+]+', devices)
        # 앞뒤 공백 제거 후 빈 문자열 제외
        clean = [p.strip() for p in parts if p.strip()]
        # 앞의 두 개만
        return ', '.join(clean[:2])