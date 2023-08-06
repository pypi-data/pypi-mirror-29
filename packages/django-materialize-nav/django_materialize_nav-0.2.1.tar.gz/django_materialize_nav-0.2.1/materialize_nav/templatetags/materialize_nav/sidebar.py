from .base import register


__all__ = ["render_sidebar_nav", "render_sidebar_search", "render_sidebar_navheader", "render_sidebar_navitem"]


# ========== Sidebar ==========
@register.inclusion_tag("materialize_nav/sidebar/sidebar_nav.html", takes_context=True)
def render_sidebar_nav(context):
    """Render sidebar navigation"""
    return context


@register.inclusion_tag("materialize_nav/sidebar/sidebar_search.html", takes_context=True)
def render_sidebar_search(context, search_url=None, search_name=None, search_filters=None):
    """Render a sidebar Search."""
    if search_url:
        context["SearchURL"] = search_url
    if search_name:
        context["SearchName"] = search_name
    if search_filters:
        if isinstance(search_filters, str):
            context["SearchFilters"] = search_filters.split(",")
        else:
            # Assume list
            context["SearchFilters"] = search_filters
    return context


@register.inclusion_tag("materialize_nav/sidebar/sidebar_navheader.html")
def render_sidebar_navheader(navheader):
    """Render a sidebar NavHeader."""
    return {"navheader": navheader}


@register.inclusion_tag("materialize_nav/sidebar/sidebar_navitem.html")
def render_sidebar_navitem(navitem, is_header=False):
    """Render a sidebar NavItem."""
    return {"navitem": navitem, "is_header": is_header}
# ========== END Sidebar ==========
