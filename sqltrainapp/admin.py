from django.contrib import admin

# Register your models here.
from .models import User, Question, Doques

class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'user_name', 'user_type', 'school', 'faculties', 'cls')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('ques_id', 'ques_type', 'ques_title', 'ques_content', 'answer', 'level', 'passnum', 'totalnum')

class DoquesAdmin(admin.ModelAdmin):
    list_display = ('run_id', 'someone', 'someques', 'start_time', 'end_time', 'answ_content', 'memory',
                    'language_type', 'result_type')

admin.site.register(User, UserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Doques, DoquesAdmin)