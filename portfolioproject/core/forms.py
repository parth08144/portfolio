from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'github_link']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter project title',
                'class': 'form-input'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter project description',
                'class': 'form-input'
            }),
            'github_link': forms.URLInput(attrs={
                'placeholder': 'Enter GitHub link',
                'class': 'form-input'
            }),
        }
