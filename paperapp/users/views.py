from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from multimedia.models import ImagePost, VideoPost, AudioPost
from .forms import SignupForm, LoginForm, ProfileForm
from .models import Profile


def user_signup(request):
    """
    This view handles the user signup process. It renders the signup form and processes the form submission.
    """
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully.")
            return redirect("login")
    else:
        form = SignupForm()
    return render(request, "users/signup.html", {"form": form})


def user_login(request):
    """
    This view handles the user login process. It renders the login form and processes the form submission.
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "You are now logged in.")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def user_logout(request):
    """
    This view logs out the user and redirects to the login page.
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


@login_required(login_url="login")
def user_profile(request):
    """
    This view displays the user profile page. They can edit their profile information here.
    """
    # Get the current user's profile
    profile = request.user.profile

    if request.method == "POST":
        # Populate the form with the existing profile data and the submitted data
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Save the form, which updates the profile
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        # Populate the form with the existing profile data
        form = ProfileForm(instance=profile)

    return render(request, "users/profile.html", {"form": form, "profile": profile})


def view_user(request, user_id):
    """
    This view displays the profile of a specific user.
    """
    user_profile = Profile.objects.get(user_id=user_id)
    image_media = ImagePost.objects.filter(author_id=user_id)
    video_media = VideoPost.objects.filter(author_id=user_id)
    audio_media = AudioPost.objects.filter(author_id=user_id)
    return render(request, "users/view_user.html",
                  {"user_profile": user_profile, "image_media": image_media, "video_media": video_media, "audio_media": audio_media})
