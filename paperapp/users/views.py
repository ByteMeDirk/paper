from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from multimedia.models import ImagePost, VideoPost, AudioPost
from paperapp import settings
from paperapp.utils import get_media_pagination
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
    image_page_obj, video_page_obj, audio_page_obj = get_media_pagination(
        request, 8, "-created_at", request.user.id
    )

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

    return render(
        request,
        "users/profile.html",
        {
            "form": form,
            "profile": profile,
            "image_page_obj": image_page_obj,
            "video_page_obj": video_page_obj,
            "audio_page_obj": audio_page_obj,
            "ckeditor_config": settings.CKEDITOR_5_CONFIGS["default"],
        },
    )


def view_user(request, user_id):
    """
    This view displays the profile of a specific user.
    """
    profile = Profile.objects.get(user_id=user_id)
    image_page_obj, video_page_obj, audio_page_obj = get_media_pagination(
        request, 8, "-created_at", user_id
    )

    total_posts = (
            ImagePost.objects.filter(author=profile.user).count()
            + VideoPost.objects.filter(author=profile.user).count()
            + AudioPost.objects.filter(author=profile.user).count()
    )

    if not profile.user.is_active:
        messages.error(request, "This user's profile is hidden.")
        return redirect("home")

    return render(
        request,
        "users/view_user.html",
        {
            "user_profile": profile,
            "image_page_obj": image_page_obj,
            "video_page_obj": video_page_obj,
            "audio_page_obj": audio_page_obj,
            "total_posts": total_posts,
        },
    )


@login_required(login_url="login")
@staff_member_required
def hide_user(request, user_id):
    """
    This view hides a user's profile from the public view.
    It is only accessible to staff members.
    """
    user = Profile.objects.get(user_id=user_id)
    user.hidden = True
    user.save()
    messages.success(request, "User hidden successfully.")
    return redirect("moderator_dashboard")


@login_required
@staff_member_required
def deactivate_user(request, user_id):
    previous_page = request.META.get("HTTP_REFERER")
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    messages.success(request, f"User {user.username} has been deactivated.")
    return HttpResponseRedirect(previous_page)


@login_required
@staff_member_required
def activate_user(request, user_id):
    previous_page = request.META.get("HTTP_REFERER")
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, f"User {user.username} has been activated.")
    return HttpResponseRedirect(previous_page)
