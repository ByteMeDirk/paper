from django import forms
from taggit.forms import TagField, TagWidget

from .models import ImagePost, VideoPost, AudioPost, MediaRating


class ImagePostForm(forms.ModelForm):
    class Meta:
        model = ImagePost
        fields = ["title", "description", "file", "content_rating", "tags"]

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Title",
            }
        )
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Description",
            }
        )
    )

    file = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "placeholder": "Image",
            }
        )
    )

    content_rating = forms.ChoiceField(
        choices=[
            ("General", "General"),
            ("Mature", "Mature"),
            ("Explicit", "Explicit"),
        ],
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )

    tags = TagField(
        widget=TagWidget(
            attrs={
                "class": "form-control",
                "placeholder": "Tags",
            }
        )
    )


class VideoPostForm(forms.ModelForm):
    class Meta:
        model = VideoPost
        fields = ["title", "description", "file", "content_rating", "tags"]

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Title",
            }
        )
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Description",
            }
        )
    )

    file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "placeholder": "Video",
            }
        )
    )

    content_rating = forms.ChoiceField(
        choices=[
            ("General", "General"),
            ("Mature", "Mature"),
            ("Explicit", "Explicit"),
        ],
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )

    tags = TagField(
        widget=TagWidget(
            attrs={
                "class": "form-control",
                "placeholder": "Tags",
            }
        )
    )


class AudioPostForm(forms.ModelForm):
    class Meta:
        model = AudioPost
        fields = ["title", "description", "thumbnail", "file", "content_rating", "tags"]

    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Title",
            }
        )
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Description",
            }
        )
    )

    thumbnail = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "placeholder": "Thumbnail",
            }
        )
    )

    file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "placeholder": "Audio",
            }
        )
    )

    content_rating = forms.ChoiceField(
        choices=[
            ("General", "General"),
            ("Mature", "Mature"),
            ("Explicit", "Explicit"),
        ],
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )

    tags = TagField(
        widget=TagWidget(
            attrs={
                "class": "form-control",
                "placeholder": "Tags",
            }
        )
    )


class SearchMediaForm(forms.Form):
    search_by_tags = TagField(
        widget=TagWidget(
            attrs={
                "class": "form-control",
                "placeholder": "Search by tags",
            }
        ),
        required=False,
    )

    # Sort by most popular, most recent, or standard
    sort_by = forms.ChoiceField(
        choices=[("recent", "Recent"), ("popular", "Popular"), ("hot", "Hot")],
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
        required=False,
    )

    # Filter by content rating
    content_rating = forms.ChoiceField(
        choices=[
            ("General", "General"),
            ("Mature", "Mature"),
            ("Explicit", "Explicit"),
        ],
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
        required=False,
    )
