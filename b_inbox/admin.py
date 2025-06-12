from django.contrib import admin
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from .models import SubmittedForm

class SubmittedFormAdmin(SnippetViewSet):
    model = SubmittedForm
    menu_label = "MarketPlace"
    icon = "form"
    menu_order = 51
    list_display = ("name", "email", "phone", "date_created")


class InboxSettingAdmin(SnippetViewSetGroup):
    menu_icon = "mail"
    menu_label = "Inbox"
    menu_name = "Inbox"
    items = (
        SubmittedFormAdmin,
    )

register_snippet(InboxSettingAdmin)
