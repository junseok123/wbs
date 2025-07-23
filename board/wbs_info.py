import pandas as pd
from board.models import WBSItem

def load_wbs_from_csv(file_or_buffer):
    """
    - 상위 7행(0~6) 메타 정보 건너뛰고, 7행을 헤더로 사용
    - 'Unnamed' 컬럼 제거, 컬럼명 통일
    - task_title은 줄바꿈 기준 첫 줄만 남기고 전처리
    - task_title이 NaN 또는 빈 문자열인 행은 삭제
    """
    # 1) 메타 정보 7행 건너뛰고 읽기
    df = pd.read_csv(
        file_or_buffer,
        skiprows=7,
        encoding='utf-8-sig'
    )

    # 2) 컬럼명 정리
    df.columns = (
        df.columns
          .str.strip()
          .str.lower()
          .str.replace(' ', '_')
          .str.replace(r'\.', '', regex=True)
    )
    # 3) Unnamed 컬럼(빈 첫 번째 컬럼) 삭제
    df = df.loc[:, [c for c in df.columns if not c.startswith('unnamed')]]

    # 4) 문자열 컬럼 전처리: 앞뒤 공백 + 개행 제거
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].astype(str).str.strip()
    # task_title은 줄바꿈(\n,\r) 기준 첫 줄만
    if 'task_title' in df.columns:
        df['task_title'] = (
            df['task_title']
            .str.split(r'[\r\n]+', regex=True)
            .str[0]
            .str.strip()
        )
        # 빈 문자열, pandas NaN, 그리고 'nan' 문자열 전부 제거
        df = df[
            df['task_title'].notna() &                   # pandas NaN 필터
            (df['task_title'] != '') &                   # 빈 문자열 필터
            (df['task_title'].str.lower() != 'nan')      # "nan" 문자열 필터
        ]
    created = 0
    for _, row in df.iterrows():
        # task_title은 이미 비어있지 않음
        title = row['task_title']

        # 날짜 변환 (NaT → None)
        raw_s = pd.to_datetime(row.get('start_date'), errors='coerce')
        raw_d = pd.to_datetime(row.get('due_date')  , errors='coerce')
        start_val = raw_s.date() if not pd.isna(raw_s) else None
        due_val   = raw_d.date() if not pd.isna(raw_d) else None

        # 숫자 변환
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
