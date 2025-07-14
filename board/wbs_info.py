# board/wbs_info.py

import pandas as pd
from board.models import WBSItem

def load_wbs_from_csv(filepath):
    # 1행(인덱스1)만 건너뛰고 실제 헤더/데이터 읽기
    df = pd.read_csv(
        filepath,
        skiprows=[1],
        encoding='utf-8-sig'
    )

    # 컬럼명 정리: 소문자 + 언더스코어
    df.columns = (
        df.columns
          .str.strip()
          .str.lower()
          .str.replace(' ', '_')
    )

    created = 0
    for _, row in df.iterrows():
        # 필수값(task_title) 없으면 건너뛰기
        if pd.isna(row['task_title']):
            continue

        # 날짜 파싱
        raw_start = pd.to_datetime(row['start_date'], errors='coerce')
        raw_due   = pd.to_datetime(row['due_date'],   errors='coerce')

        # NaT 는 None 으로, 아니면 date()로
        start_val = raw_start.date() if not pd.isna(raw_start) else None
        due_val   = raw_due.date()   if not pd.isna(raw_due)   else None

        WBSItem.objects.create(
            no         = int(row['no']),
            task_title = row['task_title'],
            task_owner = row['task_owner'],
            device     = row['device'],
            start_date = start_val,
            due_date   = due_val,
            tester     = row['tester'],
            duration   = int(row['duration']) if not pd.isna(row['duration']) else 0,
            progress   = row['progress'],
            comment    = row['comment'] or '',
        )
        created += 1

    return created
