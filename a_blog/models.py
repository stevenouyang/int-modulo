from django.db import models
from django.urls import reverse
# from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from autoslug import AutoSlugField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit, Adjust
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks
from wagtail.models import Page
from django.db.models.signals import pre_save
from django.dispatch import receiver
import math
import uuid
import os
from bs4 import BeautifulSoup
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from django.shortcuts import render, get_object_or_404
from .utils import process_blog_content


class BlogIndex(RoutablePageMixin, Page):
    template = "page/blog_index.html"

    subpage_types = ['blog.Blog']
    parent_page_types = ['home.HomePage']
    max_count = 1

    # Main listing page: /blog/
    def get_context(self, request):
        context = super().get_context(request)
        context['posts'] = Blog.objects.live().descendant_of(self)
        return context


class BlogCategory(index.Indexed, models.Model):
    name = models.CharField(max_length=30, blank=False)
    slug = AutoSlugField(populate_from="name", blank=True, null=True)
    image = models.ImageField(upload_to="blog/category", null=True, default=None)

    # date
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    search_fields = [
        index.SearchField("name"),
    ]

    panels = [
        FieldPanel("name"),
        FieldPanel("image"),
    ]

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse("portfolio:blog_list") + f"?category={self.slug}"

    def get_absolute_url(self):
        return self.get_url()


class Blog(Page):
    template = "page/blog_details.html"
    parent_page_types = ['blog.BlogIndex']
    subpage_types = []

    date = models.DateField("Post date")
    small_description = models.TextField(blank=True, null=True)

    category = models.ForeignKey(
        BlogCategory,
        blank=True,
        null=True,
        related_name="blog_category",
        on_delete=models.SET_NULL,
    )
    is_approved = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=False)

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
    total_visit = models.IntegerField(null=True, blank=True)
    reading_time = models.IntegerField(null=True, blank=True)


    content_panels = [
        FieldPanel("title"),

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
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ['-date']

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

