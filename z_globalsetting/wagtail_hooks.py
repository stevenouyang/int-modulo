from django.utils.html import format_html
from django.templatetags.static import static
from wagtail.admin.site_summary import PagesSummaryItem
from wagtail import hooks


@hooks.register("insert_global_admin_css")
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">', static("adminasset/theme.css")
    )


@hooks.register("construct_homepage_summary_items", order=1)
def hide_everything_except_pages_summary_for_partners(request, summary_items):
    summary_items[:] = []


@hooks.register("construct_main_menu")
def hide_default_menu_items(request, menu_items):
    # Remove 'Pages', 'Help', and 'Documents' menu items
    filtered_menu_items = [
        item
        for item in menu_items
        if item.name not in ["help", "images", "Task", "reports", "documents"]
    ]

    # Print every menu in the filtered_menu_items list
    # for item in filtered_menu_items:
    #     print(f"Menu Name: {item.name}, URL: {item.url}")

    # Assign the filtered_menu_items back to menu_items
    menu_items[:] = filtered_menu_items


@hooks.register("construct_settings_menu")
def hide_default_menu_items(request, menu_items):
    menu_items[:] = [
        item
        for item in menu_items
        if item.name
        not in ["workflows", "collections", "redirects", "workflow-tasks"]
    ]


@hooks.register("construct_admin_menu")
def hide_default_menu_items(request, menu_items):
    filtered_menu_items = [item for item in menu_items if item.name not in [""]]

    # Print every menu in the filtered_menu_items list
    for item in filtered_menu_items:
        print(f"Menu Name: {item.name}, URL: {item.url}")

    # Assign the filtered_menu_items back to menu_items
