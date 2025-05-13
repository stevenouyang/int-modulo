from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, TitleFieldPanel
from wagtail.search import index
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks
from wagtail.models import Page
from django.db.models.signals import pre_save
from django.dispatch import receiver
import math
from bs4 import BeautifulSoup
from wagtail.contrib.routable_page.models import RoutablePageMixin
from .utils import process_blog_content
from django.conf import settings


class BlogIndex(RoutablePageMixin, Page):
    template            = "a_page/page/dummy.html"

    subpage_types       = ['a_blog.Blog']
    parent_page_types   = ['home.HomePage']
    max_count           = 1

    # Main listing page: /blog/
    def get_context(self, request):
        context             = super().get_context(request)
        context['posts']    = Blog.objects.live().descendant_of(self)
        return context


class BlogCategory(index.Indexed, models.Model):
    name                = models.CharField(max_length=30, blank=False)
    slug                = AutoSlugField(populate_from="name", blank=True, null=True)
    image               = models.ImageField(upload_to="blog/category", null=True, default=None, blank=True)

    # date
    date_created        = models.DateTimeField(auto_now_add=True)
    date_updated        = models.DateTimeField(auto_now=True)

    search_fields = [
        index.SearchField("name"),
    ]

    panels = [
        TitleFieldPanel("name"),
        FieldPanel("image"),
    ]

    if getattr(settings, "BLOG_CATEGORY_IMAGE", False):
        panels += [
            FieldPanel("image"),
        ]

    def __str__(self):
        return self.name


class Blog(Page):
    template                = "a_blog/page/details.html"
    parent_page_types       = ['a_blog.BlogIndex']
    subpage_types           = []

    date                    = models.DateField("Post date")
    small_description       = models.TextField(blank=True, null=True)

    category                = models.ForeignKey(
                                BlogCategory,
                                blank=True,
                                null=True,
                                related_name="blog_category",
                                on_delete=models.SET_NULL,
                            )
    is_approved             = models.BooleanField(default=False)
    is_recommended          = models.BooleanField(default=False)

    image                   = models.ImageField(upload_to="blog/content", null=True, default=None)
    image_processed         = ImageSpecField(
                                source="image",
                                processors=[ResizeToFill(1920, 600)],
                                format="webP",
                                options={"quality": 90},
                            )
    image_thumbnail         = ImageSpecField(
                                source="image",
                                processors=[ResizeToFill(960, 540)],
                                format="webP",
                                options={"quality": 90},
                            )

    content                 = StreamField(
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

    # data
    total_visit             = models.IntegerField(null=True, blank=True)
    reading_time            = models.IntegerField(null=True, blank=True)


    content_panels          = [
                                TitleFieldPanel("title"),

                                FieldPanel("date"),
                                FieldPanel("category"),
                                FieldPanel("small_description"),
                                MultiFieldPanel([
                                    FieldPanel("is_approved"),
                                    FieldPanel("is_recommended"),
                                ], heading="Approval Settings"),
                                FieldPanel("image"),
                                FieldPanel("content"),
                            ]


    class Meta:
        verbose_name        = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering            = ['-date']

    def __str__(self):
        return self.title

    def get_processed_content(self):
        """
        Returns a processed version of the StreamField content with
        resized image URLs and list items extracted.
        """
        from copy import deepcopy
        content_copy = deepcopy(self.content)
        process_blog_content(content_copy)

        print("processing blog content")
        return content_copy


@receiver(pre_save, sender=Blog)
def calculate_reading_time(sender, instance, **kwargs):
    content_text = ""

    if instance.content:
        for block in instance.content:
            if block.block_type == "paragraph":
                content_text += BeautifulSoup(
                    block.value.source, "html.parser"
                ).get_text()
            elif block.block_type in ["h4", "h6"]:
                content_text += block.value
            elif block.block_type == "ordered_list":
                content_text += BeautifulSoup(
                    block.value.source, "html.parser"
                ).get_text()
            elif block.block_type == "unordered_list":
                content_text += BeautifulSoup(
                    block.value.source, "html.parser"
                ).get_text()
            elif block.block_type in ["blockquote_1"]:
                content_text += block.value

        content_length = len(content_text)
        print("Content Length :", content_length)

        avg_reading_speed = 800

        reading_time = math.ceil(content_length / avg_reading_speed)

        instance.reading_time = reading_time
