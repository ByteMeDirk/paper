from django.contrib import admin
from multimedia.models import (
    ImagePost,
    VideoPost,
    AudioPost,
    MediaRating,
    MediaModeration,
)
from users.models import Profile

admin.site.register(ImagePost)
admin.site.register(VideoPost)
admin.site.register(AudioPost)
admin.site.register(MediaRating)
admin.site.register(MediaModeration)
admin.site.register(Profile)
