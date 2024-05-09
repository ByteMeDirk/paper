from django.core.paginator import Paginator

from multimedia.models import ImagePost, VideoPost, AudioPost


def get_media_pagination(request, page_limit:int, order_by:str = "-created_at", user_id:int = None):
    """
    This function returns the paginated media objects.

    Args:
        request (HttpRequest): The request object.
        page_limit (int): The number of media objects per page.
        order_by (str): The field to order the media objects by.

    Returns:
        image_page_obj (Paginator): The paginated image objects.
        video_page_obj (Paginator): The paginated video objects.
        audio_page_obj (Paginator): The paginated audio objects.
    """
    # Get all media static
    if user_id:
        image_media = ImagePost.objects.filter(author__id=user_id).order_by(order_by)
        video_media = VideoPost.objects.filter(author__id=user_id).order_by(order_by)
        audio_media = AudioPost.objects.filter(author__id=user_id).order_by(order_by)
    else:
        image_media = ImagePost.objects.all().order_by(order_by)
        video_media = VideoPost.objects.all().order_by(order_by)
        audio_media = AudioPost.objects.all().order_by(order_by)

    # Define Media Pagination
    image_paginator = Paginator(image_media, page_limit)
    video_paginator = Paginator(video_media, page_limit)
    audio_paginator = Paginator(audio_media, page_limit)

    # Get the page
    image_page_obj = image_paginator.get_page(request.GET.get("image_page"))
    video_page_obj = video_paginator.get_page(request.GET.get("video_page"))
    audio_page_obj = audio_paginator.get_page(request.GET.get("audio_page"))

    return image_page_obj, video_page_obj, audio_page_obj