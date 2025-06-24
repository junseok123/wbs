import pandas as pd
from datetime import datetime
from board.models import WBSItem  # 실제 모델명에 따라 수정

def load_wbs_from_excel(filepath):
    df = pd.read_excel(filepath, skiprows=2)
    df.columns = df.columns.str.strip()
    created = 0

    for _, row in df.iterrows():
        if pd.isna(row['TASK TITLE']):
            continue
        WBSItem.objects.create(
            task_title=row['TASK TITLE'],
            task_owner=row.get('TASK OWNER', ''),
            device=row.get('Device', ''),
            start_date=pd.to_datetime(row['START DATE'], errors='coerce'),
            due_date=pd.to_datetime(row['DUE DATE'], errors='coerce'),
            tester=row.get('Tester', ''),
            duration=pd.to_numeric(row.get('DURATION', 0), errors='coerce'),
            progress=row.get('PROGRESS', ''),
            comment=row.get('Comment', ''),
        )
        created += 1

    return created
