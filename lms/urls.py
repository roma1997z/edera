from django.urls import path

from . import views, views_student, views_teacher

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
    path('', views_student.TeacherList.as_view(), name='teacher_list'),
]