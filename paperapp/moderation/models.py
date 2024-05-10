from django.contrib.auth.models import User
from django.db import models
from multimedia.models import ImagePost, VideoPost, AudioPost


class ReportUser(models.Model):
    """
    Model for a user report.
    """

    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reporter")
    reported = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reported")
    reason = models.TextField(max_length=500)
    resolved = models.BooleanField(default=False)
    resolved_message = models.TextField(max_length=500, null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="user_resolved_by")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reporter.username} reported {self.reported.username}"


class ReportPost(models.Model):
    """
    Model for a post report.
    """
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(ImagePost, on_delete=models.CASCADE, null=True, blank=True)
    video = models.ForeignKey(VideoPost, on_delete=models.CASCADE, null=True, blank=True)
    audio = models.ForeignKey(AudioPost, on_delete=models.CASCADE, null=True, blank=True)
    reason = models.TextField(max_length=500)
    resolved = models.BooleanField(default=False)
    resolved_message = models.TextField(max_length=500, null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="post_resolved_by")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reporter.username} reported {self.image or self.video or self.audio}"

