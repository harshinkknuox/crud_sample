# # views.py
# from django.shortcuts import render
# from .models import ToolTemplate, ToolTemplateInput

# def tool_template_list(request):
#     tool_templates = ToolTemplate.objects.all()
#     return render(request, 'tool_templates.html', {'tool_templates': tool_templates})

# def tool_template_input_detail(request, pk):
#     tool_template_input = ToolTemplateInput.objects.get(pk=pk)
#     return render(request, 'tool_template_input_detail.html', {'tool_template_input': tool_template_input})


# tool_templates = ToolTemplate.objects.all().prefetch_related('tooltemplateinput_set')

# for tool_template in tool_templates:
#     print(tool_template)  # prints the ToolTemplate instance
#     for tool_template_input in tool_template.tooltemplateinput_set.all():
#         print(tool_template_input)  # prints the related ToolTemplateInput instances


# class DynamicToolTemplateInputForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         tool_template_inputs = kwargs.pop('tool_template_inputs', [])
#         super(DynamicToolTemplateInputForm, self).__init__(*args, **kwargs)
        
#         for tool_template_input in tool_template_inputs:
#             tool_input = tool_template_input.tool_input
#             input_attributes = tool_template_input.inputs
#             input_validation_message = tool_template_input.validation_message
#             input_sort_order = tool_template_input.sort_order
            
#             field_type = tool_input.tool_type.type
#             field_name = tool_input.name
#             field_kwargs = {
#                 'label': field_name,
#                 'required': input_attributes.get('required', True),
#                 # 'initial': input_attributes.get('initial', None),
#                 # 'help_text': input_attributes.get('description', ''),
#             }
#             max_length = input_attributes.get('max_length')
#             min_length = input_attributes.get('min_length')
#             placeholder = input_attributes.get('place_holder')
#             max_validation_msg = input_attributes.get('max_validation_msg')
#             min_validation_msg = input_attributes.get('min_validation_msg')
#             validation_message = input_validation_message
            
#             if field_type == 'text':
#                 field = forms.CharField(widget=forms.TextInput(attrs={'placeholder': placeholder,'class':'form-control'}), **field_kwargs)
#                 if min_length:
#                     field.validators.append(MinLengthValidator(min_length, message=min_validation_msg))
#                 if max_length:
#                     field.validators.append(MaxLengthValidator(max_length, message=max_validation_msg))
#             elif field_type == 'number':
#                 field = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': placeholder,'class':'form-control'}), **field_kwargs)
#                 if max_length:
#                     field.validators.append(MaxValueValidator(10**(max_length-1), message=max_validation_msg))
#                 if min_length:
#                     field.validators.append(MinValueValidator(10**(min_length-1), message=min_validation_msg))
#             elif field_type == 'email':
#                 field = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': placeholder,'class':'form-control'}), **field_kwargs)
#             elif field_type == 'textarea':
#                 field = forms.CharField(widget=forms.Textarea(attrs={'placeholder': placeholder,'class':'form-control'}), **field_kwargs)
                # if min_length:
                #     field.validators.append(MinLengthValidator(min_length, message=min_validation_msg))
                # if max_length:
                #     field.validators.append(MaxLengthValidator(max_length, message=max_validation_msg))
#             else:
#                 continue
            
#             self.fields[field_name] = field

#https://stackoverflow.com/questions/67340140/how-to-insert-javascript-object-into-django-jsonfield
#https://www.quora.com/What-is-the-difference-between-request-get-and-request-GET-get-in-django
#https://chatgpt.com/share/4ce2458b-a09d-436f-9ea8-5eb52ebe864a

# {"options": [{"option_1": "Male", "option_2": "Female"}]}