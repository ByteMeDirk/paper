import unittest
from datetime import date

from django.contrib.auth.models import User

from users.models import Profile
from .models import ImagePost, VideoPost, AudioPost, MediaRating


class TestImagePost(unittest.TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            "testuser", "testuser@example.com", "testpassword"
        )

        # Update Profile
        self.profile = Profile.objects.get(user=self.user)
        self.profile.bio = "This is a test bio"
        self.profile.location = "Test Location"
        self.profile.birth_date = date(1990, 1, 1)
        self.profile.avatar = "avatars/default.png"

        self.image_post = ImagePost(
            title="Test Image Post",
            description="This is a test image post",
            author=self.user,
            file="avatars/default.png",
        )

    def tearDown(self):
        try:
            self.profile.delete()
            self.user.delete()
            self.image_post.delete()
        except ValueError:
            pass

    def test_image_post_fields(self):
        self.assertEqual(self.image_post.title, "Test Image Post")
        self.assertEqual(self.image_post.description, "This is a test image post")
        self.assertEqual(self.image_post.author, self.user)
        self.assertEqual(self.image_post.file.name, "avatars/default.png")

    def test_image_post_get_vote_count(self):
        media_rating = MediaRating(user=self.user, image_id=self.image_post.id, vote=1)
        media_rating.save()
        self.assertGreater(self.image_post.get_vote_count(), 0)

    def test_image_post_str(self):
        self.assertEqual(str(self.image_post), "Test Image Post by testuser")


class TestVideoPost(unittest.TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "testuser", "testuser@example.com", "testpassword"
        )

        # Update Profile
        self.profile = Profile.objects.get(user=self.user)
        self.profile.bio = "This is a test bio"
        self.profile.location = "Test Location"
        self.profile.birth_date = date(1990, 1, 1)
        self.profile.avatar = "avatars/default.png"

        self.video_post = VideoPost(
            title="Test Video Post",
            description="This is a test video post",
            author=self.user,
            thumbnail="avatars/default.png",
            file="test_video.mp4",
        )

    def tearDown(self):
        try:
            self.profile.delete()
            self.user.delete()
            self.video_post.delete()
        except ValueError:
            pass

    def test_video_post_fields(self):
        self.assertEqual(self.video_post.title, "Test Video Post")
        self.assertEqual(self.video_post.description, "This is a test video post")
        self.assertEqual(self.video_post.author, self.user)
        self.assertEqual(self.video_post.thumbnail.name, "avatars/default.png")
        self.assertEqual(self.video_post.file.name, "test_video.mp4")

    def test_video_post_get_vote_count(self):
        self.assertEqual(self.video_post.title, "Test Video Post")
        self.assertEqual(self.video_post.description, "This is a test video post")
        self.assertEqual(self.video_post.author, self.user)
        self.assertEqual(self.video_post.file.name, "test_video.mp4")

    def test_video_post_str(self):
        self.assertEqual(str(self.video_post), "Test Video Post by testuser")


class TestAudioPost(unittest.TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "testuser", "testuser@example.com", "testpassword"
        )

        # Update Profile
        self.profile = Profile.objects.get(user=self.user)
        self.profile.bio = "This is a test bio"
        self.profile.location = "Test Location"
        self.profile.birth_date = date(1990, 1, 1)
        self.profile.avatar = "avatars/default.png"

        self.video_post = VideoPost(
            title="Test Video Post",
            description="This is a test video post",
            author=self.user,
            thumbnail="avatars/default.png",
            file="test_video.mp4",
        )

        self.audio_post = AudioPost(
            title="Test Audio Post",
            description="This is a test audio post",
            author=self.user,
            thumbnail="avatars/default.png",
            file="test_audio.mp3",
        )

    def tearDown(self):
        try:
            self.profile.delete()
            self.user.delete()
            self.audio_post.delete()
        except ValueError:
            pass

    def test_audio_post_fields(self):
        self.assertEqual(self.audio_post.title, "Test Audio Post")
        self.assertEqual(self.audio_post.description, "This is a test audio post")
        self.assertEqual(self.audio_post.author, self.user)
        self.assertEqual(self.audio_post.thumbnail.name, "avatars/default.png")
        self.assertEqual(self.audio_post.file.name, "test_audio.mp3")

    def test_audio_post_get_vote_count(self):
        self.assertEqual(self.audio_post.title, "Test Audio Post")
        self.assertEqual(self.audio_post.description, "This is a test audio post")
        self.assertEqual(self.audio_post.author, self.user)
        self.assertEqual(self.audio_post.file.name, "test_audio.mp3")

    def test_audio_post_str(self):
        self.assertEqual(str(self.audio_post), "Test Audio Post by testuser")


class TestMediaRating(unittest.TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "testuser", "testuser@example.com", "testpassword"
        )

        # Update Profile
        self.profile = Profile.objects.get(user=self.user)
        self.profile.bio = "This is a test bio"
        self.profile.location = "Test Location"
        self.profile.birth_date = date(1990, 1, 1)
        self.profile.avatar = "avatars/default.png"

        self.video_post = VideoPost(
            title="Test Video Post",
            description="This is a test video post",
            author=self.user,
            thumbnail="avatars/default.png",
            file="test_video.mp4",
        )
        self.image_post = ImagePost(
            title="Test Image Post",
            description="This is a test image post",
            author=self.user,
            file="avatars/default.png",
        )
        self.media_rating = MediaRating(
            user=self.user, image_id=self.image_post.id, vote=1
        )

    def tearDown(self):
        try:
            self.profile.delete()
            self.user.delete()
            self.image_post.delete()
            self.media_rating.delete()
        except ValueError:
            pass

    def test_media_rating_fields(self):
        self.assertEqual(self.media_rating.user, self.user)
        self.assertEqual(self.media_rating.image_id, self.image_post.id)
        self.assertEqual(self.media_rating.vote, 1)

    def test_media_rating_str(self):
        self.assertEqual(str(self.media_rating), "testuser rated 1 for None")


# ToDo: After Moderation Feature is implemented
# class TestMediaModeration(unittest.TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             "testuser", "testuser@example.com", "testpassword"
#         )
#
#         # Update Profile
#         self.profile = Profile.objects.get(user=self.user)
#         self.profile.bio = "This is a test bio"
#         self.profile.location = "Test Location"
#         self.profile.birth_date = date(1990, 1, 1)
#         self.profile.avatar = "avatars/default.png"
#
#         self.image_post = ImagePost(title='Test Image Post', description='This is a test image post', author=self.user,
#                                     file='avatars/default.png')
#         self.media_moderation = MediaModeration(user=self.user, image_id=self.image_post.id, approved=True)
#
#
#     def tearDown(self):
#         try:
#             self.profile.delete()
#             self.user.delete()
#             self.image_post.delete()
#             self.media_moderation.delete()
#         except ValueError:
#             pass
#
#     def test_media_moderation_fields(self):
#         self.assertEqual(self.media_moderation.user, self.user)
#         self.assertEqual(self.media_moderation.image_id, self.image_post.id)
#         self.assertEqual(self.media_moderation.approved, True)
#
#     def test_media_moderation_str(self):
#         self.assertEqual(str(self.media_moderation), 'testuser moderated Test Image Post')
