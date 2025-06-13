from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, TitleFieldPanel
from wagtail.search import index
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail import blocks
from wagtail.models import Page
from django.db.models.signals import pre_save
from django.dispatch import receiver
import math
from bs4 import BeautifulSoup
from wagtail.contrib.routable_page.models import RoutablePageMixin
from django.conf import settings


class ServiceIndex(RoutablePageMixin, Page):
    template = "a_page/page/dummy.html"

    subpage_types = ['a_service.Service']
    parent_page_types = ['home.HomePage']
    max_count = 1


class ServiceCategory(index.Indexed, models.Model):
    name = models.CharField(max_length=30, blank=False)
    slug = AutoSlugField(populate_from="name", blank=True, null=True)

    # date
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    search_fields = [
        index.SearchField("name"),
    ]

    panels = [
        TitleFieldPanel("name"),
    ]

    def __str__(self):
        return self.name


class Service(Page):
    template = "a_service/page/details.html"
    parent_page_types = ['a_service.ServiceIndex']
    subpage_types = []

    date = models.DateField("Post date")
    small_description = models.TextField(blank=True, null=True)

    category = models.ForeignKey(
        ServiceCategory,
        blank=True,
        null=True,
        related_name="service_category",
        on_delete=models.SET_NULL,
    )

    image = models.ImageField(upload_to="blog/content", null=True, default=None)
    image_processed = ImageSpecField(
        source="image",
        processors=[ResizeToFill(1920, 600)],
        format="webP",
        options={"quality": 90},
    )
    image_thumbnail = ImageSpecField(
        source="image",
        processors=[ResizeToFill(960, 540)],
        format="webP",
        options={"quality": 90},
    )

    content = StreamField(
        [
            (
                "paragraph",
                blocks.RichTextBlock(features=["p", "a"]),
            ),
            (
                "h4",
                blocks.CharBlock(features=["h4"]),
            ),
            (
                "h5",
                blocks.CharBlock(features=["h6"]),
            ),
            (
                "h6",
                blocks.CharBlock(features=["h6"]),
            ),
            (
                "ordered_list",
                blocks.RichTextBlock(
                    features=["ol"],
                ),
            ),
            (
                "unordered_list",
                blocks.RichTextBlock(
                    features=["ul"],
                ),
            ),
            (
                "table",
                TableBlock(label="Table"),
            ),
            ("blockquote_1", blocks.CharBlock()),
            (
                "image_1280x720",
                ImageChooserBlock(label="Image 1280x720", help_text="1280 x 720"),
            ),
            (
                "image_1280x1280",
                ImageChooserBlock(label="Image 1280x1280", help_text="1280 x 1280"),
            ),
            (
                "image_1280x800",
                ImageChooserBlock(label="Image 1280x800", help_text="1280 x 800"),
            ),
            ("url", blocks.URLBlock()),
            ('button', blocks.StructBlock([
                ('text', blocks.CharBlock(required=True)),
                ('url', blocks.URLBlock(required=True)),
            ], icon='plus')),
            ("spacer", blocks.StaticBlock(label="Spacer")),
            ("html", blocks.RawHTMLBlock(label="Raw HTML", icon="code")),
        ],
        use_json_field=True,
        null=True,
        blank=True,
    )

    content_panels = [
        TitleFieldPanel("title"),
        FieldPanel("date"),
        FieldPanel("category"),
        FieldPanel("small_description"),
        FieldPanel("image"),
        FieldPanel("content"),
    ]

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['-date']

    def __str__(self):
        return self.title
