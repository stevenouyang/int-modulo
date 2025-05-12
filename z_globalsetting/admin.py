from django.contrib import admin
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from .models import BrandingSetting

class BrandingSettingAdmin(SnippetViewSet):
    model = BrandingSetting
    menu_label = "Branding Setting"
    icon = "image"
    menu_order = 11
    list_display = ("id" ,"site_name")
    add_to_settings_menu = True


register_snippet(BrandingSettingAdmin)
