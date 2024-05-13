from django import forms

from .models import ReportUser, ReportPost


class ReportUserForm(forms.ModelForm):
    """
    Form for reporting a user.
    """

    class Meta:
        model = ReportUser
        fields = ["reason"]
        labels = {"reason": "Reason for report"}

    reason = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Reason for report",
            }
        )
    )


class ReportPostForm(forms.ModelForm):
    """
    Form for reporting a post.
    """

    class Meta:
        model = ReportPost
        fields = ["reason"]
        labels = {"reason": "Reason for report"}

    reason = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Reason for report",
            }
        )
    )


class ModerateUserForm(forms.ModelForm):
    """
    Form for moderating a user.
    """

    class Meta:
        model = ReportUser
        fields = ["resolved", "resolved_message"]
        labels = {"resolved": "Resolved", "resolved_message": "Message to user"}

    resolved = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
            }
        )
    )

    resolved_message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Message to user",
            }
        )
    )


class ModeratePostForm(forms.ModelForm):
    """
    Form for moderating a post.
    """

    class Meta:
        model = ReportPost
        fields = ["resolved", "resolved_message"]
        labels = {"resolved": "Resolved", "resolved_message": "Message to user"}

    resolved = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
            }
        )
    )

    resolved_message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Message to user",
            }
        )
    )
