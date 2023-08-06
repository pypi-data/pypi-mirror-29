from django import forms
from django.db.models import CharField, TextField, Q, ForeignKey

from .utils import SearchResult

from .widgets import StarSelectWidget


__all__ = ["SearchForm", "SearchResult", "StarSelectWidget"]


class SearchForm(forms.Form):
    models = []
    search = forms.CharField(max_length=255)

    @classmethod
    def get_search_results(cls, search_text, filters=None, models=None, search_related=False):
        """Return a list of search results.

        Args:
            search_text (str): Test to search with
            filters (str/list)[None]: Names of models to use. Empty means use all given models
            models (list)[None]: List of models to use (filters argument will reduce the models searched).
            search_related (bool)[False]: Search foreign keys.

        Returns:
            search_results (list): List of search results.
        """
        if models is None:
            models = cls.models

        if isinstance(filters, str):
            filters = [filt.strip() for filt in filters.split(",")]

        if filters is not None and len(filters) > 0:
            models = [model for model in models if model._meta.model_name.strip() in filters]

        search_results = []

        # Iterate over models and search
        for model in models:
            name = model._meta.verbose_name

            res = []
            try:
                model_fields = model._meta.get_fields()
                query = None
                for field in model_fields:
                    if isinstance(field, (CharField, TextField)):
                        if query is None:
                            query = Q(**{field.name+"__icontains": search_text})
                        else:
                            query |= Q(**{field.name+"__icontains": search_text})

                    elif search_related and isinstance(field, ForeignKey):
                        # Reverse foreign key search
                        n = field.name + "__"
                        for rel_f in field.related_model._meta.get_fields():
                            if isinstance(rel_f, (CharField, TextField)):
                                if query is None:
                                    query = Q(**{n + rel_f.name + "__icontains": search_text})
                                else:
                                    query |= Q(**{n + rel_f.name + "__icontains": search_text})

                res = model.objects.filter(query).distinct()
                if len(res) == 0:
                    continue
            except model.DoesNotExist:
                pass
            search_results.append(SearchResult(res, name.title(), search_text))

        return search_results


class StarSelectField(forms.ChoiceField):
    widget = StarSelectWidget

    def __init__(self, *args, **kwargs):
        if "label" not in kwargs:
            kwargs["label"] = ''
        super().__init__(*args, **kwargs)
