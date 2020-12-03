from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from lms.models import Profile
from lms.forms import ProfileForm

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
def profile_form(request):
    template_name = "lms/profile.html"
    if request.method=="GET":
        form = ProfileForm(instance=request.user.profile, initial={"name":request.user.first_name})
        return render(request, template_name, context={"form":form, "email":request.user.email})
    elif request.method=="POST":
        form = ProfileForm(data=request.POST,  files=request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.first_name=request.POST["name"]
            request.user.save()
            return redirect("lms:profile")
        else:
            return render(request, template_name, {"form":form, "email":request.user.email})

