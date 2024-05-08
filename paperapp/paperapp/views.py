from django.shortcuts import render
from django.core.paginator import Paginator
from multimedia.models import ImagePost, VideoPost, AudioPost


def home(request):
    """
    View for the home page.
    """
    # Get all media content
    image_media = ImagePost.objects.all().order_by("-created_at")
    video_media = VideoPost.objects.all().order_by("-created_at")
    audio_media = AudioPost.objects.all().order_by("-created_at")

    # Define Media Pagination
    image_paginator = Paginator(image_media, 4)
    video_paginator = Paginator(video_media, 4)
    audio_paginator = Paginator(audio_media, 4)

    # Get the page number
    image_page_number = request.GET.get("image_page")
    video_page_number = request.GET.get("video_page")
    audio_page_number = request.GET.get("audio_page")

    # Get the page
    image_page_obj = image_paginator.get_page(image_page_number)
    video_page_obj = video_paginator.get_page(video_page_number)
    audio_page_obj = audio_paginator.get_page(audio_page_number)

    # Other Stats to be added
    recent_20_tags = ImagePost.tags.most_common()[:20]
    total_image_posts = ImagePost.objects.count()
    total_video_posts = VideoPost.objects.count()
    total_audio_posts = AudioPost.objects.count()

    return render(
        request,
        "home.html",
        {
            "image_page_obj": image_page_obj,
            "video_page_obj": video_page_obj,
            "audio_page_obj": audio_page_obj,
            "recent_20_tags": recent_20_tags,
            "media_count": {
                "image": total_image_posts,
                "video": total_video_posts,
                "audio": total_audio_posts,
            },
        },
    )


def wiki(request):
    return render(request, "wiki.html")


def about(request):
    return render(request, "about.html")
