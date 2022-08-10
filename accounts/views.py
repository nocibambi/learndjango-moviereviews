from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCreateForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError


def signupaccount(request):
    if request.method == "GET":
        return render(request, "signupaccount.html", {"form": UserCreateForm})
    else:
        error = ""
        if request.POST["password1"] != request.POST["password2"]:
            error = "Passwords do not match"
        elif (request.POST["username"]) in request.POST["password1"]:
            error = "Password cannot resemble username"
        elif len(request.POST["password1"]) < 8:
            error = "Password must contain at least 8 characters"

        if error:
            return render(
                request,
                "signupaccount.html",
                {"form": UserCreateForm, "error": error},
            )

        try:
            user = User.objects.create_user(
                request.POST["username"], password=request.POST["password1"]
            )
            user.save()
            login(request, user)
            return redirect("home")
        except IntegrityError:
            return render(
                request,
                "signupaccount.html",
                {
                    "form": UserCreateForm,
                    "error": "Username already taken. Choose another username.",
                },
            )


@login_required
def logoutaccount(request):
    logout(request)
    return redirect("home")


def loginaccount(request):
    if request.method == "GET":
        return render(request, "loginaccount.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )

        if user is None:
            return render(
                request,
                "loginaccount.html",
                {
                    "form": AuthenticationForm,
                    "error": "Invalid username and password pair",
                },
            )
        else:
            login(request, user)
            return redirect("home")
