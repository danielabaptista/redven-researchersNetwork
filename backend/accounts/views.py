from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.http import JsonResponse
from .models import StudentProfile, ResearcherProfile
import json
import os
from django.conf import settings
from .models import StudentProfile, ResearcherProfile


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_approved:
                login(request, user)
                return redirect("home")
            else:
                form.add_error(None, "Your account is not approved yet")
    else:
        form = CustomAuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")

