from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from users.forms import UserRegisterForm


def register(request):
    if request.method =="POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Аккаунт создан для {username}!")
            return redirect("shop-home")
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})