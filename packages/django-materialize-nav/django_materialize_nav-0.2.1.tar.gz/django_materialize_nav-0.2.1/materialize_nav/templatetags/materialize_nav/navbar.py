from .base import register

from materialize_nav.views import NavView, NavHeader


__all__ = ["is_nav_header", "render_nav", "render_navbar_items",
           "render_navbar_header", "render_navbar_dropdown_items", "render_navbar_navitem"]


@register.simple_tag
def is_nav_header(item):
    return isinstance(item, NavHeader)


@register.inclusion_tag("materialize_nav/navbar/nav.html", takes_context=True)
def render_nav(context, has_panel=None):
    """Render a navigation sidebar that hides on large devices using the title bar for navigation."""
    # if not hasattr(context["request"], "nav_context_loaded") or not context["request"].nav_context_loaded:
    #     context = NavView.get_context(context['request'], context)
    if has_panel is not None:
        context["SidePanel"] = has_panel
    return context


@register.inclusion_tag("materialize_nav/navbar/navbar_items.html", takes_context=True)
def render_navbar_items(context, AppNavigation=None):
    """Render top navbar items."""
    return {"user": context["request"].user, 'AppNavigation': AppNavigation}


@register.inclusion_tag("materialize_nav/navbar/navbar_header.html")
def render_navbar_header(navheader):
    render_dropdown = navheader.is_header() and navheader.label != ""
    return {'navheader': navheader, "render_dropdown": render_dropdown}


@register.inclusion_tag("materialize_nav/navbar/navbar_dropdown_items.html")
def render_navbar_dropdown_items(item):
    return {'navheader': item}


@register.inclusion_tag("materialize_nav/navbar/navbar_navitem.html")
def render_navbar_navitem(nav_item, nav_icon_blank=False):
    return {'nav_item': nav_item, "nav_icon_blank": nav_icon_blank}
