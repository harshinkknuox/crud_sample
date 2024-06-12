
dict1 = {
    'placeholder':'Age',
    'description':'Age of students',
    'validation_message':{ 'max_length':50,'min_length':18}
}
dict2 = {
    'placeholder':'EMail',
    'description':'Email',
}
a = {'select':[{'a':1,'set_as_default':True},{'b':{'l':[]}},{'c':3}]}
for i in a['select']:
    print(i.get('b',False))
    print('{0}-{1}'.format(i.get('a',False),i.get('set_as_default',False)))

# validation = [
#     {'input':1,'input_details':{'min_length':'','max_length':100},'validation_message':'Required','sort':1},
#     {'input':2,'input_details':{'min_length':'','max_length':200,'place_holder':'', 'description': ''},'validation_message':'Required','sort':1},
#     {'input':3,'input_details':{'min_length':'','max_length':300},'validation_message':'Required','sort':1},
# ]
# data = []
# for i in validation:
#     ToolTemplateInput(tool_template_id=1, sort=i.get('sort',None),tool_input_id=i['input'],inputs=i['input_details'])
# ToolTemplateInput.objects.bulk_create(data)


# print(dict1['placeholder'])
# print(dict1['validation_message']['min_length'])
# dict.get('description', False)
# if dict2.get('min_length', False):
#     print('**'*100)





# onditional section
# The code then checks if the input_type variable is not equal to 'email'. If this condition is true, the following section is rendered:

# More Validation section
# This section contains two list items (li elements) with classes pop-input-items. Each list item contains two input fields with labels and validation error messages:

# maxlength:
# A text input field for setting the maximum length of the input.
# A text input field for setting the validation message for the maximum length.
# minlength:
# A text input field for setting the minimum length of the input.
# A text input field for setting the validation message for the minimum length.