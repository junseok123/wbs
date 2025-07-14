from django.db import models

class WBSItem(models.Model):
    no = models.PositiveIntegerField(unique=True)
    task_title = models.CharField(max_length=255)
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
