import csv
import os
from django.core.management.base import BaseCommand
from board.models import WBSItem
from django.conf import settings
from datetime import datetime

class Command(BaseCommand):
    help = 'Import WBS items from a CSV file'

    def handle(self, *args, **kwargs):
        # CSV 파일 경로 설정 (templates 디렉토리에 있는 경우)
        csv_path = os.path.join(settings.BASE_DIR, 'templates', '_WBS_.csv')

        with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # 필수 필드가 비어있으면 skip
                task_title = row.get('TASK TITLE')
                if not task_title:
                    continue

                try:
                    WBSItem.objects.create(
                        no=int(row.get('NO', 0)),
                        task_title=task_title,
                        task_owner=row.get('TASK OWNER', ''),
                        device=row.get('Device', ''),
                        start_date=datetime.strptime(row.get('START DATE', ''), '%Y-%m-%d').date() if row.get('START DATE') else None,
                        due_date=datetime.strptime(row.get('DUE DATE', ''), '%Y-%m-%d').date() if row.get('DUE DATE') else None,
                        tester=row.get('Tester', ''),
                        duration=int(row.get('DURATION', 0)),
                        progress=row.get('PROGRESS', ''),
                        comment=row.get('Comment', '')
                    )
                except Exception as e:
                    self.stderr.write(f"❌ Error inserting row {row}: {e}")
                    continue

        self.stdout.write(self.style.SUCCESS('✅ WBS data imported successfully!'))
