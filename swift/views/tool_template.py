from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, View
from django.urls import reverse
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
                data = form.save()
                for i in item_formset:
                    input_data = {
                        'place_holder':i.cleaned_data.get('place_holder'),
                        'description':i.cleaned_data.get('description'),
                            
                        'max_length':i.cleaned_data.get('max_length'),
                        'max_validation_msg':i.cleaned_data.get('max_validation_msg'),
                        'min_length':i.cleaned_data.get('min_length'),
                        'min_validation_msg':i.cleaned_data.get('min_validation_msg'),
                    }
                    print('input_data=',input_data)
                    tool_input = i.cleaned_data['tool_input']
                    validation_message = i.cleaned_data['validation_message']
                    sort_order = i.cleaned_data['sort_order']
                    ToolTemplateInput.objects.create(
                        tool_template = data,
                        tool_input=tool_input,
                        inputs=input_data,
                        validation_message=validation_message,
                        sort_order=sort_order
                    )
                    print('save')

                response = {
                    'status': True,
                    'message': 'Form submitted successfully!',
                    'redirect_url': reverse('appswift:tooltemplate_create')
                }
            else:
                print('--invalid---')
                print('form',form.errors)
                print('item_formset',item_formset.non_form_errors())

                response = {
                    'status': False,
                    'form_errors': form.errors,
                    'message': 'Form Submission Failed!',
                    'item_formset_errors': item_formset.errors
                }
                print('Respo Print===',response)
            return JsonResponse(response)
        else:
            if form.is_valid()  and item_formset.is_valid():
                with transaction.atomic():
                    tool_template_instance = form.save()                    
                    item_formset.instance = tool_template_instance
                    item_formset.save()
                
                return redirect('appswift:tooltemplate_create')
            else:
                return render(request, 'swift/tooltemplate/index.html',)

class ToolTemplateInputCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        tool = request.GET.get('tool')
        tool_type = ToolInput.objects.get(pk=tool).tool_type.type
        data = {}
        form = ToolInputForm()
        context = {'form': form, 'id': 0, 'input_type': tool_type}
        data['status'] = True
        data['title'] = 'Add Inputs'
        data['input_type'] = tool_type
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
    

class TemplateToolList(LoginRequiredMixin,View):
    template_name = "swift/tooltemplate/tool_list.html"
    def get(self, request, *args, **kwargs):
        tool_types = ToolTemplate.objects.all()
        print('===',tool_types)
        context ={
            'tool_types':tool_types,
        }
        return render(request, self.template_name,context)
    
class TemplateToolDetail(LoginRequiredMixin,View):
    template_name = "swift/tooltemplate/template_form.html"
    def get(self, request, pk, *args, **kwargs):
        tool_template = get_object_or_404(ToolTemplate, pk=pk)
        tool_inputs = ToolTemplateInput.objects.filter(tool_template=tool_template)
        forms = DynamicToolTemplateInputForm(tool_template_inputs=tool_inputs)
        
        context = {
            'tool_template': tool_template,
            'tool_inputs': tool_inputs,
            'forms': forms,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, pk, *args, **kwargs):
        tool_template = get_object_or_404(ToolTemplate, pk=pk)
        tool_inputs = ToolTemplateInput.objects.filter(tool_template=tool_template)
        
        forms = DynamicToolTemplateInputForm(request.POST, tool_template_inputs=tool_inputs)

        if forms.is_valid():
            return redirect('/')
        
        context = {
            'tool_template': tool_template,
            'tool_inputs': tool_inputs,
            'forms': forms,
        }
        return render(request, self.template_name, context)