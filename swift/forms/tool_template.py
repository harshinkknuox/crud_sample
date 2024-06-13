from django import forms
from django.contrib.auth import authenticate
from django.forms import inlineformset_factory
from django.core.validators import MaxLengthValidator, MinLengthValidator, MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from swift.models import  ToolInput,ToolType,ToolTemplateInput,ToolTemplate,ToolKeyword
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

def min_word_validator(value):
    min_words = 5  
    words = value.split()
    if len(words) < min_words:
        raise ValidationError(f"Minimum {min_words} words required.")

class DynamicToolTemplateInputForm(forms.Form):
    def __init__(self, *args, **kwargs):
        tool_template_inputs = kwargs.pop('tool_template_inputs', [])
        super(DynamicToolTemplateInputForm, self).__init__(*args, **kwargs)
        
        for tool_template_input in tool_template_inputs:
            tool_input = tool_template_input.tool_input
            input_attributes = tool_template_input.inputs
            
            input_validation_message = tool_template_input.validation_message
            input_sort_order = tool_template_input.sort_order
            
            field_type = tool_input.tool_type.type
            field_name = tool_input.name
            field_kwargs = {
                'label': field_name,
                'required': input_attributes.get('required', True),
            }
            max_length = input_attributes.get('max_length')
            min_length = input_attributes.get('min_length')
            placeholder = input_attributes.get('place_holder')
            max_validation_msg = input_attributes.get('max_validation_msg')
            min_validation_msg = input_attributes.get('min_validation_msg')
            validation_message = input_validation_message
            input_choice_attributes = tool_input.inputs
            
            if field_type == 'text':
                field = forms.CharField(widget=forms.TextInput(attrs={'placeholder': placeholder,'class':'form-control'}), **field_kwargs)        
                if input_attributes.get('required', True):
                    field.validators.append(MinLengthValidator(5, message=validation_message))        
            elif field_type == 'number':
                field = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': placeholder,'class':'form-control'}), **field_kwargs)
                if max_length:
                    field.validators.append(MaxValueValidator(10**(max_length-1), message=max_validation_msg))
                if min_length:
                    field.validators.append(MinValueValidator(10**(min_length-1), message=min_validation_msg))
            elif field_type == 'email':
                field = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': placeholder,'class':'form-control'}), **field_kwargs)
            elif field_type == 'textarea':
                field = forms.CharField(widget=forms.Textarea(attrs={'placeholder': placeholder,'class':'form-control'}), **field_kwargs)
                if min_length:
                    field.validators.append(MinLengthValidator(min_length, message=min_validation_msg))
                if max_length:
                    field.validators.append(MaxLengthValidator(max_length, message=max_validation_msg))
            elif field_type == 'select':
                field = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), choices=input_choice_attributes, **field_kwargs)
            else:
                continue
            
            self.fields[field_name] = field




# def save(self, commit=True):
#     instance = super().save(commit=False)
#     instance.inputs = {
#         'place_holder': self.cleaned_data['place_holder'],
#         'description': self.cleaned_data['description']
#     }
#     if commit:
#         instance.save()
#     return instance