from django.db import models
from wagtail.models import Page, Orderable
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from modelcluster.models import ClusterableModel
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from wagtail import blocks
from wagtail.fields import StreamField
from colorfield.fields import ColorField

# Create your models here.
class Parent(Page):
    template            = "a_page/page/parent.html"

    # subpage_types       = ['a_page.LinkDirectory']
    parent_page_types   = ['home.HomePage']
    max_count           = 1


class LinkDirectory(Page):
    template            = "a_page/page/link_dir.html"
    parent_page_types   = ['home.HomePage']
    max_count           = 1

    description = models.TextField(blank=True)
    enable_social_link = models.BooleanField(default=False)
    enable_floating_whatsapp = models.BooleanField(default=False)

    THEME_CHOICES = (
        ('light', 'Light'),
        ('dark', 'Dark'),
    )
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light')
    primary_color = ColorField(max_length=7, default='#0f0f0f')
    secondary_color = ColorField(max_length=7, default='#0f0f0f')
    background_color = ColorField(max_length=7, default='#f2f2f2')

    meta_title = models.CharField(max_length=255, blank=True)
    meta_desc = models.TextField(blank=True)
    meta_key = models.CharField(max_length=255, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('description'),
        MultiFieldPanel([
            FieldPanel('enable_social_link'),
            FieldPanel('enable_floating_whatsapp'),
            FieldPanel('theme'),
            FieldPanel('primary_color'),
            FieldPanel('secondary_color'),
            FieldPanel('background_color'),
        ], heading="Settings"),
        InlinePanel('link_items', label="Link Items"),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('meta_title'),
        FieldPanel('meta_desc'),
        FieldPanel('meta_key'),
    ]

    class Meta:
        verbose_name = "Link Directory Page"


class LinkItem(Orderable):
    TYPE_CHOICES = [
        ('link', 'Link'),
        ('image', 'Image'),
        ('text_content', 'Text Content'),
    ]

    page = ParentalKey(LinkDirectory, related_name='link_items')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='link')
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    link = models.URLField(blank=True)

    image = models.ImageField(upload_to="link_items/images", null=True, blank=True)
    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(1280, 720)],
        format='WEBP',
        options={'quality': 90}
    )

    text_content = StreamField(
        [
            (
                "paragraph",
                blocks.RichTextBlock(features=["p", "a"]),
            ),
            (
                "h4",
                blocks.CharBlock(features=["h4"]),
            ),
        ],
        use_json_field=True,
        null=True,
        blank=True,
    )

    panels = [
        FieldPanel('type'),
        FieldPanel('title'),
        FieldPanel('subtitle'),
        FieldPanel('link'),
        FieldPanel('image'),
        FieldPanel('text_content'),
    ]

    class Meta:
        verbose_name = "Link Item"


# class RateCard():
#     template            = "a_page/page/rate_card.html"
#     parent_page_types   = ['a_page.Parent']
#     max_count           = 1
#     pass


# class CV():
#     template            = "a_page/page/cv.html"
#     parent_page_types   = ['a_page.Parent']
#     max_count           = 1
#
#     pass
#
# class Misc():
#     template            = "a_page/page/misc.html"
#     parent_page_types   = ['a_page.Parent']
#     pass
#
# class About():
#     template            = "a_page/page/about.html"
#     parent_page_types   = ['a_page.Parent']
#     max_count           = 1
#     pass
#
# class Contact():
#     template            = "a_page/page/contact.html"
#     parent_page_types   = ['a_page.Parent']
#     max_count           = 1
#     pass
#
# # inline CV :
# class Experience():
#     parent_page_types       = ['a_page.Parent']
#     pass
#
# # inline CV :
# class Education():
#     parent_page_types       = ['a_page.Parent']
#     pass
#
# # inline CV :
# class Skill():
#     parent_page_types       = ['a_page.Parent']
#     pass
#
# # inline CV :
# class Certification():
#     parent_page_types       = ['a_page.Parent']
#     pass
#
# # inline RateCard :
# class RateCardItem():
#     parent_page_types       = ['a_page.Parent']
#     pass