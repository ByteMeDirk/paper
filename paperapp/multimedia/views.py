import os
import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ImagePostForm, VideoPostForm, AudioPostForm
from .models import VideoPost, AudioPost, ImagePost, MediaRating


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


def search(request):
    """
    This view allows the user to search for posts.

    ToDo: When Moving over to Postgres, use TrigramSimilarity for better search results.
    """
    query = request.GET.get("q")
    if query:
        image_results = ImagePost.objects.filter(
            Q(author__username__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
        video_results = VideoPost.objects.filter(
            Q(author__username__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
        audio_results = AudioPost.objects.filter(
            Q(author__username__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    else:
        image_results = ImagePost.objects.none()
        video_results = VideoPost.objects.none()
        audio_results = AudioPost.objects.none()

    return render(request, 'multimedia/search_results.html', {
        'image_results': image_results,
        'video_results': video_results,
        'audio_results': audio_results,
    })


def vote(request, media_id, media_type, vote_type):
    if request.user.is_authenticated:
        media_kwargs = {
            'image_id': None,
            'video_id': None,
            'audio_id': None,
        }

        if media_type == 'image':
            media = ImagePost.objects.get(id=media_id)
            media_kwargs['image_id'] = media
        elif media_type == 'video':
            media = VideoPost.objects.get(id=media_id)
            media_kwargs['video_id'] = media
        else:  # audio
            media = AudioPost.objects.get(id=media_id)
            media_kwargs['audio_id'] = media

        vote, created = MediaRating.objects.get_or_create(user=request.user, **media_kwargs)

        if vote_type == 'up':
            vote.vote = 1
        else:  # down
            vote.vote = -1

        vote.save()

        total_votes = MediaRating.get_total_votes(media_id, media_type)

        return JsonResponse({"success": True, "total_votes": total_votes})
    else:
        return JsonResponse({"success": False, "message": "User not authenticated"})
