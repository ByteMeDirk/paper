from django.contrib import messages
from django.db.models import Count
from django.shortcuts import render

from multimedia.forms import SearchMediaForm
from multimedia.models import ImagePost, VideoPost, AudioPost


def home(request):
    """
    Home page allows for content search. Once search is run, media content is displayed.
    Otherwise, the user is presented with the most recently posted media content.
    """

    # Get all available tags form the taggit table
    tags = ImagePost.tags.all()
    tags = tags.union(VideoPost.tags.all())
    tags = tags.union(AudioPost.tags.all())

    def filter_closure(media_object, tags, sort, content_rating=None):
        """
        Filter media content by tags, content rating and sort by date or popularity.
        """
        print(f"Filtering {media_object} by tags: {tags}, content rating: {content_rating} and sort: {sort}")
        if tags:
            media = media_object.objects.filter(tags__name__in=tags).distinct()
        else:
            media = media_object.objects.all()

        if content_rating:
            media = media.filter(content_rating=content_rating)

        if sort == "hot":
            media = media.annotate(
                num_votes=Count("mediarating__up_vote") - Count("mediarating__down_vote")
            ).order_by("-num_votes")
        elif sort == "popular":
            media = media.annotate(num_votes=Count("mediarating__up_vote")).order_by(
                "-num_votes"
            )
        else:
            media = media.order_by("-created_at")

        return media

    if request.method == "POST":
        form = SearchMediaForm(request.POST)
        if form.is_valid():
            search_by_tags = form.cleaned_data["search_by_tags"]
            sort_by = form.cleaned_data["sort_by"]
            content_rating = form.cleaned_data["content_rating"]

            video_media = filter_closure(VideoPost, search_by_tags, sort_by, content_rating)
            audio_media = filter_closure(AudioPost, search_by_tags, sort_by, content_rating)
            image_media = filter_closure(ImagePost, search_by_tags, sort_by, content_rating)

            messages.success(request, "Search results displayed.")
            return render(
                request,
                "home.html",
                {
                    "form": form,
                    "video_media": video_media,
                    "audio_media": audio_media,
                    "image_media": image_media,
                    "tags": tags,
                },
            )

    else:
        form = SearchMediaForm()

        video_media = filter_closure(VideoPost, None, "date")
        audio_media = filter_closure(AudioPost, None, "date")
        image_media = filter_closure(ImagePost, None, "date")

        return render(
            request,
            "home.html",
            {
                "form": form,
                "video_media": video_media,
                "audio_media": audio_media,
                "image_media": image_media,
                "tags": tags,
            },
        )


def wiki(request):
    return render(request, "wiki.html")


def about(request):
    return render(request, "about.html")
