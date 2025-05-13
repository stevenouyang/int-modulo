from django.contrib import admin
from .models import BlogCategory
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

class BlogCategoryAdmin(SnippetViewSet):
    model = BlogCategory
    menu_label = "Blog Category"
    icon = "list"
    menu_order = 25
    list_display = ("name", )

class BlogSettingAdmin(SnippetViewSetGroup):
    menu_icon = "doc-full-inverse"
    menu_label = "Blog"
    menu_name = "Blog"
    items = (
        BlogCategoryAdmin,
    )

register_snippet(BlogSettingAdmin)
