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


#https://stackoverflow.com/questions/67340140/how-to-insert-javascript-object-into-django-jsonfield
#https://www.quora.com/What-is-the-difference-between-request-get-and-request-GET-get-in-django
#https://chatgpt.com/share/4ce2458b-a09d-436f-9ea8-5eb52ebe864a