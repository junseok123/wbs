from django.contrib.auth.models import AbstractUser
from django.db import models

class EmployeeNumber(models.Model):
    number = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.number

class CustomUser(AbstractUser):
    # 기본 필드: username(아이디), password(비번), email 등 AbstractUser에 있음
    employee_number = models.OneToOneField(
        EmployeeNumber,
        on_delete=models.PROTECT,  # 사원번호가 지워지면 회원도 보호
        null=True,
        blank=False,
        unique=True
    )
    name = models.CharField(max_length=50)  # 이름 필드 추가
   
    def __str__(self):
        return f'{self.username} ({self.employee_number})'
