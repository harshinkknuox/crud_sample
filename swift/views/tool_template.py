from django.contrib.auth.mixins import LoginRequiredMixin
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
            'inp_form': ToolInputForm(),
            'item_formset': ToolInputFormFormSet()
        }

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            
            tool_input = request.GET.get('tool_input')
            queryset = ToolTemplateInput.objects.all()
            if tool_input:
                queryset = queryset.filter(tool_input=tool_input)
            input_value = list(queryset.values("id", "name","type"))
        
            
            
            response = {
                'input_value': input_value,
                
                'status': True,
                'template': render_to_string('swift/tooltemplate/input_details_form.html', context, request=request)
            }
            return JsonResponse(response)
        
        return render(request, 'swift/tooltemplate/index.html', context)

    def post(self, request, *args, **kwargs):
        form = ToolTemplateForm(request.POST, request.FILES)
        inp_form = ToolInputForm(request.POST)
        item_formset = ToolInputFormFormSet(request.POST)

        context = {
            'form': form,
            'inp_form': inp_form,
            'item_formset': item_formset
        }

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if form.is_valid() and inp_form.is_valid() and item_formset.is_valid():
                with transaction.atomic():
                    tool_template_instance = form.save()
                    tool_input_instance = inp_form.save(commit=False)
                    tool_input_instance.tool_template = tool_template_instance
                    tool_input_instance.save()
                    item_formset.instance = tool_template_instance
                    item_formset.save()
                
                response = {
                    'status': True,
                    'message': 'Form submitted successfully!'
                }
            else:
                response = {
                    'status': False,
                    'form_errors': form.errors,
                    'inp_form_errors': inp_form.errors,
                    'item_formset_errors': item_formset.errors
                }
            return JsonResponse(response)
        else:
            if form.is_valid() and inp_form.is_valid() and item_formset.is_valid():
                with transaction.atomic():
                    tool_template_instance = form.save()
                    tool_input_instance = inp_form.save(commit=False)
                    tool_input_instance.tool_template = tool_template_instance
                    tool_input_instance.save()
                    
                    item_formset.instance = tool_template_instance
                    item_formset.save()
                
                return redirect('appswift:tooltemplate_create')
            else:
                return render(request, 'swift/tooltemplate/index.html', context)

class ToolTemplateInputCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = {}
        form = ToolInputForm()
        context = {'form': form, 'id': 0}
        data['status'] = True
        data['title'] = 'Add Inputs'
        
        data['template'] = render_to_string('swift/tooltemplate/input_details_form.html', context, request=request)
        
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        inputs_data = {
                    'place_holder': request.POST.getlist('place_holder'),
                    'description': request.POST.getlist('description'),
                    'max_length': request.POST.getlist('max_length'),
                    'inp_validation_msg1':request.POST.getlist('inp_validation_msg1'),
                    'min_length': request.POST.getlist('min_length'),
                    'inp_validation_msg2':request.POST.getlist('inp_validation_msg2')
                }
        response = {}
        form = ToolInputForm(request.POST or None,initial={'data': inputs_data})
        if form.is_valid():

            try:
                with transaction.atomic():
                    
                    tool_template = request.POST.get('tool_template', None)
                    # CHECK THE DATA EXISTS
                    if not ToolTemplateInput.objects.filter(tool_template=tool_template).exists():
                        obj = ToolTemplateInput.objects.create(tool_template=tool_template, inputs=json.dumps(inputs_data))
                        
                        
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