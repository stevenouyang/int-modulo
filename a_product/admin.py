from django.contrib import admin
from .models import ProductCategory, Product, Specification, MarketPlace
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup



class ProductMAdmin(SnippetViewSet):
    model = Product
    menu_label = "Product"
    icon = "pick"
    menu_order = 3
    list_display = ("title", "category", "is_highlight", "views")


class ProductCategoryAdmin(SnippetViewSet):
    model = ProductCategory
    menu_label = "Product Category"
    icon = "list-ul"
    menu_order = 4
    list_display = ("title", )


class SpecificationAdmin(SnippetViewSet):
    model = Specification
    menu_label = "Specification"
    icon = "list-ul"
    menu_order = 5
    list_display = ("title", "order", )


class MarketPlaceAdmin(SnippetViewSet):
    model = MarketPlace
    menu_label = "MarketPlace"
    icon = "globe"
    menu_order = 6
    list_display = ("title", "link", )


class ProductSettingAdmin(SnippetViewSetGroup):
    menu_icon = "pick"
    menu_label = "Product"
    menu_name = "Product"
    items = (
        ProductMAdmin,
        ProductCategoryAdmin,
        SpecificationAdmin,
        MarketPlaceAdmin,
    )

register_snippet(ProductSettingAdmin)
