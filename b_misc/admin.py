from django.contrib import admin
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from .models import Testimonial, ClientLogo

class TestimonialPlaceAdmin(SnippetViewSet):
    model = Testimonial
    menu_label = "Testimonial"
    icon = "comment"
    menu_order = 41
    list_display = ("name", "company", "is_show")

class ClientLogoAdmin(SnippetViewSet):
    model = ClientLogo
    menu_label = "Client Logo"
    icon = "image"
    menu_order = 43
    list_display = ("name", "is_show")

class MiscSettingAdmin(SnippetViewSetGroup):
    menu_icon = "folder"
    menu_label = "Misc Content"
    menu_name = "Misc Content"
    items = (
        TestimonialPlaceAdmin,
        ClientLogoAdmin,
    )

register_snippet(MiscSettingAdmin)
