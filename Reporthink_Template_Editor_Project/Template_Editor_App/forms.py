from django import forms
from .models import Template, TemplatePart

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
