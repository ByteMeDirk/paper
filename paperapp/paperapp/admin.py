from django.contrib import admin
from users.models import Profile
from multimedia.models import (
    ImagePost,
    VideoPost,
    AudioPost,
    MediaRating,
)
from moderation.models import ReportUser, ReportPost
admin.site.register(Profile)
admin.site.register(ImagePost)
admin.site.register(VideoPost)
admin.site.register(AudioPost)
admin.site.register(MediaRating)
admin.site.register(ReportUser)
admin.site.register(ReportPost)


