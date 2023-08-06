from django.views.generic.detail import SingleObjectMixin
from django.views.generic.list import MultipleObjectMixin
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View


__all__ = ['TemplateMixin']


class TemplateMixin(TemplateResponseMixin, ContextMixin, View):
    """Make the view work like a regular template view."""
    def __init__(self, *args, **kwargs):
        if isinstance(self, MultipleObjectMixin) and not hasattr(self, "object_list"):
            self.object_list = None
        elif isinstance(self, SingleObjectMixin) and not hasattr(self, "object"):
            self.object = None
        super().__init__(*args, **kwargs)

    @classmethod
    def get_context(cls, request, context=None, **kwargs):
        if context is None:
            context = {}
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.get_context(self.request, context=context)
        return context

    def get(self, request, *args, **kwargs):
        if hasattr(super(), "get"):
            return super().get(request, *args, **kwargs)

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
