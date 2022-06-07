from django.contrib import admin

# Register your models here.
from practice.models import Student
class StudentL(admin.ModelAdmin):
    list_display = ['id']

admin.site.register(Student,StudentL)