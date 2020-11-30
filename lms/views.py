from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from lms.models import Profile

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

            pr = Profile(user_id=user, role="student")
            pr.save()
            login(request, user)
            return redirect('lms:teacher_list')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
