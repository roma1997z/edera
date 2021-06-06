from django.contrib import admin
from .models import Profile, TeacherKey, TeacherDesc, TeacherTime, InterestKey, Interest, InterestUser
from .models import MatchUser, Lesson, UserTeacher


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'role', 'active')


class LessonAdmin(admin.ModelAdmin):
    list_display = ('conn', 'name', 'date', 'duration', 'notification')


class UserTeacherAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'teacher', 'active')
    list_filter = ('teacher', )


class MatchUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'teacher', 'like', 'date')
    list_filter = ('teacher','like')
    search_fields = ('user_id',)


class TeacherDescAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'key', 'text')
    list_filter = ('teacher','key')
    search_fields = ('teacher','text',)


class InterestAdmin(admin.ModelAdmin):
    list_display = ('key', 'name', 'important', 'active')
    list_filter = ('active','key')
    search_fields = ('name', )


class InterestUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'interest', 'date')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(TeacherKey)
admin.site.register(TeacherDesc, TeacherDescAdmin)
admin.site.register(TeacherTime)
admin.site.register(InterestKey)
admin.site.register(Interest, InterestAdmin)
admin.site.register(InterestUser, InterestUserAdmin)
admin.site.register(MatchUser, MatchUserAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(UserTeacher, UserTeacherAdmin)
