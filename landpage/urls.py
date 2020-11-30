# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 15:26:26 2020

@author: RomanZakharov
"""

from django.urls import path

from . import views, views_q

app_name = 'landpage'
urlpatterns = [
    path('', views.index, name='index'),
    path('fame', views.report_view, name='person_report'),
    path('quiz/', views_q.quiz_list, name='quiz_list'),
    path('quiz/<int:pk>/', views_q.show_quiz, name='show_quiz'),
    #path('comments', views.comments, name='comments')
]