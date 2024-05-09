import unittest
from datetime import date

from PIL import Image
from django.contrib.auth.models import User

from users.models import Profile


class TestProfile(unittest.TestCase):
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

    def tearDown(self):
        try:
            self.profile.delete()
            self.user.delete()
        except ValueError:
            pass

    def test_profile_fields(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.bio, "This is a test bio")
        self.assertEqual(self.profile.location, "Test Location")
        self.assertEqual(self.profile.birth_date, date(1990, 1, 1))
        self.assertEqual(self.profile.avatar.name, "avatars/default.png")

    def test_profile_age(self):
        self.assertEqual(self.profile.age(), 34)

    def test_profile_save(self):
        self.profile.save()
        image = Image.open(self.profile.avatar.path)
        width, height = image.size
        self.assertEqual(width, height)
