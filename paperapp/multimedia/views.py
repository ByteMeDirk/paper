import os
import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import TrigramSimilarity
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from paperapp import settings
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

            if post_type == "audio":
                # Only audio posts have thumbnails
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
        request,
        "multimedia/create_post.html",
        {
            "form": form,
            "post_type": post_type,
            "ckeditor_config": settings.CKEDITOR_5_CONFIGS["default"],
        },
    )


@login_required(login_url="login")
def edit_post(request, post_type, post_id):
    """
    This view allows the user to edit a post of the specified type.
    """
    if post_type == "video":
        post = get_object_or_404(VideoPost, pk=post_id)
    elif post_type == "audio":
        post = get_object_or_404(AudioPost, pk=post_id)
    else:
        post = get_object_or_404(ImagePost, pk=post_id)

    # Check if the request.user is the author of the post
    if post.author.id != request.user.id:
        messages.error(request, "You are not authorized to edit this post.")
        return redirect("home")

    form = (
        VideoPostForm(request.POST or None, request.FILES or None, instance=post)
        if post_type == "video"
        else (
            AudioPostForm(request.POST or None, request.FILES or None, instance=post)
            if post_type == "audio"
            else ImagePostForm(
                request.POST or None, request.FILES or None, instance=post
            )
        )
    )

    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            # If a new file is not provided, keep the old file
            if not request.FILES:
                post.file = post.file

            post.save()
            form.save_m2m()  # Save many-to-many fields
            messages.success(request, "Post updated successfully.")
            return redirect("home")

    return render(
        request,
        "multimedia/edit_post.html",
        {
            "form": form,
            "post_type": post_type,
            "post": post,
            "ckeditor_config": settings.CKEDITOR_5_CONFIGS["default"],
        },
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

    # Check if the request.user is the author of the post
    if post.author.id != request.user.id:
        messages.error(request, "You are not authorized to delete this post.")
        return redirect("home")

    post.delete()
    messages.success(request, "Post deleted successfully.")
    return redirect("home")


@login_required(login_url="login")
def view_post(request, post_type, post_id):
    """
    This view allows the user to view a post of the specified type.
    """
    if post_type == "video":
        post = get_object_or_404(VideoPost, pk=post_id)
        artists_posts = VideoPost.objects.filter(author=post.author)[:5]
        similar_posts = (
            VideoPost.objects.annotate(
                similarity=TrigramSimilarity("tags__name", post.tags.first().name)
            )
            .filter(similarity__gt=0.3)
            .exclude(id=post_id)
            .order_by("id", "-similarity")
            .distinct("id")[:5]
        )

    elif post_type == "audio":
        post = get_object_or_404(AudioPost, pk=post_id)
        artists_posts = AudioPost.objects.filter(author=post.author)[:5]
        similar_posts = (
            AudioPost.objects.annotate(
                similarity=TrigramSimilarity("tags__name", post.tags.first().name)
            )
            .filter(similarity__gt=0.3)
            .exclude(id=post_id)
            .order_by("id", "-similarity")
            .distinct("id")[:5]
        )
    else:
        post = get_object_or_404(ImagePost, pk=post_id)
        artists_posts = ImagePost.objects.filter(author=post.author)[:5]
        similar_posts = (
            ImagePost.objects.annotate(
                similarity=TrigramSimilarity("tags__name", post.tags.first().name)
            )
            .filter(similarity__gt=0.3)
            .exclude(id=post_id)
            .order_by("id", "-similarity")
            .distinct("id")[:5]
        )

    # Increment the view count
    post.views += 1
    post.save()

    return render(
        request,
        "multimedia/view_post.html",
        {
            "post": post,
            "post_type": post_type,
            "artists_posts": artists_posts,
            "similar_posts": similar_posts,
        },
    )


def search(request):
    """
    This view allows the user to search for posts.
    """
    query = request.GET.get("q")
    if query:
        image_results = (
            ImagePost.objects.annotate(
                similarity=TrigramSimilarity("author__username", query)
                + TrigramSimilarity("tags__name", query),
            )
            .filter(similarity__gt=0.3)
            .order_by("id", "-created_at", "-similarity")
            .distinct("id")
        )[:100]

        video_results = (
            VideoPost.objects.annotate(
                similarity=TrigramSimilarity("author__username", query)
                + TrigramSimilarity("tags__name", query),
            )
            .filter(similarity__gt=0.3)
            .order_by("id", "-created_at", "-similarity")
            .distinct("id")
        )[:100]

        audio_results = (
            AudioPost.objects.annotate(
                similarity=TrigramSimilarity("author__username", query)
                + TrigramSimilarity("tags__name", query),
            )
            .filter(similarity__gt=0.3)
            .order_by("id", "-created_at", "-similarity")
            .distinct("id")
        )[:100]
    else:
        image_results = ImagePost.objects.none()
        video_results = VideoPost.objects.none()
        audio_results = AudioPost.objects.none()

    return render(
        request,
        "multimedia/search_results.html",
        {
            "image_results": image_results,
            "video_results": video_results,
            "audio_results": audio_results,
            "query": query,
        },
    )


def vote(request, media_id, media_type, vote_type):
    if request.user.is_authenticated:
        media_kwargs = {
            "image_id": None,
            "video_id": None,
            "audio_id": None,
        }

        if media_type == "image":
            media = ImagePost.objects.get(id=media_id)
            media_kwargs["image_id"] = media
        elif media_type == "video":
            media = VideoPost.objects.get(id=media_id)
            media_kwargs["video_id"] = media
        else:  # audio
            media = AudioPost.objects.get(id=media_id)
            media_kwargs["audio_id"] = media

        vote, created = MediaRating.objects.get_or_create(
            user=request.user, **media_kwargs
        )

        if vote_type == "up":
            vote.vote = 1
        else:  # down
            vote.vote = 0

        vote.save()

        total_votes = MediaRating.get_total_votes(media_id, media_type)
        return JsonResponse({"success": True, "total_votes": total_votes})
    else:
        return JsonResponse({"success": False, "message": "User not authenticated"})


@login_required(login_url="login")
def view_gallery(request, media_type):
    """
    This view displays all the media posts using pagination.
    """
    media_models = {
        "image": ImagePost,
        "video": VideoPost,
        "audio": AudioPost,
    }

    sort_by = request.GET.get(
        "sort_by", "-created_at"
    )  # Default sorting is by date created
    if media_type in media_models:
        # Get all media of the specified type
        media_model = media_models[media_type]
        media_objects = media_model.objects.annotate(
            votes=Sum("mediarating__vote")
        ).order_by(sort_by)

        # Define Pagination
        paginator = Paginator(
            media_objects, 12
        )  # Increase the number of objects per page

        # Get the page number
        page_number = request.GET.get("page")

        # Get the page
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            "multimedia/view_gallery.html",
            {
                f"{media_type}_page_obj": page_obj,
                "media_type": media_type,
            },
        )

    else:
        return redirect("home")
