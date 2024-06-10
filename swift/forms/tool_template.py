from django import forms
from django.contrib.auth import authenticate
from swift.models import  ToolInput,ToolType,ToolTemplateInput,ToolTemplate,ToolKeyword
from django.forms import inlineformset_factory

class ToolTemplateForm(forms.ModelForm):
    class Meta:
        model = ToolTemplate
        fields = ['tool_type','tool_name','tool_context','youtube_link']
        widgets = {
            'tool_type': forms.Select(attrs={'class': 'form-control','required':'True'}),
            'tool_name': forms.TextInput(attrs={'class': 'form-control','required':'True'}),
            'tool_context': forms.Textarea(attrs={'class': 'form-control','required':'True'}),
            'youtube_link': forms.URLInput(attrs={'class': 'form-control','required':'True'}),
        }

class ToolInputForm(forms.Form):
    place_holder =forms.CharField(
            label='Place Holder',
            max_length=150,
            required=True,
            widget=forms.TextInput(attrs={'autocomplete': 'off'})
        )
    
    description =forms.CharField(
            label='description',
            max_length=150,
            required=True,
            widget=forms.TextInput(attrs={'autocomplete': 'off'})
        )

    max_length =forms.IntegerField(
            label='Max Length',required=False,
            widget=forms.NumberInput(attrs={'autocomplete': 'off'})
        )

    max_validation_msg =forms.CharField(
            label='Max Validation Message',required=False,
            max_length=150,
            widget=forms.TextInput(attrs={'autocomplete': 'off'})
        )
    
    min_length =forms.IntegerField(
            label='Min Length',required=False,
            widget=forms.NumberInput(attrs={'autocomplete': 'off'})
        )
    min_validation_msg =forms.CharField(
            label='Min Validation Message',required=False,
            max_length=150,
            widget=forms.TextInput(attrs={'autocomplete': 'off'})
        )

class ToolTemplateInputForm(forms.ModelForm):
    place_holder =forms.CharField(
            label='Place Holder',
            max_length=150,
            required=True,
            widget=forms.TextInput(attrs={'autocomplete': 'off'})
        )
    
    description =forms.CharField(
            label='description',
            max_length=150,
            required=True,
            widget=forms.TextInput(attrs={'autocomplete': 'off'})
        )

    max_length =forms.IntegerField(
            label='Max Length',required=False,
            widget=forms.NumberInput(attrs={'autocomplete': 'off'})
        )

    max_validation_msg =forms.CharField(
            label='Max Validation Message',required=False,
            max_length=150,
            widget=forms.TextInput(attrs={'autocomplete': 'off'})
        )
    
    min_length =forms.IntegerField(
            label='Min Length',required=False,
            widget=forms.NumberInput(attrs={'autocomplete': 'off'})
        )
    min_validation_msg =forms.CharField(
            label='Min Validation Message',required=False,
            max_length=150,
            widget=forms.TextInput(attrs={'autocomplete': 'off'})
        )
    class Meta:
        model = ToolTemplateInput
        fields = ['tool_input','validation_message','sort_order']
        widgets = {
            'tool_input': forms.Select(attrs={'class': 'form-control tool-select','required':'True'}),
            'validation_message': forms.TextInput(attrs={'class': 'form-control','required':'True'}),
            'sort_order': forms.TextInput(attrs={'class': 'form-control','required':'True'}),
        }


ToolInputFormFormSet = inlineformset_factory(
    ToolTemplate,
    ToolTemplateInput,
    form=ToolTemplateInputForm,
    extra=2,
    can_delete=True,
)


    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     instance.inputs = {
    #         'place_holder': self.cleaned_data['place_holder'],
    #         'description': self.cleaned_data['description']
    #     }
    #     if commit:
    #         instance.save()
    #     return instance