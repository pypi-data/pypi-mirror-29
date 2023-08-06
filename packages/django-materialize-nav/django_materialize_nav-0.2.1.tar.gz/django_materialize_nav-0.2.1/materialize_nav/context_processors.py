from .views import NavView


def nav(request):
    """Context processor to add nav context to every view.

    Args:
        request (HttpRequest): http request.
    """
    # Check if materialize_nav has already loaded the conext
    if hasattr(request, "nav_context_loaded") and request.nav_context_loaded:
        return {}
    return NavView.get_context(request)
