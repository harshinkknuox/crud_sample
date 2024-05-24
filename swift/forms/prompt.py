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


class PromptOutputForm(forms.ModelForm):
    prompt = forms.ModelChoiceField(
        queryset=Prompt.objects.all(),
        label='Prompt',
        required=True,
        empty_label=None, 
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    text = forms.JSONField(
        label='Text',
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        error_messages={'required': 'The text should not be empty'}
    )

    class Meta:
        model = PromptOutput
        fields = ['prompt', 'text']

    def __init__(self, *args, **kwargs):
        super(PromptOutputForm, self).__init__(*args, **kwargs)
        # Add any additional customizations here if needed