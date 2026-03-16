#tasks/url.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from .models import CustomUser
from .models import EmployeeNumber
from .forms import CustomUserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

def login_page(request):
    # 로그인 페이지 렌더링
    return render(request, 'registration/login.html')


def signup(request):
    print("signup 함수 진입")  # 디버그용 로그
    if request.method == 'POST':
        # POST 데이터로 폼 바인딩
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home.html')  # 가입 후 홈으로 이동
    else:
        # GET 요청: 빈 폼 초기화
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def check_duplicate_user_id(request):
    # 쿼리 파라미터에서 username 추출
    user_id = request.GET.get('username')
    # 동일 username 존재 여부 확인
    exists = CustomUser.objects.filter(username=user_id).exists()
    # 'true' / 'false' 문자열로 반환 (프론트 호환용)
    return JsonResponse({'duplicate': str(exists).lower()})


def custom_login(request):
    if request.method == 'POST':
        # POST 데이터에서 아이디 · 비밀번호 추출
        username = request.POST.get('usr_id')
        password = request.POST.get('password')

        # Django 인증 처리
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # 세션에 사용자 저장
            return JsonResponse({'message': 'Login success'})
        else:
            # 인증 실패 시 401 반환
            return JsonResponse({'message': 'Login failed'}, status=401)


@csrf_exempt  # API 클라이언트 호환을 위해 CSRF 검사 제외
def join(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Registration success'}, content_type='application/json')
        else:
            # 폼 에러를 JSON 문자열로 변환
            errors = form.errors.as_json()

            # 사원번호 관련 에러 우선 처리
            if "employee_number" in errors:
                if "등록되지 않은 사원번호입니다" in errors:
                    return JsonResponse({'message': 'not_allowed'}, content_type='application/json', status=400)
                elif "이미 가입된 사원번호입니다" in errors:
                    return JsonResponse({'message': 'already_registered'}, content_type='application/json', status=400)

            # 그 외 유효성 검사 실패
            return JsonResponse({'message': 'Registration failed', 'errors': errors}, content_type='application/json', status=400)

    # GET 요청: 회원가입 폼 페이지 렌더링
    form = CustomUserCreationForm()
    return render(request, 'registration/join.html', {'form': form})


