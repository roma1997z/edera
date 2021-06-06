from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters
import telegram
import datetime, pytz

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone

from django.conf import settings

from .models import UserTeacher, Lesson
from .tools_bot import *

admin_chat_id =421373121

@csrf_exempt
def index_tg(request):
    host = request.get_host()
    if (request.method == "POST"):
        bot = telegram.Bot(settings.token_tg)


@csrf_exempt
def send_msg(request):
    context = {}
    bot = telegram.Bot(settings.TOKEN_TG)

    if (request.method=="GET"):
        context["conns"] = UserTeacher.objects.all()
        start_date = timezone.now()
        end_date = timezone.now()+datetime.timedelta(hours=24)
        lessons = Lesson.objects.filter(date__range=(start_date, end_date), notification=False)

        # admin send
        text = "Начата рассылка сообщений"
        text += "\n"
        text += "\n".join(str(el.conn)+" " + format_text(el.date) for el in lessons)
        bot.send_message(chat_id=admin_chat_id,
                         text=text)

        for lesson in lessons:
            try:
                chat_id = lesson.conn.chat_id
                text = format_text(lesson.date)
                bot.send_message(chat_id=chat_id,
                                 text=text)
                lesson.notification = True
                lesson.save()
            except Exception as e:
                # admin error
                text = "Ошибка "+str(e) + "\n"
                text += str(lesson.conn)
                bot.send_message(chat_id=admin_chat_id,
                                 text=text)

        return render(request, "lms/bot_test.html", context)

    if request.method=="POST":
        chat_id = request.POST["chat_id"]
        conn = UserTeacher.objects.filter(chat_id=chat_id).first()

        lesson = Lesson.objects.filter(conn=conn, date__gt=timezone.now(), notification=False).first()
        if lesson is not None:
            bot.send_message(chat_id=chat_id,
                         text="Ваш следующий урок {}".format(lesson.date))
            lesson.notification=True
        else:
            print("lesson doesn't exist")
        return HttpResponse(200)
