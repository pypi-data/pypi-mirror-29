from django import template


__all__ = ["register", "get_url_modifiers"]


register = template.Library()


def get_url_modifiers(context):
    # ===== Sorting and Filtering support =====
    if "base_url" not in context:
        try:
            base_url = "?" + context["request"].get_full_path().split("?", 1)[1]
        except IndexError:
            base_url = "?"
        context["base_url"] = base_url
    else:
        base_url = context["base_url"]
    # ===== END Sorting =====

    # ===== Modify Page URL =====
    if "base_page_url" not in context:
        try:
            page_name = context["view"].page_kwarg
        except:
            page_name = "page"
        try:
            if page_name+"=" in base_url:
                start, end = base_url.split(page_name+"=", 1)
                if "&" in end:
                    rm, end = end.split("&", 1)
                else:
                    end = ""
                    if start.endswith("&"):
                        start = start[:-1]
                base_page_url = start + end + "&"+page_name+"="  # should end with "&"
            else:
                base_page_url = base_url + "&"+page_name+"="
        except IndexError:
            base_page_url = "?"+page_name+"="
        context["base_page_url"] = base_page_url
    # ===== END Modify Page URL =====

    return context
