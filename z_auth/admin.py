from django.contrib import admin
from .models import User
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email"]

admin.site.register(User, UserAdmin)