from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

from lms.models import TeacherDesc, InterestKey, Interest
from lms.models import MatchUser

class TeacherList(LoginRequiredMixin, TemplateView):
    template_name = 'lms/teacher_list.html'
    login_url = 'lk/login/'

    def teacher_info(self, teacher):
        info = TeacherDesc.objects.filter(teacher=teacher).values_list("key__key", "text")
        print(info)
        info = {k:v for k,v in info}
        # print(model_to_dict(teacher))
        # print(teacher.user_id)
        return {"name":teacher.first_name, "photo": teacher.profile.photo.url if teacher.profile.photo else "", "user_id":teacher.id, "info":info}

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

        #teacher_ids = request.session.get("teacher_ids", [])
        #teachers = User.objects.filter(profile__role="teacher").exclude(user_id__in=teacher_ids)


        # for interest filtering
        interests = []
        interest_key = InterestKey.objects.filter(active=True)
        for key in interest_key:
            key_interests = Interest.objects.filter(active=True, key=key).values("note_id", "name")
            interests.append({"name":key.name, "key_id":key.note_id, "options":key_interests})
        context["interests"]=interests

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
            print(request.POST)
            # interests = request.POST["filter"]


        return HttpResponseRedirect(reverse("lms:teacher_list"))