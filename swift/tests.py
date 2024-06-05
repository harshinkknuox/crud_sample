from django.test import TestCase
from swift.models import ToolTemplateInput,ToolInput,ToolTemplate
# Create your tests here

# input_keys = [key for key in request.POST.keys() if key.startswith('input_tool')]
#             for key in input_keys:
#                 index = key.split('[')[1][:-1]
#                 input_tool_values = request.POST.getlist(f'input_tool[{index}]')
#                 for input_tool in input_tool_values:
#                     if input_tool:
#                         placeholder_key = f'place_holder[{index}]'
#                         description_key = f'description[{index}]'

#                         placeholder = request.POST.get(placeholder_key,'')
#                         description = request.POST.get(description_key,'')
#                         print('=description=',description)

#                         tool_template_input_instance = ToolTemplateInput.objects.create(description=description, placeholder=placeholder)


# data = json.loads(request.body)
#             print("json data----",data)