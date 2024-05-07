from django import forms
from taggit.forms import TagField, TagWidget

from .models import ImagePost, VideoPost, AudioPost


class ImagePostForm(forms.ModelForm):
    class Meta:
        model = ImagePost
        fields = ["title", "description", "file", "tags"]

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

    tags = TagField(
        widget=TagWidget(
            attrs={
                "class": "form-control",
                "placeholder": "Tags",
            }
        )
    )

    help_text = {
        "title": "The title of the image post.",
        "description": "A description of the image post.",
        "image": "The image file to be uploaded.",
        "tags": "Tags to categorize the image post.",
    }


class VideoPostForm(forms.ModelForm):
    class Meta:
        model = VideoPost
        fields = ["title", "description", "file", "tags"]

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
        fields = ["title", "description", "file", "tags"]

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
                "placeholder": "Audio",
            }
        )
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
        )
    )

    # Sort by most popular, most recent, or standard
    sort_by = forms.ChoiceField(
        choices=[("popular", "Popular"), ("recent", "Recent"), ("standard", "Hot")],
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ),
    )
