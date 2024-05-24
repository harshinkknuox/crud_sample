from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, View
from swift.forms.prompt import PromptForm
from swift.helper import renderfile, is_ajax, LogUserActivity
from swift.models import Prompt
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import *
from swift.constantvariables import PAGINATION_PERPAGE
from django.shortcuts import get_object_or_404
from swift.models import CREATE,  UPDATE, SUCCESS, FAILED, DELETE, READ
from django.db import transaction
import pdb


class PromptView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context, response = {}, {}
        page = int(request.GET.get('page', 1))
        prompts = Prompt.objects.filter(is_active=True).order_by('-id')

        paginator = Paginator(prompts, PAGINATION_PERPAGE)
        try:
            prompts = paginator.page(page)
        except PageNotAnInteger:
            prompts = paginator.page(1)
        except EmptyPage:
            prompts = paginator.page(paginator.num_pages)

        context['prompts'], context['current_page'] = prompts, page
        if is_ajax(request=request):
            response['status'] = True
            response['pagination'] = render_to_string("swift/prompt/pagination.html",context=context,request=request)
            response['template'] = render_to_string('swift/prompt/prompt_list.html', context, request=request)
            return JsonResponse(response)
        context['form']  = PromptForm()
        return renderfile(request, 'prompt', 'index', context)
    

