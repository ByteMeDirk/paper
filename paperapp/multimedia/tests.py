import unittest
from datetime import date

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import connection
from django.test import TestCase, Client
from django.urls import reverse

from multimedia.models import ImagePost, VideoPost, AudioPost
from users.models import Profile
from .models import MediaRating


class SelectPostTypeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        try:
            self.user = User.objects.get(username="testuser")
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                "testuser", "testuser@example.com", "testpassword"
            )

        # Get or create Profile
        self.profile, created = Profile.objects.get_or_create(user=self.user)
        self.client.login(username="testuser", password="testpassword")
        self.select_post_type_url = reverse("select_post_type")

    def tearDown(self):
        self.profile.delete()
        self.user.delete()

    def test_select_post_type_view(self):
        response = self.client.get(self.select_post_type_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "multimedia/select_post_type.html")


class CreatePostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        try:
            self.user = User.objects.get(username="testuser")
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                "testuser", "testuser@example.com", "testpassword"
            )

        # Get or create Profile
        self.profile, created = Profile.objects.get_or_create(user=self.user)
        self.create_post_url = reverse("create_post", args=["image"])

        self.image_file = SimpleUploadedFile(
            name="test_image.jpg",
            content=open("media/avatars/default.png", "rb").read(),
            content_type="image/jpeg",
        )

    def tearDown(self):
        self.profile.delete()
        self.user.delete()
        self.image_file.close()

    def test_create_post_view(self):
        response = self.client.post(
            self.create_post_url,
            {
                "file": self.image_file,
                "title": "Test Image",
                "description": "Test Description",
                "tags": "test, image",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")


class EditPostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        try:
            self.user = User.objects.get(username="testuser")
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                "testuser", "testuser@example.com", "testpassword"
            )

        # Get or create Profile
        self.profile, created = Profile.objects.get_or_create(user=self.user)
        self.client.login(username="testuser", password="testpassword")

        self.image_file = SimpleUploadedFile(
            name="avatars/default.png",
            content=open("media/avatars/default.png", "rb").read(),
            content_type="image/jpeg",
        )

        self.post = ImagePost.objects.create(
            author=self.user,
            title="Test Image",
            description="Test Description",
            file=self.image_file,
            tags="test, image",
        )

        self.edit_post_url = reverse("edit_post", args=["image", self.post.id])

    def tearDown(self):
        self.profile.delete()
        self.user.delete()
        self.post.delete()

    def test_edit_post_view(self):
        response = self.client.get(self.edit_post_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "multimedia/edit_post.html")


class DeletePostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        try:
            self.user = User.objects.get(username="testuser")
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                "testuser", "testuser@example.com", "testpassword"
            )

        # Get or create Profile
        self.profile, created = Profile.objects.get_or_create(user=self.user)
        self.client.login(username="testuser", password="testpassword")

        self.image_file = SimpleUploadedFile(
            name="avatars/default.png",
            content=open("media/avatars/default.png", "rb").read(),
            content_type="image/jpeg",
        )

        self.post = ImagePost.objects.create(
            author=self.user,
            title="Test Image",
            description="Test Description",
            file=self.image_file,
            tags="test, image",
        )

        self.delete_post_url = reverse("delete_post", args=["image", self.post.id])

    def tearDown(self):
        self.profile.delete()
        self.user.delete()

    def test_delete_post_view(self):
        response = self.client.post(self.delete_post_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        with self.assertRaises(ImagePost.DoesNotExist):
            ImagePost.objects.get(pk=self.post.id)


class ViewPostTest(TestCase):
    def setUp(self):
        self.client = Client()
        try:
            self.user = User.objects.get(username="testuser")
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                "testuser", "testuser@example.com", "testpassword"
            )

        # Get or create Profile
        self.profile, created = Profile.objects.get_or_create(user=self.user)
        self.client.login(username="testuser", password="testpassword")

        self.image_file = SimpleUploadedFile(
            name="avatars/default.png",
            content=open("media/avatars/default.png", "rb").read(),
            content_type="image/jpeg",
        )

        self.post = ImagePost.objects.create(
            author=self.user,
            title="Test Image",
            description="Test Description",
            file=self.image_file,
            tags="test, image",
        )

        self.view_post_url = reverse("view_post", args=["image", self.post.id])

    def tearDown(self):
        self.profile.delete()
        self.user.delete()
        self.post.delete()

    def test_view_post(self):
        initial_views = self.post.views
        response = self.client.get(self.view_post_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "multimedia/view_post.html")
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, initial_views + 1)


class SearchViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        try:
            self.user = User.objects.get(username="testuser")
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                "testuser", "testuser@example.com", "testpassword"
            )

        # Get or create Profile
        self.profile, created = Profile.objects.get_or_create(user=self.user)
        self.client.login(username="testuser", password="testpassword")

        self.image_file = SimpleUploadedFile(
            name="avatars/default.png",
            content=open("media/avatars/default.png", "rb").read(),
            content_type="image/jpeg",
        )

        self.post = ImagePost.objects.create(
            author=self.user,
            title="Test Image",
            description="Test Description",
            file=self.image_file,
            tags="test, image",
        )

        with connection.cursor() as cursor:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")

        self.search_url = reverse("search") + "?q=test"

    def tearDown(self):
        self.profile.delete()
        self.user.delete()
        self.post.delete()

    def test_search_view(self):
        response = self.client.get(self.search_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "multimedia/search_results.html")


class VoteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        try:
            self.user = User.objects.get(username="testuser")
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                "testuser", "testuser@example.com", "testpassword"
            )

        # Get or create Profile
        self.profile, created = Profile.objects.get_or_create(user=self.user)
        self.client.login(username="testuser", password="testpassword")

        self.image_file = SimpleUploadedFile(
            name="avatars/default.png",
            content=open("media/avatars/default.png", "rb").read(),
            content_type="image/jpeg",
        )

        self.post = ImagePost.objects.create(
            author=self.user,
            title="Test Image",
            description="Test Description",
            file=self.image_file,
            tags="test, image",
        )

        self.vote_url = reverse("vote", args=[self.post.id, "image", "up"])

    def tearDown(self):
        self.profile.delete()
        self.user.delete()
        self.post.delete()

    def test_vote_view(self):
        initial_votes = MediaRating.get_total_votes(self.post.id, "image")
        response = self.client.post(self.vote_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(
            MediaRating.get_total_votes(self.post.id, "image"), initial_votes + 1
        )


class ViewGalleryTest(TestCase):
    def setUp(self):
        self.client = Client()
        try:
            self.user = User.objects.get(username="testuser")
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                "testuser", "testuser@example.com", "testpassword"
            )

        # Get or create Profile
        self.profile, created = Profile.objects.get_or_create(user=self.user)
        self.client.login(username="testuser", password="testpassword")

        self.image_file = SimpleUploadedFile(
            name="avatars/default.png",
            content=open("media/avatars/default.png", "rb").read(),
            content_type="image/jpeg",
        )

        self.post = ImagePost.objects.create(
            author=self.user,
            title="Test Image",
            description="Test Description",
            file=self.image_file,
            tags="test, image",
        )

        self.view_gallery_url = reverse("view_gallery", args=["image"])

    def tearDown(self):
        self.profile.delete()
        self.user.delete()
        self.post.delete()

    def test_view_gallery(self):
        response = self.client.get(self.view_gallery_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "multimedia/view_gallery.html")


class TestImagePost(unittest.TestCase):

    def setUp(self):
        try:
            self.user = User.objects.get(username="testuser")
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                "testuser", "testuser@example.com", "testpassword"
            )

        # Get or create Profile
        self.profile, created = Profile.objects.get_or_create(user=self.user)

        # Update Profile
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
        try:
            self.user = User.objects.get(username="testuser")
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                "testuser", "testuser@example.com", "testpassword"
            )

        # Get or create Profile
        self.profile, created = Profile.objects.get_or_create(user=self.user)

        # Update Profile
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
        try:
            self.user = User.objects.get(username="testuser")
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                "testuser", "testuser@example.com", "testpassword"
            )

        # Get or create Profile
        self.profile, created = Profile.objects.get_or_create(user=self.user)

        # Update Profile
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
        try:
            self.user = User.objects.get(username="testuser")
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                "testuser", "testuser@example.com", "testpassword"
            )

        # Get or create Profile
        self.profile, created = Profile.objects.get_or_create(user=self.user)

        # Update Profile
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
