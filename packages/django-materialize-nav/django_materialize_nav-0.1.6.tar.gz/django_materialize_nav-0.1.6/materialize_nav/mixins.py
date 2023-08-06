from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin


__all__ = ["FilterMixin"]


def get_context_object_name(view):
    """Return the context_object_name for a view or None."""
    try:
        if isinstance(view, MultipleObjectMixin):
            return view.get_context_object_name(object_list=view.object_list)
        elif isinstance(view, SingleObjectMixin):
            return view.get_context_object_name(view.object)
        else:
            return view.get_context_object_name()
    except:
        try:
            return view.get_context_object_name()
        except:
            pass

    try:
        return view.context_object_name
    except:
        pass


class ViewMixin(object):
    def __init__(self, *args, **kwargs):
        self.object_list = None
        self.object = None
        self._modified_qs = None
        super().__init__(*args, **kwargs)

    def get_content_object(self, context):
        context_object_name = get_context_object_name(self)
        # Get the content that may be manipulated
        if context_object_name not in context:
            return None

        qs = context[context_object_name]
        if isinstance(self, FilterMixin) and self.context_filter_object_name:
            try:
                qs = getattr(qs, self.context_filter_object_name)
                qs = qs.all()
            except:
                pass
            context[self.context_filter_object_name] = qs

        return qs

    def set_content_object(self, context, qs, **kwargs):
        if isinstance(self, FilterMixin) and self.context_filter_object_name:
            context[self.context_filter_object_name] = qs
        else:
            context[get_context_object_name(self)] = qs

    def _modify_queryset(self, qs, **kwargs):
        """Actually modify the queryset."""
        return qs

    def modify_queryset(self, qs, **kwargs):
        """Method to modify a queryset and store the queryset in self._modified_qs. Ever parent call to this method that
        does modify the queryset should set self._modified_qs.
        """
        qs = self._modify_queryset(qs, **kwargs)
        self._modified_qs = qs
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self._modified_qs is None:
            qs = self.get_content_object(context)
            self.modify_queryset(qs)

        if self._modified_qs is not None:
            self.set_content_object(context, self._modified_qs)

        return context


class FilterMixin(ViewMixin):
    """Support for django-filter"""
    filter_class = None
    context_filter_name = 'filter'
    context_filter_object_name = None

    def __init__(self, *args, **kwargs):
        self._filter = None
        self._modified_qs = None
        super().__init__(*args, **kwargs)

    def filter_qs(self, qs):
        filt = self.filter_class(self.request.GET, queryset=qs)
        return filt, filt.qs

    def _modify_queryset(self, qs, page_size=None, **kwargs):
        """Actually modify the queryset."""
        qs = super()._modify_queryset(qs)

        if qs is not None:
            self._filter, qs = self.filter_qs(qs)

        return qs

    def modify_queryset(self, qs, **kwargs):
        """Method to modify a queryset and store the queryset in self._modified_qs. Ever parent call to this method that
        does modify the queryset should set self._modified_qs.
        """
        qs = super().modify_queryset(qs, **kwargs)
        if self._filter and self.filter_class:
            self._filter._qs = qs  # self._filter.qs is a property without a setter. set the underlying qs variable.
        return qs

    def set_content_object(self, context, qs, **kwargs):
        super().set_content_object(context, qs, **kwargs)
        context[self.context_filter_name] = self._filter