class PromptCreate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = {}
        form = PromptForm()
        context = {'form': form, 'id': 0}
        data['status'] = True
        data['title'] = 'Add Prompt'
        data['template'] = render_to_string('swift/prompt/prompt_form.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        response = {}
        form = PromptForm(request.POST or None)
        if form.is_valid():
            try:
                with transaction.atomic():
                    name = request.POST.get('name', None)
                    # CHECK THE DATA EXISTS
                    if not Prompt.objects.filter(name=name).exists():
                        obj = Prompt.objects.create(name=name)

                        # log entry
                        log_data = {}
                        log_data['module_name'] = 'Prompt'
                        log_data['action_type'] = CREATE
                        log_data['log_message'] = 'Prompt Created'
                        log_data['status'] = SUCCESS
                        log_data['model_object'] = obj
                        log_data['db_data'] = {'name':name}
                        log_data['app_visibility'] = True
                        log_data['web_visibility'] = True
                        log_data['error_msg'] = ''
                        log_data['fwd_link'] = '/prompt/'
                        LogUserActivity(request, log_data)

                        response['status'] = True
                        response['message'] = 'Added successfully'
                    else:
                        response['status'] = False
                        response['message'] = 'Prompt Already exists'

            except Exception as error:
                log_data = {}
                log_data['module_name'] = 'Prompt'
                log_data['action_type'] = CREATE
                log_data['log_message'] = 'Prompt updation failed'
                log_data['status'] = FAILED
                log_data['model_object'] = None
                log_data['db_data'] = {}
                log_data['app_visibility'] = False
                log_data['web_visibility'] = False
                log_data['error_msg'] = error
                log_data['fwd_link'] = '/prompt/'
                LogUserActivity(request, log_data)

                response['status'] = False
                response['message'] = 'Something went wrong'
        else:
            response['status'] = False
            context = {'form': form}
            response['title'] = 'Edit Prompt'
            response['valid_form'] = False
            response['template'] = render_to_string('swift/prompt/prompt_form.html', context, request=request)
        return JsonResponse(response)
    


class PromptUpdate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk', None)
        data = {}
        obj = get_object_or_404(Prompt, id = id)
        form = PromptForm(instance=obj)
        context = {'form': form, 'id': id}
        data['status'] = True
        data['title'] = 'Edit Prompt'
        data['template'] = render_to_string('swift/prompt/prompt_form.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data, response = {} , {}
        id = kwargs.get('pk', None)
        obj = get_object_or_404(Prompt, id=id)
        previous_name = obj.name
        form = PromptForm(request.POST or None, instance=obj)

        if form.is_valid():
            try:
                with transaction.atomic():
                    if Prompt.objects.filter(name__icontains=request.POST.get('name')).exclude(id=id).exists():
                        response['status'] = False
                        response['message'] = "Name already exists"
                        return JsonResponse(response)
                    obj.name = request.POST.get('name' or None)
                    obj.description = request.POST.get('description' or None)
                    obj.save()

                    # log entry
                    log_data = {}
                    log_data['module_name'] = 'Prompt'
                    log_data['action_type'] = UPDATE
                    log_data['log_message'] = 'Prompt Updated'
                    log_data['status'] = SUCCESS
                    log_data['model_object'] = obj
                    log_data['db_data'] = {'previous_name':previous_name,'updated_name':obj.name}
                    log_data['app_visibility'] = True
                    log_data['web_visibility'] = True
                    log_data['error_msg'] = ''
                    log_data['fwd_link'] = '/prompt/'
                    LogUserActivity(request, log_data)

                    response['status'] = True
                    response['message'] = "Prompt updated successfully"
                    return JsonResponse(response)
                
            except Exception as dberror:
                log_data = {}
                log_data['module_name'] = 'Prompt'
                log_data['action_type'] = UPDATE
                log_data['log_message'] = 'Prompt updation failed'
                log_data['status'] = FAILED
                log_data['model_object'] = None
                log_data['db_data'] = {}
                log_data['app_visibility'] = False
                log_data['web_visibility'] = False
                log_data['error_msg'] = dberror
                log_data['fwd_link'] = '/prompt/'
                LogUserActivity(request, log_data)

                response['message'] = "Something went wrong"
                response['status'] = True
        else:
            response['status'] = False
            context = {'form': form}
            response['title'] = 'Edit Prompt'
            response['valid_form'] = False
            response['template'] = render_to_string('swift/prompt/prompt_form.html', context, request=request)
            return JsonResponse(response)
        


class PromptOutCreate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        data = {}
        form = PromptForm()
        context = {'form': form, 'id': 0}
        data['status'] = True
        data['title'] = 'Add Prompt'
        data['template'] = render_to_string('swift/prompt/prompt_form.html', context, request=request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        response = {}
        form = PromptForm(request.POST or None)
        if form.is_valid():
            try:
                with transaction.atomic():
                    name = request.POST.get('name', None)
                    # CHECK THE DATA EXISTS
                    if not Prompt.objects.filter(name=name).exists():
                        obj = Prompt.objects.create(name=name)

                        # log entry
                        log_data = {}
                        log_data['module_name'] = 'Prompt'
                        log_data['action_type'] = CREATE
                        log_data['log_message'] = 'Prompt Created'
                        log_data['status'] = SUCCESS
                        log_data['model_object'] = obj
                        log_data['db_data'] = {'name':name}
                        log_data['app_visibility'] = True
                        log_data['web_visibility'] = True
                        log_data['error_msg'] = ''
                        log_data['fwd_link'] = '/prompt/'
                        LogUserActivity(request, log_data)

                        response['status'] = True
                        response['message'] = 'Added successfully'
                    else:
                        response['status'] = False
                        response['message'] = 'Prompt Already exists'

            except Exception as error:
                log_data = {}
                log_data['module_name'] = 'Prompt'
                log_data['action_type'] = CREATE
                log_data['log_message'] = 'Prompt updation failed'
                log_data['status'] = FAILED
                log_data['model_object'] = None
                log_data['db_data'] = {}
                log_data['app_visibility'] = False
                log_data['web_visibility'] = False
                log_data['error_msg'] = error
                log_data['fwd_link'] = '/prompt/'
                LogUserActivity(request, log_data)

                response['status'] = False
                response['message'] = 'Something went wrong'
        else:
            response['status'] = False
            context = {'form': form}
            response['title'] = 'Edit Prompt'
            response['valid_form'] = False
            response['template'] = render_to_string('swift/prompt/prompt_form.html', context, request=request)
        return JsonResponse(response)
