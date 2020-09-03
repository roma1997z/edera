from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Quiz, QuizResult
from django.conf import settings

import json
import os

def quiz_list(request):
    return HttpResponseRedirect(reverse('landpage:show_quiz', kwargs={'pk':1}))

def quiz1_analyze(data):
    r1 = 0
    r2 = 0
    for i in range(1,8):
        key = "question"+str(i)
        r1 += int(data[key])

    for i in range(8,14):
        key = "question"+str(i)
        r2 += int(data[key])

    return {"r1":r1, "r2":r2}

@csrf_exempt
def show_quiz(request, pk):
    if request.method == "GET":
        quiz = Quiz.objects.get(note_id=pk)
        #print("path to json", settings.MEDIA_ROOT + quiz.data.url)
        #with quiz.data.file as f:
        data = json.load(quiz.data.file)
        context = {'quiz':json.dumps(data)}
        return render(request, 'landpage/show_quiz.html', context)

    elif request.method=="POST":
        data = request.POST
        print(data)
        quiz = Quiz.objects.get(note_id=pk)
        qr = QuizResult(quiz_id = quiz, email = request.POST['email'], result = json.dumps(request.POST))
        qr.save()
        result = quiz1_analyze(data)
        return JsonResponse(result)

