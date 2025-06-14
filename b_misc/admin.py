from django.contrib import admin
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup
from .models import Testimonial, ClientLogo, HomeSlider, ImageGallery, AnnouncementBar

class TestimonialPlaceAdmin(SnippetViewSet):
    model = Testimonial
    menu_label = "Testimonial"
    icon = "comment"
    menu_order = 41
    list_display = ("name", "company", "is_show")

class HomeSliderAdmin(SnippetViewSet):
    model = HomeSlider
    menu_label = "Home Slider"
    icon = "image"
    menu_order = 42
    list_display = ("title", "is_active")

class ClientLogoAdmin(SnippetViewSet):
    model = ClientLogo
    menu_label = "Client Logo"
    icon = "image"
    menu_order = 43
    list_display = ("name", "is_show")

class ImageGalleryAdmin(SnippetViewSet):
    model = ImageGallery
    menu_label = "Image Gallery"
    icon = "image"
    menu_order = 44
    list_display = ("title")

class AnnouncementBarAdmin(SnippetViewSet):
    model = AnnouncementBar
    menu_label = "Announcement Bar"
    icon = "info-circle"
    menu_order = 45
    list_display = ("title", "is_show")

class MiscSettingAdmin(SnippetViewSetGroup):
    menu_icon = "folder"
    menu_label = "Misc Content"
    menu_name = "Misc Content"
    items = (
        TestimonialPlaceAdmin,
        HomeSliderAdmin,
        ClientLogoAdmin,
        ImageGalleryAdmin,
        AnnouncementBarAdmin
    )

register_snippet(MiscSettingAdmin)
