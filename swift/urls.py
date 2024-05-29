from django.urls import path
from swift.views.account import *
from swift.views.curriculum import *
from swift.views.course import *
from swift.views.prompt import *
from swift.views.tool_template import *

app_name = "appswift"
# views
urlpatterns = [
    # Landing Page
    path("", SignIn.as_view(), name="signin"),
    path("home/", Home.as_view(), name="home"),

    #Login Actions 
    path("signin/", SignIn.as_view(), name="signin"),
    path("forgot-password/", ForgotPassword.as_view(),name="forgot_password"),
    path("signout/", SignOut.as_view(), name="signout"),

    #Curriculum
    path("curriculum/", CurriculumView.as_view(), name="curriculum"),
    path('curriculum/create/', CurriculumCreate.as_view(), name='create_curriculum'),
    path('curriculum/<int:pk>/update/', CurriculumUpdate.as_view(), name='update_curriculum'),
    path('curriculum/<int:pk>/delete/', CurriculumDelete.as_view(), name='delete_curriculum'),


    #Course
    path('course/', CourseView.as_view(), name='course'),
    # path('course/create/', CourseCreate.as_view(), name='create_course'),
    # path('course/<int:pk>/update/', CourseUpdate.as_view(), name='update_course'),
    # path('course/<int:pk>/delete/', CourseDelete.as_view(), name='delete_course'),
    
    #Prompt
    path('prompt/', PromptView.as_view(), name='prompt'),
    path('prompt/create/', PromptCreate.as_view(), name='create_prompt'),
    path('prompt/<int:pk>/update/', PromptUpdate.as_view(), name='update_prompt'),

    #PromptOut
    path('promptout/create/', PromptOutCreate.as_view(), name='create_promptout'),


    #ToolTemplate
    path('tooltemplate/create', ToolTemplateView.as_view(), name='tooltemplate_create'),
    path('tooltemplate/input-details/create',ToolTemplateInputCreateView.as_view(), name='tooltemplate_input_create'),
    
    
]