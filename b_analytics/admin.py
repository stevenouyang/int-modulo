from django.contrib import admin
from .models import PageVisitLog, WhatsappLog
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

class WhatsappLogAdmin(SnippetViewSet):
    model = WhatsappLog
    menu_label = "Whatsapp Logs"
    icon = "view"
    menu_order = 25
    list_display = ("ip", "final_url")

class PageVisitLogAdmin(SnippetViewSet):
    model = PageVisitLog
    menu_label = "Page Visit Logs"
    icon = "view"
    menu_order = 25
    list_display = ("ip", "url")

class AnalyticSettingAdmin(SnippetViewSetGroup):
    menu_icon = "view"
    menu_label = "Analytics"
    menu_name = "Analytics"
    items = (
        WhatsappLogAdmin,
        PageVisitLogAdmin
    )

register_snippet(AnalyticSettingAdmin)
