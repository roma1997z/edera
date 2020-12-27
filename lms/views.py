from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from lms.models import Profile
from lms.forms import ProfileForm
from lms import tools
from django.contrib.auth.models import User


def signup(request):
    if request.method == 'POST':
        d = dict(request.POST)
        for k in ["username", "password1", "password2"]:
            d[k] = request.POST[k]
        d["email"] = request.POST["username"]
        print(d)
        form = UserCreationForm(d)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            user.email=d["email"]
            user.save()

            pr = Profile(user_id=user, role=request.POST["role"])
            pr.save()

            login(request, user)
            return redirect('lms:teacher_list')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def profile_form(request, *args, **kwargs):
    template_name = "lms/profile.html"
    context={}
    user_id = kwargs.get('id',None)
    if user_id is not None:
        theuser = User.objects.get(id=user_id)
        context["moderator"] = True
        context["id"] = user_id
        if not tools.can_edit_teacher_profile(request.user):
            return HttpResponseForbidden("Only moderators can access this page")
    else:
        theuser = request.user

    if request.method=="GET":
        form = ProfileForm(instance=theuser.profile, initial={"name":theuser.first_name})
        context.update({"form": form, "email": theuser.email})
        return render(request, template_name, context=context)
    elif request.method=="POST":
        if "change_status" in request.POST:
            if tools.can_edit_teacher_profile(request.user):
                role = request.user.profile.role
                if role=="teacher":
                    request.user.profile.role="student"
                else:
                    request.user.profile.role = "teacher"
                request.user.profile.save()

            return redirect(request.path_info)
        else:
            form = ProfileForm(data=request.POST,  files=request.FILES, instance=theuser.profile)
            if form.is_valid():
                form.save()
                theuser.first_name=request.POST["name"]
                theuser.save()
                return redirect(request.path_info)
            else:
                context.update({"form": form, "email": theuser.email})
                return render(request, template_name, context)

