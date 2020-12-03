from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse, HttpResponse, HttpResponseForbidden

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

from lms.models import TeacherDesc, TeacherKey

class TeacherDescForm(LoginRequiredMixin, TemplateView):
    template_name = 'lms/teacher_desc.html'
    login_url = 'lk/login/'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        teacher = request.user
        if request.user.profile.role!="teacher":
            return HttpResponseForbidden("Only for teachers")

        desc=[]
        keys = TeacherKey.objects.filter(active=True)
        for key in keys:
            info = TeacherDesc.objects.filter(teacher=teacher, key=key).values_list("text", flat=True)
            desc.append({"note_id":key.note_id, "name":key.name, "text":info[0] if len(info)>0 else ""})
        context["keys"] = desc
        print(desc)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        teacher = request.user
        for tkey in request.POST:
            #print(tkey)
            if "key" in tkey:
                key = TeacherKey.objects.get(note_id=tkey.split("-")[1])
                info = TeacherDesc.objects.filter(teacher=teacher, key=key)
                if len(info)>0:
                    obj = info.first()
                else:
                    obj =  TeacherDesc(teacher=teacher, key=key)
                obj.text = request.POST[tkey]
                obj.save()

        return redirect("lms:teacher_desc")


class InterestForm():
    template_name = 'lms/teacher_desc.html'
    login_url = 'lk/login/'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        teacher = request.user


    def post(self, request, *args, **kwargs):
        teacher = request.user
