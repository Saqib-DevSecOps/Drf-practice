from django.contrib import admin

# Register your models here.
from practice.models import Student, Singer, Song


class StudentL(admin.ModelAdmin):
    list_display = ['id']


admin.site.register(Student, StudentL)
admin.site.register(Song)
admin.site.register(Singer)
