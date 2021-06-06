from django.urls import path

from . import views, views_student, views_teacher, views_bot

app_name = 'lms'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile_form, name='profile'),
    path('profile/<int:id>/', views.profile_form, name='profile'),
    path('profile/desc/', views_teacher.TeacherDescForm.as_view(), name='teacher_desc'),
    path('profile/desc/<int:id>/', views_teacher.TeacherDescForm.as_view(), name='teacher_desc'),
    path('profile/time/', views_teacher.AddTime.as_view(), name='teacher_time'),
    path('profile/time/<int:id>/', views_teacher.AddTime.as_view(), name='teacher_time'),
    path('lesson/', views_student.LessonList.as_view(), name='lesson_list'),
    path('choose/<int:id>/', views_student.ChooseTime.as_view(), name='choose_time'),
    path('choose/', views_student.ChooseTime2.as_view(), name='choose_time'),
    path('choose/type/', views_student.ChooseType.as_view(), name='choose_type'),
    path('choose/day/', views_student.ChooseDay.as_view(), name='choose_day'),
    path('', views_student.TeacherList.as_view(), name='teacher_list'),
    path('bot/msg/', views_bot.send_msg, name='bot_send_msg'),
]