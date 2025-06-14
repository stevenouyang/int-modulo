from django.contrib import admin
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from .models import Car, CarSpecCategory, Specification

class ProductAdmin(SnippetViewSet):
    model = Car
    menu_label = "Product"
    icon = "pick"
    menu_order = 20
    list_display = ("title", "is_coming_soon", )

class CarSpecAdmin(SnippetViewSet):
    model = Specification
    menu_label = "Car Specifications"
    icon = "sliders"
    menu_order = 20
    list_display = ("title", "carspec_category", )

class CarSpecCategoryAdmin(SnippetViewSet):
    model = CarSpecCategory
    menu_label = "Car Spec Category"
    icon = "list-ul"
    menu_order = 20
    list_display = ("title", )

class ProductSettingAdmin(SnippetViewSetGroup):
    menu_icon = "pick"
    menu_label = "Dealer"
    menu_name = "Dealer"
    items = (
        ProductAdmin,
        CarSpecAdmin,
        CarSpecCategoryAdmin
    )

register_snippet(ProductSettingAdmin)
