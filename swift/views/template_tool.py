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


class TemplateToolView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = {}
        form = ToolTemplateForm()
        context = {'form': form, 'id': 0}
        if is_ajax(request=request):
            data['status'] = True
            data['title'] = 'Add Template Tool'
            data['template'] = render_to_string('swift/templatetool/tool_create_form.html', context, request=request)
            return JsonResponse(data)
        return renderfile(request, 'templatetool', 'index', context)
    
    def post(self, request, *args, **kwargs):
        form = ToolTemplateForm(request.POST or None)
        response = {}
        if form.is_valid():
            try:
                with transaction.atomic():
                    tool_name = request.POST.get('tool_name', None)
                    form.save()  
                    print('####----',tool_name)
                    if not ToolTemplate.objects.filter(tool_name=tool_name).exists():
                        response['status'] = True
                        response['message'] = 'Added successfully'
                    else:
                        response['status'] = False
                        response['message'] = 'Template Already exists'
            except Exception as error:
                response['status'] = False
                response['message'] = 'Something went wrong'
        else:
            response['status'] = False
            context = {'form': form}
            response['title'] = 'create'
            response['valid_form'] = False
            response['template'] = render_to_string('swift/templatetool/tool_create_form.html', context, request=request)
        return JsonResponse(response)