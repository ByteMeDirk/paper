from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from multimedia.models import ImagePost, VideoPost, AudioPost
from paperapp.utils import get_media_pagination


@login_required(login_url="about")
def home(request):
    """
    View for the home page.
    """
    # Get the pages
    image_page_obj, video_page_obj, audio_page_obj = get_media_pagination(
        request, 4, "-created_at"
    )

    # Other Stats to be added
    recent_20_tags = ImagePost.tags.most_common()[:20]

    return render(
        request,
        "home.html",
        {
            "image_page_obj": image_page_obj,
            "video_page_obj": video_page_obj,
            "audio_page_obj": audio_page_obj,
            "recent_20_tags": recent_20_tags,
        },
    )


def wiki(request):
    return render(request, "wiki.html")


def about(request):
    return render(request, "about.html")
