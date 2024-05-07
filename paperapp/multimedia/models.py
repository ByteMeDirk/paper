from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager


class ImagePost(models.Model):
    """
    Model for an image post.
    """

    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    thumbnail = models.ImageField(upload_to="thumbnails/")
    file = models.ImageField(upload_to="images/")
    content_rating = models.CharField(max_length=10, default="General")
    tags = TaggableManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    metadata = models.JSONField(null=True, blank=True)


class VideoPost(models.Model):
    """
    Model for a video post.
    """

    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    thumbnail = models.ImageField(upload_to="thumbnails/")
    file = models.FileField(upload_to="videos/")
    content_rating = models.CharField(max_length=10, default="General")
    tags = TaggableManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    metadata = models.JSONField(null=True, blank=True)


class AudioPost(models.Model):
    """
    Model for an audio post.
    """

    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    thumbnail = models.ImageField(upload_to="thumbnails/")
    file = models.FileField(upload_to="audio/")
    content_rating = models.CharField(max_length=10, default="General")
    tags = TaggableManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MediaRating(models.Model):
    """
    This represents the up_vote, down_vote and rating of the media.
    This is for images, videos and audio, and the frequency of the rating
    to aid in the recommendation system.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User can only vote once

    image_id = models.ForeignKey(
        ImagePost, on_delete=models.CASCADE, null=True, blank=True
    )
    video_id = models.ForeignKey(
        VideoPost, on_delete=models.CASCADE, null=True, blank=True
    )
    audio_id = models.ForeignKey(
        AudioPost, on_delete=models.CASCADE, null=True, blank=True
    )

    up_vote = models.BooleanField(default=False)
    down_vote = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "image_id", "video_id", "audio_id")
        verbose_name = "Media Rating"
        verbose_name_plural = "Media Ratings"


class MediaModeration(models.Model):
    """
    This represents the moderation of the media.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # User can only moderate once

    image_id = models.ForeignKey(
        ImagePost, on_delete=models.CASCADE, null=True, blank=True
    )
    video_id = models.ForeignKey(
        VideoPost, on_delete=models.CASCADE, null=True, blank=True
    )
    audio_id = models.ForeignKey(
        AudioPost, on_delete=models.CASCADE, null=True, blank=True
    )

    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "image_id", "video_id", "audio_id")
        verbose_name = "Media Moderation"
        verbose_name_plural = "Media Moderations"