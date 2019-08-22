from django.contrib import admin

from .models import Subject, Teacher, User
from .forms import UserForm


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('no', 'name', 'create_date', 'is_hot')
    ordering = ('no',)


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('no', 'name', 'detail', 'good_count', 'bad_count', 'subject')
    ordering = ('subject', 'no')


class UserAdmin(admin.ModelAdmin):
    list_display = ('no', 'username', 'password')
    ordering = ('no',)
    form = UserForm
    list_per_page = 10


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(User, UserAdmin)
