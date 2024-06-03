from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, View
from swift.forms.tool_template import * 
from swift.helper import renderfile, is_ajax, LogUserActivity
from swift.models import ToolInput,ToolType,ToolTemplateInput,ToolTemplate,ToolKeyword
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, redirect, render
from swift.models import CREATE,  UPDATE, SUCCESS, FAILED, DELETE, READ
from django.db import transaction
import pdb
import json


class ToolTemplateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': ToolTemplateForm(),
            'item_formset': ToolInputFormFormSet()
        }
        return render(request, 'swift/tooltemplate/index.html', context)

    def post(self, request, *args, **kwargs):
        form = ToolTemplateForm(request.POST, request.FILES)
        item_formset = ToolInputFormFormSet(request.POST)
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if form.is_valid()  and item_formset.is_valid():
                with transaction.atomic():
                    form.save()
                    print("form save")
                    item_formset.instance= form.instance
                    item_formset.save()
                    print('item_formset===',item_formset)
                response = {
                    'status': True,
                    'message': 'Form submitted successfully!',
                    'redirect_url': reverse('appswift:tooltemplate_create')
                    
                }
            else:
                print('form',form.errors)
                print('item_formset',item_formset.errors)
                response = {
                    'status': False,
                    'form_errors': form.errors,
                    'item_formset_errors': item_formset.errors
                }
            return JsonResponse(response)
        else:
            if form.is_valid()  and item_formset.is_valid():
                with transaction.atomic():
                    tool_template_instance = form.save()  
                    item_formset.instance = tool_template_instance
                    item_formset.save()
                
                return redirect('appswift:tooltemplate_create')
            else:
                return render(request, 'swift/tooltemplate/index.html')

class ToolTemplateInputCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tool = request.GET.get('tool')
        prefix = request.POST.get('prefix')
        print("prefix====",prefix)
        tool_type = ToolInput.objects.get(pk=tool).tool_type.type
        data = {}
        form = ToolInputForm(prefix=prefix)
        context = {'form': form, 'id': 0, 'input_type': tool_type}
        data['status'] = True
        data['title'] = 'Add Inputs'
        data['template'] = render_to_string('swift/tooltemplate/input_details_form.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        response = {}
        inputs_data = {
            'place_holder': request.POST.getlist('place_holder'),
            'description': request.POST.getlist('description'),
            'max_length': request.POST.getlist('max_length'),
            'inp_validation_msg1': request.POST.getlist('inp_validation_msg1'),
            'min_length': request.POST.getlist('min_length'),
            'inp_validation_msg2': request.POST.getlist('inp_validation_msg2')
        }
        print('inputs_data---',inputs_data)
        form = ToolInputForm(request.POST or None, initial={'data': inputs_data})
        print('form_data---',form)
        
        temp_form = ToolTemplateForm(request.POST, request.FILES)
        print('temp_form----',temp_form)
        if form.is_valid() and temp_form.is_valid():
            try:
                with transaction.atomic():
                    tool_template = request.POST.get('tool_template', None)
                    if not ToolTemplateInput.objects.filter(tool_template=tool_template).exists():
                        inputs_data_json = json.dumps(inputs_data)
                        obj = ToolTemplateInput.objects.create(tool_template=tool_template, inputs=inputs_data_json)
                        
                        response['status'] = True
                        response['message'] = 'Added successfully'
                    else:
                        response['status'] = False
                        response['message'] = 'Inputs Already exists'
            except Exception as error:
                response['status'] = False
                response['message'] = 'Something went wrong'
        else:
            response['status'] = False
            context = {'form': form}
            response['title'] = 'Add Inputs'
            response['valid_form'] = False
            response['template'] = render_to_string('swift/tooltemplate/input_details_form.html', context, request=request)
        return JsonResponse(response)