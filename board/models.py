from django.db import models

class WBSItem(models.Model):
    no = models.PositiveIntegerField(unique=True)
    task_title = models.CharField(max_length=255)
    task_owner = models.CharField(max_length=100)
    device = models.CharField(max_length=100)
    start_date = models.DateField()
    due_date = models.DateField()
    tester = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()
    progress = models.CharField(max_length=50)
    comment = models.TextField(blank=True)

    def __str__(self):
        return self.task_title
