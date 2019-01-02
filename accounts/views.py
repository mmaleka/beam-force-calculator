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
