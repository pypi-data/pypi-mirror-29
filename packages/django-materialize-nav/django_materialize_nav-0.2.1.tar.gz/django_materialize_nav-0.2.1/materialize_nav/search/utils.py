from ..navigation.utils import list_property


__all__ = ['SearchResult', 'list_property']


class SearchResult(list):
    """Search results. Stores information about a search.

    Args:
        results (QuerySet): Result queryset
        model (str): Model name.
        search_text (str): Test that was used in the search.
    """
    results = list_property(0, [])
    model = list_property(1, None)
    search_text = list_property(2, "")

    def __init__(self, results, model, search_text):
        super().__init__((results, model, search_text))
