from django.contrib import admin
from .models import EmployeeNumber
from .models import CustomUser

admin.site.register(EmployeeNumber)
admin.site.register(CustomUser)