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
    return render(request, 'registration/login.html')

def signup(request):
    print("signup 함수 진입")  # 1
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home.html')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def check_duplicate_user_id(request):
    user_id = request.GET.get('username')
    exists = CustomUser.objects.filter(username=user_id).exists()
    return JsonResponse({'duplicate': str(exists).lower()})

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('usr_id')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login success'})
        else:
            return JsonResponse({'message': 'Login failed'}, status=401)
        
@csrf_exempt
def join(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Registration success'}, content_type='application/json')
        else:
            errors = form.errors.as_json()
            if "employee_number" in errors:
                if "등록되지 않은 사원번호입니다" in errors:
                    return JsonResponse({'message': 'not_allowed'}, content_type='application/json', status=400)
                elif "이미 가입된 사원번호입니다" in errors:
                    return JsonResponse({'message': 'already_registered'}, content_type='application/json', status=400)
            return JsonResponse({'message': 'Registration failed', 'errors': errors}, content_type='application/json', status=400)

    # 👇 GET 요청이 오면 단순히 HTML 페이지를 렌더링하면 됩니다.
    form = CustomUserCreationForm()
    return render(request, 'registration/join.html', {'form': form})


