from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, View
from swift.forms.course import CourseForm
from swift.helper import renderfile, is_ajax, LogUserActivity
from swift.models import Course
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.core.paginator import *
from swift.constantvariables import PAGINATION_PERPAGE
from django.shortcuts import get_object_or_404
from swift.models import CREATE,  UPDATE, SUCCESS, FAILED, DELETE, READ
from django.db import transaction
import pdb

class CourseView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        context, response = {},{}
        page = int(request.GET.get('page', 1))
        courses = Course.objects.filter(is_active=True).order_by('-id')
        paginator = Paginator(courses, PAGINATION_PERPAGE)
        try:
            courses = paginator.page(page)
        except PageNotAnInteger:
            courses = paginator.page(1)
        except EmptyPage:
            courses = paginator.page(paginator.num_pages)

        context['courses'], context['current_page'] = courses , page

        if is_ajax(request=request):
            response['status'] = True
            return JsonResponse(response)
        context['form'] = CourseForm
        return renderfile(request,'course','index',context)
    

class CourseCreate(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        data = {}
        form = CourseForm()
        context = {'form':form,'id':0}
        data['status'] = True
        data['title'] = 'Add Course'
        data['template'] = render_to_string('swift/course/course_form.html', context, request=request)
        return JsonResponse(data)