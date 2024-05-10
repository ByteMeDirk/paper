from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render

from multimedia.models import ImagePost, VideoPost, AudioPost
from multimedia.views import view_post
from users.views import view_user
from .forms import ReportUserForm, ReportPostForm, ModerateUserForm, ModeratePostForm
from .models import ReportPost, ReportUser


@login_required(login_url="login")
def report_user(request, user_id):
    """
    View for reporting a user.
    """
    user = User.objects.get(id=user_id)

    # Check if the user has already reported this user
    existing_report = ReportUser.objects.filter(reporter=request.user, reported=user_id, resolved=False).first()
    if existing_report:
        messages.error(request, "You have already reported this user and it's still under review.")
        return view_user(request, user_id)

    if request.method == "POST":
        form = ReportUserForm(request.POST)

        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user
            report.reported = user
            report.save()

            messages.success(request, "User reported successfully.")
            return view_user(request, user_id)
    else:
        form = ReportUserForm()

    return render(request, "moderation/report_user.html", {"form": form, "user": user})


@login_required(login_url="login")
def report_post(request, post_id, post_type):
    """
    View for reporting a post.
    Check if the user has already reported this post and it's still unresolved
    """

    existing_report = None
    if post_type == "image":
        post = ImagePost.objects.get(id=post_id)
        existing_report = ReportPost.objects.filter(reporter=request.user, image=post_id, resolved=False).first()
    elif post_type == "video":
        post = VideoPost.objects.get(id=post_id)
        existing_report = ReportPost.objects.filter(reporter=request.user, video=post_id, resolved=False).first()
    elif post_type == "audio":
        post = AudioPost.objects.get(id=post_id)
        existing_report = ReportPost.objects.filter(reporter=request.user, audio=post_id, resolved=False).first()

    if existing_report:
        messages.error(request, "You have already reported this post and it's still under review.")
        return view_post(request, post_type, post_id)

    if request.method == "POST":
        form = ReportPostForm(request.POST)

        if form.is_valid():
            report = form.save(commit=False)
            report.reporter = request.user

            if post_type == "image":
                report.image = post
            elif post_type == "video":
                report.video = post
            elif post_type == "audio":
                report.audio = post

            try:
                report.save()
                messages.success(request, "Post reported successfully.")
            except ValidationError as e:
                messages.error(request, str(e))

            return view_post(request, post_type, post_id)
    else:
        form = ReportPostForm()

    return render(request, "moderation/report_post.html", {"form": form, "post": post, "post_type": post_type})


@login_required(login_url="login")
@staff_member_required
def moderator_dashboard(request):
    """
    View for the moderator dashboard.
    """

    # Get all unresolved reports
    user_reports = ReportUser.objects.filter(resolved=False)
    post_reports = ReportPost.objects.filter(resolved=False)

    return render(request, "moderation/moderator_dashboard.html",
                  {"user_reports": user_reports, "post_reports": post_reports})



@login_required(login_url="login")
@staff_member_required
def resolve_user_report(request, report_id):
    """
    View for resolving a user report.
    """
    report = ReportUser.objects.get(id=report_id)

    if request.method == "POST":
        form = ModerateUserForm(request.POST, instance=report)

        if form.is_valid():
            form.save()
            messages.success(request, "Report resolved successfully.")
            return moderator_dashboard(request)
    else:
        form = ModerateUserForm(instance=report)

    return render(request, "moderation/resolve_user_report.html", {"form": form, "report": report})


@login_required(login_url="login")
@staff_member_required
def resolve_post_report(request, report_id):
    """
    View for resolving a post report.
    """
    report = ReportPost.objects.get(id=report_id)

    if request.method == "POST":
        form = ModeratePostForm(request.POST, instance=report)

        if form.is_valid():
            form.save()
            messages.success(request, "Report resolved successfully.")
            return moderator_dashboard(request)
    else:
        form = ModeratePostForm(instance=report)

    return render(request, "moderation/resolve_post_report.html", {"form": form, "report": report})