from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.models import User

from lms.models import TeacherDesc, InterestKey, Interest

class TeacherList(LoginRequiredMixin, TemplateView):
    template_name = 'lms/teacher_list.html'
    login_url = 'lk/login/'

    def teacher_info(self, teacher):
        info = TeacherDesc.objects.filter(teacher=teacher).values_list("key__key", "text")
        print(info)
        info = {k:v for k,v in info}
        return info

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        teachers = User.objects.filter(profile__role="teacher")
        infos = []
        for teacher in teachers:
            infos.append({"teacher":teacher, "info":self.teacher_info(teacher)})
        context["teachers"] = infos

        keys = InterestKey.objects.filter(active=True)
        for key in keys:
            interests = Interest.objects.filter(key=key)
        #    print(key.interest)
        # interests = Interest.objects.filter

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse("lms:teacher_list"))