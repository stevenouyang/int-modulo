from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel

# admin:
class WhatsappLog(models.Model):
    ip = models.CharField(max_length=50, blank=True, null=True)
    device = models.CharField(max_length=30, blank=True, null=True)
    final_url = models.URLField()
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("ip"),
                FieldPanel("device"),
                FieldPanel("final_url"),
                FieldPanel("whatsapp_number"),
            ],
            heading="Log Information",
        ),
    ]

    def __str__(self):
        return self.ip

# admin:
class WhatsappLog(models.Model):
    ip = models.CharField(max_length=50, blank=True, null=True)
    device = models.CharField(max_length=30, blank=True, null=True)
    final_url = models.URLField()
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("ip"),
                FieldPanel("device"),
                FieldPanel("final_url"),
                FieldPanel("whatsapp_number"),
            ],
            heading="Log Information",
        ),
    ]

    def __str__(self):
        return self.ip


# admin:
class PageVisitLog(models.Model):
    url = models.URLField()
    type = models.CharField(
        max_length=50, blank=True, null=True
    )
    # INDEX / BLOG_LIST / BLOG_DETAILS / PRODUCT_LIST / PRODUCT_DETAILS / PORTFOLIO_LIST / PORTFOLIO_DETAILS / PAGES
    ip = models.CharField(max_length=50, blank=True, null=True)
    user_agent = models.CharField(max_length=1000, blank=True, null=True)
    preferred_language = models.CharField(max_length=1000, blank=True, null=True)
    referer = models.CharField(max_length=1000, blank=True, null=True)

    # date
    created_at = models.DateTimeField(auto_now_add=True)

    panels = [
        FieldPanel("user"),
        FieldPanel("url"),
        FieldPanel("type"),
        FieldPanel("ip"),
        FieldPanel("user_agent"),
        FieldPanel("preferred_language"),
        FieldPanel("referer"),
    ]

    def __str__(self):
        return self.ip if not self.user else f"{self.user.username} - {self.ip}"
