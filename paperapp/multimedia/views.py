from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import os
import uuid
from django.core.files.base import ContentFile
from .forms import ImagePostForm, VideoPostForm, AudioPostForm


@login_required
def select_post_type(request):
    """
    This view allows the user to select the type of post they want to create.
    """
    return render(request, "multimedia/select_post_type.html")


@login_required
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
            ext = os.path.splitext(post.file.name)[1]
            post.file.name = file_name + ext

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

    return render(request, "multimedia/create_post.html", {"form": form, "post_type": post_type})
