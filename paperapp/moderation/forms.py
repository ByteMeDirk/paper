from django import forms
from .models import ReportUser, ReportPost



class ReportUserForm(forms.ModelForm):
    """
    Form for reporting a user.
    """
    class Meta:
        model = ReportUser
        fields = ['reason']
        labels = {
            'reason': 'Reason for report'
        }

    reason = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Reason for report',
            }
        )
    )


class ReportPostForm(forms.ModelForm):
    """
    Form for reporting a post.
    """
    class Meta:
        model = ReportPost
        fields = ['reason']
        labels = {
            'reason': 'Reason for report'
        }

    reason = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Reason for report',
            }
        )
    )
