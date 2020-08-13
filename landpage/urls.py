# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 15:26:26 2020

@author: RomanZakharov
"""

from django.urls import path

from . import views

app_name = 'camps'
urlpatterns = [
    path('', views.index, name='index'),
    #path('comments', views.comments, name='comments')
]