from django import forms
from django.contrib.auth import authenticate
from swift.models import Course

class CourseForm(forms.ModelForm):
    name = forms.CharField( 
        label="Title", max_length=200, required = True,
        widget=forms.TextInput(attrs={'autocomplete':'off'}),
        error_messages={ 'required': 'The name should not be empty' }
    )
    curriculum = forms.CharField(
        label="Curriculum Name", required = True,
        widget=forms.Select(attrs={'autocomplete':'off'}),
        error_messages={ 'required': 'The carriculum should not be empty' }
    )
    
    class Meta:
        model = Course
        fields = ['name','curriculum']