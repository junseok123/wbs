## WBS 프로젝트 관리 시스템

Django 기반의 사내 WBS(Work Breakdown Structure) 항목 관리 웹 애플리케이션입니다.  
사원번호 인증 기반 회원가입, CSV 업로드, 항목 CRUD, 한국 공휴일 반영 영업일 계산 기능을 제공합니다.

---

## 📁 프로젝트 구조

```
wbs_project/
├── wbs/                    # Django 프로젝트 설정 (settings, urls, wsgi)
├── tasks/                  # 회원가입 / 로그인 / 인증 앱
├── board/                  # WBS 항목 관리 앱 (CRUD, CSV 업로드)
├── home/                   # 홈 대시보드 앱
├── templates/              # HTML 템플릿
│   ├── home.html
│   ├── wbs_input_home.html
│   └── registration/
│       ├── login.html
│       └── join.html
├── static/                 # 정적 파일 (CSS, JS, 이미지)
├── manage.py
└── requirements.txt
```

---

## ⚙️ 주요 기능

### 인증 (tasks 앱)
- 사원번호(`EmployeeNumber`) 기반 회원가입 — 등록되지 않은 사원번호 거부
- 아이디 중복 검사 (Ajax)
- 아이디·비밀번호·이름·사원번호 클라이언트 유효성 검사
- 커스텀 유저 모델 (`CustomUser`) 사용

### WBS 항목 관리 (board 앱)
- CSV 파일 업로드로 항목 일괄 등록
- 항목 목록 조회 (제목 검색 / 진행 상태 필터 / 담당자 필터 / 페이지네이션 30개)
- 항목 상세보기 · 수정 · 삭제 (Bootstrap 모달)
- 새 항목 추가 (Ajax POST)
- **한국 공휴일 제외 영업일 자동 계산** (`holidays.KR` 라이브러리 사용)

### 홈 대시보드 (home 앱)
- Task Owner TOP 5 랭킹
- 진행 상태별 항목 수 현황 (In Progress / COMPLETE / Wait / Hold)
- 최근 In Progress 항목 10개 목록

---

## 🚀 설치 및 실행

### 1. 저장소 클론

```bash
git clone <저장소 URL>
cd wbs_project
```

### 2. 가상환경 생성 및 패키지 설치

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 데이터베이스 마이그레이션

```bash
python manage.py migrate
```

### 4. 관리자 계정 생성 (선택)

```bash
python manage.py createsuperuser
```

### 5. 개발 서버 실행

```bash
python manage.py runserver
```

브라우저에서 `http://127.0.0.1:8000/` 접속 → 로그인 페이지로 이동합니다.

---

## 📦 의존성 (requirements.txt)

| 패키지 | 버전 | 용도 |
|---|---|---|
| Django | 5.2.4 | 웹 프레임워크 |
| holidays | 0.76 | 한국 공휴일 계산 |
| pandas | 2.3.1 | CSV 데이터 처리 |
| numpy | 2.3.1 | pandas 의존성 |
| sqlparse | 0.5.3 | Django SQL 쿼리 파싱 |
| asgiref | 3.9.1 | Django 비동기 지원 |

---

## 🗄️ 주요 모델

### `WBSItem` (board 앱)

| 필드 | 타입 | 설명 |
|---|---|---|
| `no` | PositiveIntegerField | 항목 고유 번호 (unique) |
| `task_title` | CharField | 작업 제목 |
| `task_content` | TextField | 작업 내용 |
| `task_owner` | CharField | 담당자 |
| `device` | CharField | 대상 기기 |
| `start_date` | DateField | 시작일 |
| `due_date` | DateField | 마감일 |
| `tester` | CharField | 테스터 |
| `duration` | PositiveIntegerField | 기간 (영업일) |
| `progress` | CharField | 진행 상태 |
| `comment` | TextField | 코멘트 |

**주요 프로퍼티**

- `short_title` — 제목 첫 줄만 반환
- `short_devices` — 기기 목록 앞 2개만 반환
- `short_testers` — 테스터 목록 앞 2개만 반환
- `business_days` — 한국 공휴일 제외 영업일 계산
- `duration_calc` — 전체 기간(일수) 계산

### `CustomUser` (tasks 앱)

Django 기본 `AbstractUser` 확장 모델로, `name`과 `employee_number` 필드가 추가되어 있습니다.

---

## 🌐 URL 구조

| URL | 앱 | 설명 |
|---|---|---|
| `/` | tasks | 로그인 페이지 |
| `/join/` | tasks | 회원가입 |
| `/join/do_duplicate_check/` | tasks | 아이디 중복 검사 API |
| `/login/` | tasks | 로그인 API |
| `/home/` | home | 홈 대시보드 |
| `/board/` | board | WBS 목록 |
| `/board/edit/<no>/` | board | WBS 항목 수정 |
| `/board/api/create/` | board | WBS 항목 생성 API |
| `/board/api/delete/<no>/` | board | WBS 항목 삭제 API |
| `/admin/` | Django | 관리자 페이지 |

---

## 📥 CSV 업로드 형식

`/board/` 페이지에서 CSV 파일을 업로드하여 WBS 항목을 일괄 등록할 수 있습니다.  
업로드 시 기존 데이터는 전체 삭제 후 새로 적재됩니다.

**CSV 헤더 (필수)**

```
NO, TASK TITLE, TASK OWNER, Device, START DATE, DUE DATE, Tester, DURATION, PROGRESS, Comment
```

- 날짜 형식: `YYYY-MM-DD`
- `TASK TITLE`이 비어 있는 행은 건너뜁니다.

또는 아래 커맨드로 직접 임포트할 수 있습니다:

```bash
python manage.py import_wbs
# templates/_WBS_.csv 파일을 읽어서 DB에 적재합니다.
```

---

## 📝 진행 상태 값

| 값 | 표시 색상 |
|---|---|
| `In progress` | 빨간색 |
| `COMPLETE` | 파란색 |
| `Wait` | 노란색 |
| `Hold` | 검정색 |

---

## ⚠️ 주의 사항

- `SECRET_KEY`는 반드시 환경 변수로 분리하여 관리하세요.
- CSV 업로드 시 기존 데이터가 전체 삭제되므로 주의하세요.
