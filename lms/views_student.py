from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

from lms.models import TeacherTime, TeacherDesc, InterestKey, Interest, InterestUser
from lms.models import MatchUser, Lesson, LessonBook

from lms import tools
import portion as P
import math
import numpy as np
import datetime


class ChooseType(LoginRequiredMixin, TemplateView):
    template_name = 'lms/choose_type.html'
    login_url = '/lk/login/'
    keys = ['typ', 'subject', 'grade']

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["interests"] = tools.get_interest_json(self.keys)

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        interests = request.POST.getlist("interest")
        tools.set_interest(interests, request.user)

        short = InterestUser.objects.filter(user_id=request.user, interest__key__key='typ', interest__symbol='short')
        if len(short) == 0:
            return redirect("lms:teacher_list")
        else:
            return redirect("lms:choose_time")



class TeacherList(LoginRequiredMixin, TemplateView):
    template_name = 'lms/teacher_list.html'
    login_url = '/lk/login/'
    keys = ['exam', 'subject', 'grade']

    def teacher_info(self, teacher):
        info = TeacherDesc.objects.filter(teacher=teacher).values_list("key__key","key__name", "text")
        print(info)
        info = [{"key":k, "name":name, "text":v} for k,name,v in info]
        # print(model_to_dict(teacher))
        # print(teacher.user_id)
        return {"name":teacher.first_name,
                "photo": teacher.profile.photo.url if teacher.profile.photo else "",
                "user_id":teacher.id, "info":info}

    def next_teacher(self, request, teacher_id=None):
        teacher_ids = request.session.get("teacher_ids", [])
        if teacher_id is not None:
            teacher_ids.append(int(teacher_id))
            request.session["teacher_ids"] = teacher_ids
        print(teacher_ids)
        teachers = User.objects.filter(profile__role="teacher").exclude(id__in=teacher_ids)
        if len(teachers)>0:
            return teachers.first()
        else:
            return None

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if tools.can_edit_teacher_profile(request.user):
            context["moderator"] = True
        # for interest filtering
        context["interests"] = tools.get_interest_json(self.keys)

        # teacher list
        """
        infos = []
        for teacher in teachers:
            infos.append({"teacher":teacher, "info":self.teacher_info(teacher)})
        context["teachers"] = infos
        """

        teacher = self.next_teacher(request)
        if teacher is not None:
            context["teacher"] = self.teacher_info(teacher)

        context['user_interests'] = list(InterestUser.objects.filter(user_id=request.user).values_list("interest__note_id", flat=True))

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_id = request.user

        # save match
        teacher_id = request.POST.get("teacher_id", None)
        if "like" in request.POST:
            like = int(request.POST["like"])
            if like != 0:
                like = False if like<0 else True
                teacher = get_object_or_404(User, id=teacher_id)
                mu = MatchUser(user_id=user_id, teacher=teacher, like=like)
                mu.save()

            teacher = self.next_teacher(request, teacher_id)
            if teacher is not None:
                teacherd = self.teacher_info(teacher)
                return JsonResponse(teacherd, safe=False)
            else:
                return JsonResponse({"error":"No more teachers"}, safe=False)

        elif "filter" in request.POST:
            request.session.pop("teacher_ids", None)
            interests = request.POST.getlist("interest")
            tools.set_interest(interests, user_id)
            # interests = request.POST["filter"]

        return HttpResponseRedirect(reverse("lms:teacher_list"))


