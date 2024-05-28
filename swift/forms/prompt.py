from django import forms
from django.contrib.auth import authenticate
from swift.models import Prompt,PromptOutput

class PromptForm(forms.ModelForm):
    name = forms.CharField(
        label='Prompt Name',max_length=150,required=True,
        widget=forms.TextInput(attrs={'autocomplete':'off'}),
        error_messages={ 'required': 'The name should not be empty' }
    )

    class Meta:
        model = Prompt
        fields = ['name']


class PromptOutForm(forms.ModelForm):
    name = forms.CharField(
        label='Name',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
    description = forms.CharField(
        label='Description',
        required=True,
        widget=forms.Textarea(attrs={'rows': 4})
    )

    class Meta:
        model = PromptOutput
        fields = ['prompt', 'name', 'description']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.text = {
            'name': self.cleaned_data['name'],
            'description': self.cleaned_data['description']
        }
        if commit:
            instance.save()
        return instance