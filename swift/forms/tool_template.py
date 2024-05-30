from django import forms
from django.contrib.auth import authenticate
from swift.models import  ToolInput,ToolType,ToolTemplateInput,ToolTemplate,ToolKeyword
from django.forms import inlineformset_factory

class ToolTemplateForm(forms.ModelForm):
    tool_type = forms.ModelChoiceField(
        queryset=ToolType.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
        label="Tool Type",
    )

    tool_name = forms.CharField( 
        label="Tool ", max_length=200, required = True,
        widget=forms.TextInput(attrs={'autocomplete':'off'}),
        error_messages={ 'required': 'The name should not be empty' }
    )
    tool_context = forms.CharField(
        label="Context/Prompt", required = True,
        widget=forms.TextInput(attrs={'autocomplete':'off'}),
        error_messages={ 'required': 'This should not be empty' }
    )
    
    youtube_link = forms.CharField(label="Link", required = True,
        widget=forms.TextInput(attrs={'autocomplete':'off'}),
        error_messages={ 'required': 'This should not be empty' })

    class Meta:
        model = ToolTemplate
        fields = ['tool_type','tool_name','tool_context','youtube_link']

class ToolInputForm(forms.ModelForm):
    tool_input = forms.ModelChoiceField(queryset=ToolInput.objects.all(),                                                   
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False,
        label="Tool Input",)
    
    place_holder =forms.CharField(
            label='place_holder',
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
    
    validation_message =forms.CharField(
            label='validation_message',
            max_length=150,
            required=True,
            widget=forms.TextInput(attrs={'autocomplete': 'off'})
        )

    sort_order =forms.CharField(
            label='sort_order',
            max_length=150,
            required=True,
            widget=forms.TextInput(attrs={'autocomplete': 'off'})
        )
    

    max_length =forms.IntegerField(
            label='maxlength',
            required=True,
            widget=forms.NumberInput(attrs={'autocomplete': 'off'})
        )

    inp_validation_msg1 =forms.CharField(
            label='Validation Message',
            max_length=150,
            required=True,
            widget=forms.TextInput(attrs={'autocomplete': 'off'})
        )
    
    min_length =forms.IntegerField(
            label='minlength',
            required=True,
            widget=forms.NumberInput(attrs={'autocomplete': 'off'})
        )
    
    inp_validation_msg2 =forms.CharField(
            label='Validation Message',
            max_length=150,
            required=True,
            widget=forms.TextInput(attrs={'autocomplete': 'off'})
        )

    class Meta:
        model = ToolTemplateInput
        fields = ['tool_input','place_holder','description','validation_message','sort_order','max_length','inp_validation_msg1','min_length','inp_validation_msg2']


ToolInputFormFormSet = inlineformset_factory(
    ToolTemplate,
    ToolTemplateInput,
    form=ToolInputForm,
    extra=1,
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

