from django.urls import path

from . import views, views_student, views_teacher

app_name = 'lms'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views_student.TeacherList.as_view(), name='teacher_list'),
]