from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse, HttpResponseForbidden

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

from lms.models import UserTeacher, Profile, Lesson
import requests, json, datetime, pytz, random

tz=pytz.timezone(settings.TIME_ZONE)

def user_dict(el):
    return {"user_id":el.id, "name":el.first_name, "role":el.profile.role}

def pair_dict(el):
    return {"pair_id":el.note_id, "chat_id":0 if el.chat_id is None else el.chat_id, "name":str(el)}


def lesson_dict(el):
    start_time = el.date
    end_time = start_time + datetime.timedelta(minutes=el.duration)
    start_fmt = "%A, (%d %B) %H:%M "
    end_fmt = "%H:%M"
    return {"id":el.note_id, "start":start_time.astimezone(tz).strftime(start_fmt),
            "end":end_time.astimezone(tz).strftime(end_fmt),
            "notification":el.notification, "name":el.name,
            "repeat":el.repeat, "teacher":el.conn.teacher.first_name}


class AddUser(LoginRequiredMixin, TemplateView):
    template_name = 'lms/user_manage.html'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        context["users"] = [user_dict(el) for el in User.objects.all()]
        context["pairs"] = [pair_dict(el) for el in UserTeacher.objects.all()]

        chat_ids_in_use = UserTeacher.objects.filter(chat_id__isnull=False).values_list("chat_id", flat=True)

        chats = requests.get("https://api.telegram.org/bot{}/getUpdates".format(settings.TOKEN_TG))
        chat_ids = []
        chats = chats.json()['result']# json.loads(chats)['result']
        tz = pytz.timezone("Europe/Moscow")
        for el in chats:
            try:
                if "message" in el:
                    data = el['message']
                    chat_id=data['chat']['id']

                    if chat_id not in chat_ids_in_use:
                        text = data['text']
                        date = tz.localize(datetime.datetime.fromtimestamp(data['date'])).strftime('%Y-%m-%d %H:%M')
                        chat_ids.append({"chat_id":chat_id, "text":text, "date":date})
            except:
                pass
        context["chats"] = chat_ids
        context["today"] = timezone.now().strftime("%Y-%m-%d")

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if "add_user" in request.POST:
            last_id = User.objects.all().last().id
            username = "id{}".format(last_id)
            email = username+"@edera-school.com"
            password = "Ed@Era" + str(random.randint(1,10000))

            user = User(username=username, email=email, password=password, first_name=request.POST['name'])
            user.save()

            pr = Profile(user_id=user, role=request.POST["role"])
            pr.save()
            return JsonResponse({"user":user_dict(user)})

        elif "add_pair" in request.POST:
            user_id = User.objects.get(id=request.POST['user_id'])
            teacher = User.objects.get(id=request.POST['teacher'])
            ut = UserTeacher.objects.filter(user_id=user_id, teacher=teacher).first()
            if ut is None:
                ut=UserTeacher(user_id=user_id, teacher=teacher)
                ut.save()
                return JsonResponse({"pair":pair_dict(ut), "ok":1})
            else:
                return JsonResponse({"ok":0})

        elif "add_chat" in request.POST:
            pair = UserTeacher.objects.get(note_id=request.POST['pair_id'])
            chat_id = request.POST['chat_id']
            pair.chat_id = chat_id
            pair.save()
            return JsonResponse({"ok":1, "chat_id":chat_id})

        elif "add_lesson" in request.POST:
            pair = UserTeacher.objects.get(note_id=request.POST['pair_id'])
            date = str(request.POST["date"]) + " " + request.POST["time"]
            date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")#.replace(tzinfo=tz)
            print(date)
            lesson = Lesson(conn=pair, date=date, duration=int(request.POST["duration"]),
                            name=request.POST["name"], repeat=request.POST["repeat"])
            lesson.save()
            lessons = [lesson_dict(el) for el in Lesson.objects.filter(conn=pair, date__gt=timezone.now()).order_by("date")]
            return JsonResponse({"info": lessons}, safe=True)

        elif "cancel_lesson" in request.POST:
            lesson = Lesson.objects.get(note_id=request.POST["cancel_lesson"])
            pair = lesson.conn
            lesson.delete()
            lessons = [lesson_dict(el) for el in
                       Lesson.objects.filter(conn=pair, date__gt=timezone.now()).order_by("date")]
            return JsonResponse({"info":lessons})

        elif "pair_id_info" in request.POST:
            pair = UserTeacher.objects.get(note_id=request.POST["pair_id_info"])
            lessons = [lesson_dict(el) for el in Lesson.objects.filter(conn=pair, date__gt=timezone.now()).order_by("date")]
            day = datetime.datetime.today().weekday()
            week_start = datetime.datetime.today() - datetime.timedelta(days=day)
            old_lessons = [lesson_dict(el) for el in Lesson.objects.filter(conn=pair, date__range=(week_start, timezone.now())).order_by("date")]

            return JsonResponse({"info":lessons, "old_info":old_lessons}, safe=True)

        elif "delete_user" in request.POST:
            user_id = User.objects.get(id=request.POST['delete_user'])
            user_id.profile.delete()
            user_id.delete()
            return JsonResponse({"users":[user_dict(el) for el in User.objects.all()]})

        elif "delete_pair" in request.POST:
            conn = UserTeacher.objects.get(note_id=request.POST["delete_pair"])
            conn.delete()
            return JsonResponse({"pairs":[pair_dict(el) for el in UserTeacher.objects.all()]})


class AddConnection(LoginRequiredMixin, TemplateView):
    template_name = 'lms/add_user.html'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)