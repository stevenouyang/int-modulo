from django.contrib import admin
from .models import ServiceCategory
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

# Register your models here.
class ServiceCategoryAdmin(SnippetViewSet):
    model = ServiceCategory
    menu_label = "Service Category"
    icon = "list-ul"
    menu_order = 28
    list_display = ("name", )

class ServiceSettingAdmin(SnippetViewSetGroup):
    menu_icon = "doc-full"
    menu_label = "Service"
    menu_name = "Service"
    items = (
        ServiceCategoryAdmin,
    )

register_snippet(ServiceSettingAdmin)
