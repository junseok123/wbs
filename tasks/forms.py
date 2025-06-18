from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, EmployeeNumber

class CustomUserCreationForm(UserCreationForm):
    employee_number = forms.CharField(max_length=20)
    name = forms.CharField(max_length=50)  # 이름 필드 추가

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'name', 'employee_number')  # name 필드 추가

    def clean_employee_number(self):
        number = self.cleaned_data['employee_number']
        try:
            emp = EmployeeNumber.objects.get(number=number)
        except EmployeeNumber.DoesNotExist:
            raise forms.ValidationError("등록되지 않은 사원번호입니다.")

        if CustomUser.objects.filter(employee_number=emp).exists():
            raise forms.ValidationError("이미 가입된 사원번호입니다.")

        return emp

    def save(self, commit=True):
        user = super().save(commit=False)
        user.employee_number = self.cleaned_data['employee_number']
        user.name = self.cleaned_data['name']   # 이름 저장
        if commit:
            user.save()
        return user
