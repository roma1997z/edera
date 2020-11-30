from django.contrib import admin
from .models import MyOption, TeachersTZ, University, Contact, TextTZ, Quiz, QuizResult, PersonReport
# Register your models here.

class MyOptionAdmin(admin.ModelAdmin):

    list_display = ('key','text', 'period','active', 'date')
    list_filter = ['key']
    search_fields = ['key', 'text']


class TeachersTZAdmin(admin.ModelAdmin):
    list_display = ('name','photo', 'description', 'orderindex', 'lang')
    list_filter = ['lang']
    search_fields = ['name', 'description']
    save_as = True


class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name','photo','orderindex')


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'from_email','subject', 'message','date')


class TextTZAdmin(admin.ModelAdmin):
    list_display = ('text_name','text','lang', 'active')
    list_filter = ['lang', 'active']
    search_fields = ['text_name', 'text']
    save_as = True


class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'data', 'date')
    search_fields = ['name']


class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('quiz_id', 'email', 'result')
    search_fields =['email']


class PersonReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc', 'video_link')
    search_fields =['name']
    list_filter = ['active']

admin.site.register(MyOption, MyOptionAdmin)
admin.site.register(TeachersTZ, TeachersTZAdmin)
admin.site.register(University, UniversityAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(TextTZ, TextTZAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuizResult, QuizResultAdmin)
admin.site.register(PersonReport, PersonReportAdmin)