class ChooseTime2(LoginRequiredMixin, TemplateView):
    template_name = 'lms/choose_time2.html'
    login_url = '/lk/login/'

    splits = 4
    step = int(60 / splits)
    start_hour = 8

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        dim = (24 - self.start_hour) * self.splits
        m = np.zeros((7, dim))
        for day in range(7):
            time = P.empty()
            tt = TeacherTime.objects.filter(teacher=request.user, day=day)
            for t in tt:
                time = time|P.closed(tools.to_min(t.start_time), tools.to_min(t.end_time))
            print(time)
            if time != P.empty():
                for t in range(dim):
                    if P.closed(t*self.step+self.start_hour*60, (t+1)*self.step+self.start_hour*60) in time:
                        m[day, t] = 1
        print(m.shape)
        context["freetime"] = m.tolist()

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        step = self.step
        start_hour = self.start_hour

        TeacherTime.objects.filter(teacher=request.user).delete()
        for day in range(7):
            times = P.empty()
            for time in range((24-self.start_hour)*self.step):
                if request.POST.get("{}_{}".format(day, time), False):
                    times = times|P.closed(time, time+1)

            if times!=P.empty():
                for time in list(times):
                    print(time.lower, time.upper)
                    start_time = tools.to_time(time.lower, step, duration=start_hour*60)
                    end_time = tools.to_time(time.upper, step, duration=start_hour*60)
                    print(start_time, end_time)
                    tt = TeacherTime(teacher=request.user, day=day, start_time = start_time, end_time = end_time)
                    tt.save()
                #duration = request.POST["day_{}".format(day)]
                #LessonBook(day=day, duration=duration, user_id=request.user, )


        return redirect(reverse('lms:choose_time'))


class ChooseTime(LoginRequiredMixin, TemplateView):
    template_name = 'lms/choose_time.html'
    login_url = '/lk/login/'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        teacher = User.objects.get(id=self.kwargs['id'])

        t_all = []
        week = ["Пн", "Вт", "Ср", "Чт", "Пт", "Cб", "Вс"]
        my_week = []
        for day in range(7):
            t = tools.get_free_teacher_time(teacher, day)

            if t[0]!=P.empty():
                t_all.append([tools.min_to_time(el.lower), tools.min_to_time(el.upper)] for el in t)
                my_week.append((day, week[day]))
            else:
                t_all.append(())
        context["times"] = t_all
        context["week"] = my_week
        context["teacher"] = teacher

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        teacher = User.objects.get(id=self.kwargs['id'])
        day = request.POST["day"]
        print(request.POST)
        if "choose_time" in request.POST:
            tt = request.POST["time"].split("-")
            l = Lesson(teacher=teacher, day=int(request.POST["day"]), user_id=request.user,
                                                start_time=tt[0], end_time=tt[1], active=2)
            l.save()
            return redirect(reverse("lms:lesson_list"))

        t = tools.get_free_teacher_time(teacher, day)

        duration = int(request.POST["duration"])
        good_times = []
        step_time = 15

        times = list(t)

        if len(times)>0:
            for el in times:
                start_time=el.lower
                end_time=el.upper
                if end_time-start_time>=int(duration):
                    point_0 = math.ceil(start_time/step_time)
                    point_1 = math.floor((end_time-duration)/step_time)
                    good_times += [(tools.to_time(time_0, step_time), tools.to_time(time_0, step_time,duration)) for time_0 in range(point_0, point_1+1)]
        print(good_times)
        return JsonResponse({"times":good_times})


class LessonList(LoginRequiredMixin, TemplateView):
    template_name = 'lms/lesson_list.html'
    login_url = '/lk/login/'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        context["matches"] = MatchUser.objects.filter(user_id=request.user, like=True)
        lessons = []
        if request.user.profile.role=="teacher":
            context["teacher"] = True
            for day in range(7):
                l = Lesson.objects.filter(teacher=request.user, day=day, active__gt=0).order_by("start_time")
                lessons.append(l)
        else:
            for day in range(7):
                l = Lesson.objects.filter(user_id=request.user, day=day, active__gt=0).order_by("start_time")
                lessons.append(l)
        context["lessons"] = lessons

        print(context)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        l = Lesson.objects.get(note_id=request.POST["note_id"])
        l.active = int(request.POST["decision"])
        l.save()
        return redirect(self.request.path_info)