from django.contrib import admin
from swift.models import *
# Register your models here.

@admin.register(InputType)
class InputTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "type",)
@admin.register(ToolInput)
class ToolInputAdmin(admin.ModelAdmin):
    list_display = ("name",)
@admin.register(ToolType)
class ToolTypeAdmin(admin.ModelAdmin):
    list_display = ("tool_type_category", "custom_tool_name",)
@admin.register(ToolTemplate)
class ToolTemplateAdmin(admin.ModelAdmin):
    list_display = ("tool_type", "tool_name",)
@admin.register(ToolTemplateInput)
class ToolTemplateInputAdmin(admin.ModelAdmin):
    list_display = ("tool_template", "tool_input",)

