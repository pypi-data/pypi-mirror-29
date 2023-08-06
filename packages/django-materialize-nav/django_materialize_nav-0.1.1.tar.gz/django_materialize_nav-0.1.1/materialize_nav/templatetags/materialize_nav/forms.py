from .base import register


__all__ = ["render_delete_btn", "render_filter"]


@register.inclusion_tag("materialize_nav/forms/delete_btn_template.html", takes_context=True)
def render_delete_btn(context, delete_instance, check_super_user=True, check_owner=True):
    """Render a delete button for a form.

    Args:
        context (Context): Passed in automatically
        delete_instance (object): Model object instance. Usuall from "form.instance". Must have "get_delete_url".
        check_super_user (bool)[True]: Check if the user is a super user in order to delete
        check_owner (bool)[True]: Check if the user is the owner in order to delete
    """

    try:
        user = context["request"].user
        try:
            is_super = user.is_superuser or user.is_elevated
        except AttributeError:
            is_super = user.is_superuser

        context["can_delete"] = True
        if check_super_user and not is_super:
            context["can_delete"] = False
        elif ((check_owner and not is_super) and
              (hasattr(delete_instance, "owner") and delete_instance.owner != user) or
              (hasattr(delete_instance, "user") and delete_instance.user != user)):
            context["can_delete"] = False
    except:
        pass
    context["delete_instance"] = delete_instance
    return context


@register.inclusion_tag("materialize_nav/forms/filter.html")
def render_filter(filt):
    return {"filter": filt}


# ========== Form Fields ==========
from django.forms import TypedChoiceField

@register.inclusion_tag("materialize_nav/forms/render_form_field.html")
def render_form_field(field, label=None, input_type=None, is_hidden=None, inline=False, style="", input_class="",):
    """Render form field. Should move to crispy forms someday."""
    if label is not None:
        field.label = label
    if input_type is None:
        try:
            input_type = field.field.widget.input_type
        except AttributeError:
            type_ = str(field.field.widget).lower()
            if isinstance(field.field.widget, TypedChoiceField):
                input_type = "autocomplete"
            elif "select" in type_:
                input_type = "select"
            elif "textarea" in type_:
                input_type = "textarea"
            else:
                input_type = "checkbox"
    if is_hidden is None:
        is_hidden = field.is_hidden

    return {"field": field, "input_type": input_type, "is_hidden": is_hidden,
            "inline": inline, "style": style, "input_class": input_class, "widget": field.field.widget}
