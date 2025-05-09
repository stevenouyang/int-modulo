from django.db import models
from wagtail.models import Page

# Create your models here.
class Parent(Page):
    template            = "a_page/page/parent.html"

    # subpage_types       = ['a_page.RateCard', 'a_page.LinkDirectory', 'a_page.CV', 'a_page.Misc', 'a_page.About', 'a_page.Contact']
    parent_page_types   = ['home.HomePage']
    max_count           = 1


# class RateCard():
#     template            = "a_page/page/rate_card.html"
#     parent_page_types   = ['a_page.Parent']
#     max_count           = 1
#     pass
#
# class LinkDirectory():
#     template            = "a_page/page/link_dir.html"
#     parent_page_types   = ['a_page.Parent']
#     max_count           = 1
#     pass
#
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