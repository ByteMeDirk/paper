import os
import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ImagePostForm, VideoPostForm, AudioPostForm
from .models import VideoPost, AudioPost, ImagePost


@login_required(login_url="login")
def select_post_type(request):
    """
    This view allows the user to select the type of post they want to create.
    """
    return render(request, "multimedia/select_post_type.html")


@login_required(login_url="login")
def create_post(request, post_type):
    """
    This view allows the user to create a post of the specified type.
    """
    if request.method == "POST":
        if post_type == "video":
            form = VideoPostForm(request.POST, request.FILES)
        elif post_type == "audio":
            form = AudioPostForm(request.POST, request.FILES)
        else:
            form = ImagePostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            # Change File name to a unique name
            file_name = str(uuid.uuid4())
            file_ext = os.path.splitext(post.file.name)[1]
            post.file.name = file_name + file_ext
            thumbnail_ext = os.path.splitext(post.thumbnail.name)[1]
            post.thumbnail.name = file_name + thumbnail_ext

            post.save()
            form.save_m2m()  # Save many-to-many fields
            messages.success(request, "Post created successfully.")
            return redirect("home")

    else:
        if post_type == "video":
            form = VideoPostForm()
        elif post_type == "audio":
            form = AudioPostForm()
        else:
            form = ImagePostForm()

    return render(
        request, "multimedia/create_post.html", {"form": form, "post_type": post_type}
    )


@login_required(login_url="login")
def edit_post(request, post_type, post_id):
    """
    This view allows the user to edit a post of the specified type.
    """
    if post_type == "video":
        post = get_object_or_404(VideoPost, pk=post_id)
        form = VideoPostForm(request.POST or None, request.FILES or None, instance=post)
    elif post_type == "audio":
        post = get_object_or_404(AudioPost, pk=post_id)
        form = AudioPostForm(request.POST or None, request.FILES or None, instance=post)
    else:
        post = get_object_or_404(ImagePost, pk=post_id)
        form = ImagePostForm(request.POST or None, request.FILES or None, instance=post)

    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            # Change File name to a unique name
            file_name = str(uuid.uuid4())
            ext = os.path.splitext(post.file.name)[1]
            post.file.name = file_name + ext

            post.save()
            form.save_m2m()  # Save many-to-many fields
            messages.success(request, "Post updated successfully.")
            return redirect("home")

    return render(
        request, "multimedia/edit_post.html", {"form": form, "post_type": post_type}
    )


@login_required(login_url="login")
def delete_post(request, post_type, post_id):
    """
    This view allows the user to delete a post of the specified type.
    """
    if post_type == "video":
        post = get_object_or_404(VideoPost, pk=post_id)
    elif post_type == "audio":
        post = get_object_or_404(AudioPost, pk=post_id)
    else:
        post = get_object_or_404(ImagePost, pk=post_id)

    post.delete()
    messages.success(request, "Post deleted successfully.")
    return redirect("home")
