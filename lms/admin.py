from django.contrib import admin
from .models import Profile, TeacherKey, TeacherDesc, TeacherTime, InterestKey, Interest, InterestUser
from .models import MatchUser


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'role', 'active')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(TeacherKey)
admin.site.register(TeacherDesc)
admin.site.register(TeacherTime)
admin.site.register(InterestKey)
admin.site.register(Interest)
admin.site.register(InterestUser)
admin.site.register(MatchUser)
