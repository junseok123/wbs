from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, EmployeeNumber

class CustomUserCreationForm(UserCreationForm):
    employee_number = forms.CharField(max_length=20)  # 사원번호 입력 필드
    name = forms.CharField(max_length=50)             # 이름 입력 필드

    class Meta:
        model = CustomUser
        # 폼에 표시할 필드 목록
        fields = ('username', 'password1', 'password2', 'name', 'employee_number')

    def clean_employee_number(self):
        number = self.cleaned_data['employee_number']

        # DB에서 사원번호 존재 여부 확인
        try:
            emp = EmployeeNumber.objects.get(number=number)
        except EmployeeNumber.DoesNotExist:
            raise forms.ValidationError("등록되지 않은 사원번호입니다.")

        # 이미 가입된 사원번호인지 확인
        if CustomUser.objects.filter(employee_number=emp).exists():
            raise forms.ValidationError("이미 가입된 사원번호입니다.")

        # 검증 통과 시 EmployeeNumber 인스턴스 반환
        return emp

    def save(self, commit=True):
        # 부모 클래스로 user 인스턴스 생성 (아직 DB 저장 안 함)
        user = super().save(commit=False)

        # 검증된 사원번호·이름을 user에 할당
        user.employee_number = self.cleaned_data['employee_number']
        user.name = self.cleaned_data['name']

        if commit:
            user.save()  # commit=True일 때만 DB에 저장
        return user