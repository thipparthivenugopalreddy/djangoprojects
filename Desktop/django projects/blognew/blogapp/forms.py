from django import forms
from blogapp.models import post

class postform(forms.ModelForm):
    class Meta:
        model=post
        fields="__all__"
