import pandas as pd
import re
from board.models import WBSItem

def load_wbs_from_csv(file_or_buffer):
    """
    - 첫 번째 행(인덱스 0)을 헤더로 사용하고, 두 번째 행(인덱스 1)을 건너뛰어 CSV를 읽습니다.
    - 'task_title' 컬럼의 원본 멀티라인 데이터를 분리하여,
      첫 줄은 task_title, 나머지는 task_content로 저장합니다.
    - 컬럼명 통일, Unnamed 열 제거, 문자열 전처리 수행
    - task_title이 NaN 혹은 빈 문자열인 행은 모두 제거
    """
    # 1) CSV 읽기: 헤더는 0행, 1행만 건너뛰기
    df = pd.read_csv(
        file_or_buffer,
        skiprows=[1],
        encoding='utf-8-sig'
    )

    # 2) 컬럼명 정리: 소문자, 언더스코어, 온점 제거
    df.columns = (
        df.columns
          .str.strip()
          .str.lower()
          .str.replace(' ', '_', regex=False)
          .str.replace(r'\.', '', regex=True)
    )

    # 3) Unnamed 열 제거
    df = df.loc[:, [c for c in df.columns if not c.startswith('unnamed')]]

    # 4) 문자열 컬럼 전처리: 앞뒤 공백 제거
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].astype(str).str.strip()

    # 5) 원본 멀티라인 task_title을 변수로
    if 'task_title' not in df.columns:
        # 컬럼이 없으면 바로 리턴
        return 0
    raw = df['task_title'].astype(str)

    # 6) 원본 raw에 NaN 또는 빈 문자열인 행 제거
    df = df[raw.str.strip() != '']
    raw = raw[df.index]

    # 7) 멀티라인 분리: 첫 줄 제목, 나머지 내용
    titles = raw.str.split(r'[\r\n]+', regex=True).str
    df['task_title'] = titles[0].str.strip()
    df['task_content'] = raw.str.split(r'[\r\n]+', regex=True).apply(lambda parts: '\n'.join(parts[1:]).strip())

    # 8) 최종 빈 제목 제거
    df = df[df['task_title'].astype(bool)]

    # 9) DB 인서트
    created = 0
    for _, row in df.iterrows():
        no_val       = int(row.get('no'))      if pd.notna(row.get('no'))       else None
        duration_val = int(row.get('duration')) if pd.notna(row.get('duration')) else 0
        raw_s = pd.to_datetime(row.get('start_date'), errors='coerce')
        raw_d = pd.to_datetime(row.get('due_date'),   errors='coerce')

        WBSItem.objects.create(
            no           = no_val,
            task_title   = row['task_title'],
            task_content = row.get('task_content', ''),
            task_owner   = row.get('task_owner', ''),
            device       = row.get('device', ''),
            start_date   = raw_s.date() if pd.notna(raw_s) else None,
            due_date     = raw_d.date() if pd.notna(raw_d) else None,
            tester       = row.get('tester', ''),
            duration     = duration_val,
            progress     = row.get('progress', ''),
            comment      = row.get('comment', ''),
        )
        created += 1

    return created
