from django import forms
from lms.models import Profile

# Create the form class.
class ProfileForm(forms.ModelForm):
    name = forms.CharField(max_length=32)
    class Meta:
        model = Profile
        fields = ['photo','phone']