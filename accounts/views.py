from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import SignUpForm, ProfileEditForm

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("home")
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})


@login_required
def profile(request):
    return render(request, "accounts/profile.html")


@login_required
def profile_edit(request):
    user = request.user

    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("accounts:profile")

    else:
        # Convert list → string for textbox display
        initial_data = {
            "favorite_authors": ", ".join(user.favorite_authors) if user.favorite_authors else ""
        }
        form = ProfileEditForm(instance=user, initial=initial_data)

    return render(request, "accounts/profile_edit.html", {"form": form})