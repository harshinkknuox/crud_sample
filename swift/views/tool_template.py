from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, View
from swift.forms.tool_template import * 
from swift.helper import renderfile, is_ajax, LogUserActivity
from swift.models import ToolInput,ToolType,ToolTemplateInput,ToolTemplate,ToolKeyword
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from swift.models import CREATE,  UPDATE, SUCCESS, FAILED, DELETE, READ
from django.db import transaction
import pdb



class ToolTemplateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context, response = {}, {}
        
        if is_ajax(request=request):
            response['status'] = True
            response['template'] = render_to_string('swift/tooltemplate/tool_template_form.html', context, request=request)
            return JsonResponse(response)
        context['form']  = ToolTemplateForm()
        context['inp_form'] = ToolInputForm()
        return renderfile(request, 'tooltemplate', 'index', context)
    
class ToolTemplateCreate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = {}
        form = ToolTemplateForm()
        context = {'form': form, 'id': 0}
        data['status'] = True
        data['template'] = render_to_string('swift/tooltemplate/tool_template_form.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        response = {}
        form = ToolTemplateForm(request.POST or None)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    name = request.POST.get('name', None)
                    # CHECK THE DATA EXISTS
                    if not ToolTemplate.objects.filter(name=name).exists():
                        obj = ToolTemplate.objects.create(name=name)

                        # log entry
                        log_data = {}
                        log_data['module_name'] = 'Curriculum'
                        log_data['action_type'] = CREATE
                        log_data['log_message'] = 'Curriculum Created'
                        log_data['status'] = SUCCESS
                        log_data['model_object'] = obj
                        log_data['db_data'] = {'name':name}
                        log_data['app_visibility'] = True
                        log_data['web_visibility'] = True
                        log_data['error_msg'] = ''
                        log_data['fwd_link'] = '/curriculum/'
                        LogUserActivity(request, log_data)

                        response['status'] = True
                        response['message'] = 'Added successfully'
                    else:
                        response['status'] = False
                        response['message'] = 'Curriculum Already exists'

            except Exception as error:
                log_data = {}
                log_data['module_name'] = 'Curriculum'
                log_data['action_type'] = CREATE
                log_data['log_message'] = 'Curriculum updation failed'
                log_data['status'] = FAILED
                log_data['model_object'] = None
                log_data['db_data'] = {}
                log_data['app_visibility'] = False
                log_data['web_visibility'] = False
                log_data['error_msg'] = error
                log_data['fwd_link'] = '/curriculum/'
                LogUserActivity(request, log_data)

                response['status'] = False
                response['message'] = 'Something went wrong'
        else:
            response['status'] = False
            context = {'form': form}
            response['title'] = 'toolss'
            response['valid_form'] = False
            response['template'] = render_to_string('swift/tooltemplate/tool_template_form.html', context, request=request)
        return JsonResponse(response)
    
