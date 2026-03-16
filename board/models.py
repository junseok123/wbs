import re
import holidays
from django.db import models
import pandas as pd
from datetime import timedelta

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
    @property
    def short_testers(self):
        # tester 값을 문자열로 변환 후 공백 기준으로 분리
        parts = str(self.tester).split()
        # 빈 문자열과 'nan' 값 제거 후 앞뒤 공백 정리
        clean = [p.strip() for p in parts if p.strip() and p.lower() != 'nan']
        # 최대 2개 항목만 쉼표로 연결하여 반환
        return ', '.join(clean[:2])


    
    @property
    def duration_calc(self):
        """
        전체 기간(일수) 계산: due_date - start_date
        """
        if self.start_date and self.due_date and self.due_date >= self.start_date:
            return (self.due_date - self.start_date).days
        return 0

    @property
    def business_days(self):
        """
        대한민국 공휴일을 제외한 순영업일(일수)을 계산합니다.
        공휴일 라이브러리 holidays.KR() 사용.
        """
        if not (self.start_date and self.due_date and self.due_date >= self.start_date):
            return 0
        # 연도 범위 내 한국 공휴일
        years = list(range(self.start_date.year, self.due_date.year + 1))
        kr_holidays = holidays.KR(years=years)
        total_days = (self.due_date - self.start_date).days + 1
        business = 0
        for i in range(total_days):
            day = self.start_date + timedelta(days=i)
            # 평일 체크: 0~4 => 월~금
            if day.weekday() < 5 and day not in kr_holidays:
                business += 1
        return business