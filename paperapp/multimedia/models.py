from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from taggit.managers import TaggableManager


class ImagePost(models.Model):
    """
    Model for an image post.
    """

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    file = models.ImageField(upload_to="images/")
    content_rating = models.CharField(max_length=10, default="General")
    tags = TaggableManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    metadata = models.JSONField(null=True, blank=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} by {self.author.username}"

    def get_vote_count(self):
        return (
            MediaRating.objects.filter(image_id=self.id).aggregate(Sum("vote"))[
                "vote__sum"
            ]
            or 0
        )


class VideoPost(models.Model):
    """
    Model for a video post.
    """

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True)
    file = models.FileField(upload_to="videos/")
    content_rating = models.CharField(max_length=10, default="General")
    tags = TaggableManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    metadata = models.JSONField(null=True, blank=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} by {self.author.username}"

    def get_vote_count(self):
        return (
            MediaRating.objects.filter(image_id=self.id).aggregate(Sum("vote"))[
                "vote__sum"
            ]
            or 0
        )


class AudioPost(models.Model):
    """
    Model for an audio post.
    """

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    thumbnail = models.ImageField(upload_to="thumbnails/")
    file = models.FileField(upload_to="audio/")
    content_rating = models.CharField(max_length=10, default="General")
    tags = TaggableManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    metadata = models.JSONField(null=True, blank=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} by {self.author.username}"

    def get_vote_count(self):
        return (
            MediaRating.objects.filter(image_id=self.id).aggregate(Sum("vote"))[
                "vote__sum"
            ]
            or 0
        )


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

    vote = models.IntegerField(default=0)  # 1 for up_vote, -1 for down_vote

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} rated {self.vote} for {self.image_id or self.video_id or self.audio_id}"

    class Meta:
        unique_together = ("user", "image_id", "video_id", "audio_id")
        verbose_name = "Media Rating"
        verbose_name_plural = "Media Ratings"

    @staticmethod
    def get_total_votes(media_id, media_type):
        # Get all votes for the specified media
        if media_type == "image":
            votes = MediaRating.objects.filter(image_id=media_id)
        elif media_type == "video":
            votes = MediaRating.objects.filter(video_id=media_id)
        else:  # audio
            votes = MediaRating.objects.filter(audio_id=media_id)

        # Calculate the total votes as the sum of the vote values
        total_votes = votes.aggregate(total_votes=Sum("vote"))["total_votes"]

        return total_votes


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

    message = models.TextField(max_length=500, null=True, blank=True)

    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} moderated {self.image_id or self.video_id or self.audio_id}"

    class Meta:
        unique_together = ("user", "image_id", "video_id", "audio_id")
        verbose_name = "Media Moderation"
        verbose_name_plural = "Media Moderations"
