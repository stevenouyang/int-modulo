from django.db import models
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    BaseSiteSetting,
    register_setting,
)
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit, Adjust
from solo.models import SingletonModel
from colorfield.fields import ColorField
from wagtail.models import Site
from django.conf import settings


class BrandingSetting(SingletonModel):
    site_name                   = models.CharField(max_length=255, verbose_name="Site Name", default="Denza")
    company_name                = models.CharField(max_length=255, verbose_name="Company Name", default="Denza Indonesia")

    logo                        = models.ImageField(upload_to='branding/logo/', blank=True, null=True, verbose_name="Logo")
    logo_processed              = ImageSpecField(
                                    source="logo",
                                    processors=[ResizeToFill(1920, 600)],
                                    format="webP",
                                    options={"quality": 90},
                                )

    emblem                      = models.ImageField(upload_to='branding/emblem/', blank=True, null=True, verbose_name="Emblem")
    emblem_processed            = ImageSpecField(
                                    source="emblem",
                                    processors=[ResizeToFill(400, 400)],
                                    format="webP",
                                    options={"quality": 90},
                                )

    emblem_rounded              = models.ImageField(upload_to='branding/emblem/', blank=True, null=True, verbose_name="Emblem Ronded BG")
    emblem_rounded_processed    = ImageSpecField(
                                    source="emblem_rounded",
                                    processors=[ResizeToFill(400, 400)],
                                    format="webP",
                                    options={"quality": 90},
                                )

    favicon                     = models.ImageField(upload_to='branding/favicon/', blank=True, null=True, verbose_name="Favicon")
    favicon_processed           = ImageSpecField(
                                    source="favicon",
                                    processors=[ResizeToFill(1920, 600)],
                                    format="webP",
                                    options={"quality": 90},
                                )

    panels = [
        FieldPanel("site_name"),
        FieldPanel("company_name"),
        FieldPanel("logo"),
        FieldPanel("emblem"),
        FieldPanel("emblem_rounded"),
        FieldPanel("favicon"),
    ]

    def __str__(self):
        return "Branding Settings"

    class Meta:
        verbose_name = "Branding Setting"


@register_setting
class ContactSetting(BaseGenericSetting):
    whatsapp_number     = models.CharField(max_length=15, blank=True, null=True)
    whatsapp_link       = models.URLField(blank=True, null=True)
    email               = models.EmailField(max_length=50, blank=True, null=True)
    address             = models.TextField(blank=True, null=True)
    phone               = models.CharField(max_length=15, blank=True, null=True)
    phone_display       = models.CharField(max_length=20, blank=True, null=True)
    whatsapp_prefix     = models.CharField(max_length=50, blank=True, null=True)

    panels = [
        FieldPanel("whatsapp_number"),
        FieldPanel("whatsapp_link"),
        FieldPanel("whatsapp_prefix"),
        FieldPanel("email"),
        FieldPanel("address"),
        FieldPanel("phone"),
        FieldPanel("phone_display"),
    ]


@register_setting
class SocialSetting(BaseGenericSetting):
    instagram_link      = models.URLField(blank=True, null=True)
    linkedin_link       = models.URLField(blank=True, null=True)
    tiktok_link         = models.URLField(blank=True, null=True)
    facebook_link       = models.URLField(blank=True, null=True)
    twitter_link        = models.URLField(blank=True, null=True)
    youtube_link        = models.URLField(blank=True, null=True)

    panels = [
        FieldPanel("instagram_link"),
        FieldPanel("linkedin_link"),
        FieldPanel("tiktok_link"),
        FieldPanel("facebook_link"),
        FieldPanel("twitter_link"),
        FieldPanel("youtube_link"),
    ]


@register_setting
class PageSEOSetting(BaseGenericSetting):
    home_meta_key           = models.TextField(max_length=100, blank=True, null=True)
    home_meta_desc          = models.TextField(max_length=160, blank=True, null=True)
    blog_meta_key           = models.TextField(max_length=100, blank=True, null=True)
    blog_meta_desc          = models.TextField(max_length=160, blank=True, null=True)
    product_meta_key        = models.TextField(max_length=100, blank=True, null=True)
    product_meta_desc       = models.TextField(max_length=160, blank=True, null=True)
    portfolio_meta_key      = models.TextField(max_length=100, blank=True, null=True)
    portfolio_meta_desc     = models.TextField(max_length=160, blank=True, null=True)
    service_meta_key        = models.TextField(max_length=100, blank=True, null=True)
    service_meta_desc       = models.TextField(max_length=160, blank=True, null=True)
    booking_meta_key        = models.TextField(max_length=100, blank=True, null=True)
    booking_meta_desc       = models.TextField(max_length=160, blank=True, null=True)
    property_meta_key       = models.TextField(max_length=100, blank=True, null=True)
    property_meta_desc      = models.TextField(max_length=160, blank=True, null=True)
    event_meta_key          = models.TextField(max_length=100, blank=True, null=True)
    event_meta_desc         = models.TextField(max_length=160, blank=True, null=True)

    panels = [
        FieldPanel("home_meta_key"),
        FieldPanel("home_meta_desc"),
    ]

    if getattr(settings, "MODULE_BLOG", False):
        panels += [
            FieldPanel("blog_meta_key"),
            FieldPanel("blog_meta_desc"),
        ]

    if getattr(settings, "MODULE_PRODUCT", False):
        panels += [
            FieldPanel("product_meta_key"),
            FieldPanel("product_meta_desc"),
        ]

    if getattr(settings, "MODULE_PORTFOLIO", False):
        panels += [
            FieldPanel("portfolio_meta_key"),
            FieldPanel("portfolio_meta_desc"),
        ]

    if getattr(settings, "MODULE_SERVICE", False):
        panels += [
            FieldPanel("service_meta_key"),
            FieldPanel("service_meta_desc"),
        ]

    if getattr(settings, "MODULE_BOOKING", False):
        panels += [
            FieldPanel("booking_meta_key"),
            FieldPanel("booking_meta_desc"),
        ]

    if getattr(settings, "MODULE_PROPERTY", False):
        panels += [
            FieldPanel("property_meta_key"),
            FieldPanel("property_meta_desc"),
        ]

    if getattr(settings, "MODULE_EVENT", False):
        panels += [
            FieldPanel("event_meta_key"),
            FieldPanel("event_meta_desc"),
        ]


@register_setting
class DisplayFlag(BaseGenericSetting):
    display_floating_whatsapp   = models.BooleanField(default=True)

    panels = [
        FieldPanel("display_floating_whatsapp"),
    ]


@register_setting
class ThemeSetting(BaseGenericSetting):
    primary_color           = ColorField(default="#0846b4")
    secondary_color         = ColorField(default="#2a7aff")

    panels = [
        FieldPanel("primary_color"),
        FieldPanel("secondary_color"),
    ]
