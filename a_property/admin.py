from django.contrib import admin
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from .models import *

class PropertyAgentAdmin(SnippetViewSet):
    model = PropertyAgent
    menu_label = "Property Agent"
    icon = "group"
    list_display = ["name"]



class PropertyAdminGroup(SnippetViewSetGroup):
    menu_icon = "pick"
    menu_label = "Property"
    menu_name = "Property"
    items = (
        PropertyAgentAdmin,
    )


register_snippet(PropertyAdminGroup)
