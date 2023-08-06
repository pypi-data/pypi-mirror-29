from django.db.models import Q
from django.http import JsonResponse

from ..navigation.template_mixin import TemplateMixin


__all__ = ['AutocompleteView']


class AutocompleteView(TemplateMixin):
    model = None
    query_name = "query"
    lookup_expr = "name__istartswith"  # ['name__icontains', 'description__icontains']

    def get_queryset(self):
        """Return the general queryset for all objects."""
        return self.model.objects.all()

    def get_lookup_expr(self):
        """Return a list of names to use for the query filter."""
        if isinstance(self.lookup_expr, (list, tuple)):
            return self.lookup_expr
        return [self.lookup_expr]

    def filter_queryset(self, qs, filt):
        """Filter and return the new queryset.

        Args:
            qs (QuerySet): Queryset that needs to be filtered.
            filt (str): Filter parameter that was passed to this view.

        Returns:
            qs (QuerySet): The filtered queryset to use.
        """
        q = Q()
        for lookup in self.get_lookup_expr():
            q = q | Q(**{lookup: filt})
        qs = qs.filter(q)
        return qs

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        filt = request.GET.get(self.query_name, None)
        if filt:
            qs = self.filter_queryset(qs, filt)
        return JsonResponse(qs, status=200)
