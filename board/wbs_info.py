# board/wbs_info.py

import pandas as pd
from board.models import WBSItem

def load_wbs_from_csv(file_or_buffer):
    """
    - 0~6행(메타 정보) 건너뛰고 7행을 헤더로 사용
    - 빈 ‘302’ 레코드(헤더 다음 행에서 TASK TITLE이 NaN)를 삭제
    - 컬럼명 통일, task_title 첫 줄만 남기기
    """
    # 1) 메타 정보 7행(skiprows=7) 건너뛰고 읽기
    df = pd.read_csv(
        file_or_buffer,
        skiprows=7,
        encoding='utf-8-sig'
    )

    # 2) 헤더 다음(302번) 레코드에서 TASK TITLE이 NaN인 행을 아예 제거
    if 'TASK TITLE' in df.columns:
        df = df[df['TASK TITLE'].notna()]

    # 3) 컬럼명 정리
    df.columns = (
        df.columns
          .str.strip()
          .str.lower()
          .str.replace(' ', '_')
          .str.replace(r'\.', '', regex=True)
    )

    # 4) Unnamed 컬럼(빈 첫 번째 컬럼) 삭제
    df = df.loc[:, [c for c in df.columns if not c.startswith('unnamed')]]

    # 5) 문자열 컬럼 앞뒤 공백 제거
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].astype(str).str.strip()

    # 6) task_title은 셀 내 줄바꿈 기준 첫 줄만 추출
    if 'task_title' in df.columns:
        df['task_title'] = (
            df['task_title']
              .str.split(r'[\r\n]+', regex=True)
              .str[0]
              .str.strip()
        )

    created = 0
    for _, row in df.iterrows():
        title = row.get('task_title')
        if not title:
            continue

        # 날짜 파싱 (NaT → None)
        raw_s = pd.to_datetime(row.get('start_date'), errors='coerce')
        raw_d = pd.to_datetime(row.get('due_date')  , errors='coerce')
        start_val = raw_s.date() if not pd.isna(raw_s) else None
        due_val   = raw_d.date() if not pd.isna(raw_d) else None

        # 숫자 파싱
        no_val       = int(row.get('no'))      if not pd.isna(row.get('no'))      else None
        duration_val = int(row.get('duration')) if not pd.isna(row.get('duration')) else 0

        WBSItem.objects.create(
            no         = no_val,
            task_title = title,
            task_owner = row.get('task_owner', ''),
            device     = row.get('device', ''),
            start_date = start_val,
            due_date   = due_val,
            tester     = row.get('tester', ''),
            duration   = duration_val,
            progress   = row.get('progress', ''),
            comment    = row.get('comment', ''),
        )
        created += 1

    return created
