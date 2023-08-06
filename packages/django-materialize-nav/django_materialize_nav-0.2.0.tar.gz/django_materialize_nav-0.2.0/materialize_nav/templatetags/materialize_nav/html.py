from django.utils.safestring import mark_safe

from .base import register
from ...utils import get_star_type

__all__ = ["include_materialize_header", "render_link_item", "define", "getitem", "getattribute", "replace"]


@register.inclusion_tag("materialize_nav/forms/widgets/stars.html")
def show_stars(ranking, num_stars=5, color="yellow"):
    stars = [get_star_type(i, ranking) for i in range(num_stars)]
    return {'widget': {'num_stars': num_stars, "ranking": ranking, "stars": stars, "color": color}}


@register.inclusion_tag("materialize_nav/html/materialize_header.html")
def include_materialize_header(icons=True, jquery=True, materializecss=True, style=True, stars=True, favicon=True,
                               ajax_helper=True):
    return {"icons": icons, "jquery": jquery, "materializecss": materializecss, "style": style, "stars": stars,
            "favicon": favicon, "ajax_helper": ajax_helper}


@register.inclusion_tag("materialize_nav/html/link_item.html")
def render_link_item(name, url=None, tooltip=None, icon="web_asset"):
    """Render a simple link item with an 'a' tag

    Args:
        name (str): Display name.
        url (str): Url string
        tooltip (str)[""]: Tooltip on hover.
        icon (str)["web_asset"]: Icon name. "web_asset", "add", "edit", ...
    """
    if not isinstance(name, str):
        icon_name = str(icon).lower()
        if url is None:
            if icon_name == "create" or icon_name == "add":
                icon_name = "add"
                try:
                    url = name.get_create_url()
                except AttributeError:
                    pass

            elif icon_name == "edit":
                try:
                    url = name.get_update_url()
                except AttributeError:
                    pass

            if url is None:
                try:
                    url = name.get_absolute_url()
                except AttributeError:
                    pass
        if tooltip is None:
            if icon_name == "add":
                tooltip = "Create Item"
            elif icon_name == "edit":
                tooltip = "Update Item"
            else:
                tooltip = "View Details"

        name = str(name)

    return {"name": name, "url": url, "tooltip": None, "icon": icon}  # Link tooltips cause too many divs


@register.simple_tag
def define(val=None):
    return val


@register.filter
def getitem(value, arg):
    try:
        return value[arg]
    except:
        pass
    return value[int(arg)]


@register.filter
def getattribute(value, arg, *, add=None, replace=None, replace_with=None):
    """Gets an attribute of an object dynamically from a string name"""
    arg = str(arg)
    if replace is not None and replace_with is not None:
        arg = arg.replace(str(replace), str(replace_with))

    if add is not None:
        arg = arg + str(add)

    return getattr(value, arg)


@register.filter
def replace(text, replace_with):
    text = str(text)
    rep, *replace_with = str(replace_with).split(",")
    for rep_with in replace_with:
        text = text.replace(rep, rep_with)
    return text
