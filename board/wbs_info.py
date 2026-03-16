# board/wbs_info.py
import re
import pandas as pd
from board.models import WBSItem

def load_wbs_from_csv(file_or_buffer):
    df = pd.read_csv(file_or_buffer, skiprows=7, encoding='utf-8-sig')

    # 컬럼명 정리
    df.columns = (df.columns.str.strip()
                            .str.lower()
                            .str.replace(' ', '_')
                            .str.replace(r'\.', '', regex=True))
    # unnamed 제거
    df = df.loc[:, [c for c in df.columns if not c.startswith('unnamed')]]

    # ── 제목/본문 분리 ─────────────────────────────────────────────
    # 원본 컬럼(제목+본문)이 'task_title'에 들어온다고 가정
    raw = df.get('task_title', pd.Series(dtype=str)).astype(str).fillna('').str.strip()

    # 제목: 첫 줄
    df['task_title'] = raw.str.split(r'[\r\n]+', regex=True).str[0].str.strip()

    # 본문: 둘째 줄 이후를 개행으로 합치기
    def split_content(s: str) -> str:
        parts = re.split(r'[\r\n]+', s)
        return '\n'.join(parts[1:]).strip() if len(parts) > 1 else ''

    df['task_content'] = raw.apply(split_content)

    # 제목이 비었거나 'nan' 문자열인 행 제거
    mask = df['task_title'].notna() & (df['task_title'] != '') & (df['task_title'].str.lower() != 'nan')
    df = df[mask]

    created = 0
    for _, row in df.iterrows():
        # 날짜
        s = pd.to_datetime(row.get('start_date'), errors='coerce')
        d = pd.to_datetime(row.get('due_date'),   errors='coerce')
        start_val = s.date() if pd.notna(s) else None
        due_val   = d.date() if pd.notna(d) else None

        # 숫자
        no_val       = int(row.get('no')) if pd.notna(row.get('no')) else None
        duration_val = int(row.get('duration')) if pd.notna(row.get('duration')) else 0

        WBSItem.objects.create(
            no           = no_val,
            task_title   = row.get('task_title', ''),
            task_content = row.get('task_content', ''),  # 여기 저장
            task_owner   = row.get('task_owner', ''),
            device       = row.get('device', ''),
            start_date   = start_val,
            due_date     = due_val,
            tester       = row.get('tester', ''),
            duration     = duration_val,
            progress     = row.get('progress', ''),
            comment      = row.get('comment', ''),
        )
        created += 1

    return created