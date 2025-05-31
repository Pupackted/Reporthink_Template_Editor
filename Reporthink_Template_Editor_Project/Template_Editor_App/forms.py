from django import forms
from .models import Template, TemplatePart
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class TemplateForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ['name']  # Only ask for name initially
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter template name'}),
        }
class TemplatePartForm(forms.ModelForm):
    class Meta:
        model = TemplatePart
        fields = ['html_file', 'thumbnail']


# authentication forms

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')