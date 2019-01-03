from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .forms import UserLoginForm, UserRegisterForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from analytics.models import RegisterCount
from beam_diagram.models import Beamlength
import socket

# Create your views here.




def login_view(request):
    print(request.user.is_authenticated)
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    print("request.user.is_authenticated1", request.user.is_authenticated)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        print("request.user.is_authenticated2", request.user.is_authenticated)
        # Redirect here
        if next:
            return redirect(next)
        return redirect('new_beam:new_beam')

    context = {
        "form": form,
        "title": "Login",
    }

    return render(request, 'accounts/form_login.html', context)



def register_view(request):


    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        print("IP dress: ", s.getsockname()[0])
        IP = s.getsockname()[0]
        s.close()


        view, created = RegisterCount.objects.get_or_create(
            ip_address = str(IP),
        )
        if view:
            view.views_count += 1
            view.save()

    except Exception as e:
        print("Error getting IP adress", e)

    form = UserRegisterForm(request.POST or None)





    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect('new_beam:new_beam')

    context = {
                'title': 'Sign Up',
                'form': form,
            }
    return render(request, "accounts/form_register.html", context)



def logout_view(request):
    logout(request)
    return redirect('new_beam:new_beam')


@login_required
def profile_view(request):

    if request.user.is_authenticated:
        user = request.user
    else:
        user = 5

    print("user: ", user)
    project_list = Beamlength.objects.filter(user=request.user)

    paginator = Paginator(project_list, 20) # Show 25 contacts per page

    page = request.GET.get('page')
    orders = paginator.get_page(page)

    context = {
        'project_list': project_list,
    }

    return render(request, "accounts/profile.html", context)
